import copy
import os
import shutil
from argparse import ArgumentParser

import allesfitter
import astroplan
import matplotlib
from astroplan.plots import plot_airmass
from astropy.coordinates import SkyCoord, get_moon
import astropy.units as u
from astroplan import EclipsingSystem, moon_illumination, Constraint
import pandas as pd
import numpy as np
from astroplan import (Observer, FixedTarget, AtNightConstraint, AltitudeConstraint)
import matplotlib.pyplot as plt

from astropy.time import Time, TimeDelta
from lcbuilder.lcbuilder_class import LcBuilder
from pytz import timezone, utc
from timezonefinder import TimezoneFinder

from sherlockpipe.observation_report import ObservationReport


class MoonIlluminationSeparationConstraint(Constraint):
    """
    Constrain the distance between the Earth's moon and some targets.
    """

    def __init__(self, min_dist, max_dist):
        """
        Parameters
        ----------
        min_dist : `~astropy.units.Quantity`
            Minimum moon distance when moon illumination is 0
        max_dist : `~astropy.units.Quantity`
            Maximum moon distance when moon illumination is 1
        """
        self.min_dist = min_dist
        self.max_dist = max_dist

    def compute_constraint(self, times, observer, targets):
        """
        Computes the observability of the moon given a minimum distance to the moon between self.min_dist (for
        illumination = 0) and self.max_dist (for illumination = 1) by interpolating an intermediate distance from those
        two values following a linear regression.
        @param times: the times to compute the constraint for
        @param observer: the observer to compute the constraint for
        @param targets: the list of targets to compute the constraint for
        @return: the positive mask for target being observable for the given times and observer given the constraint
        is matched
        """
        # removed the location argument here, which causes small <1 deg
        # inaccuracies, but it is needed until astropy PR #5897 is released
        # which should be astropy 1.3.2
        moon = get_moon(times)
        # note to future editors - the order matters here
        # moon.separation(targets) is NOT the same as targets.separation(moon)
        # the former calculates the separation in the frame of the moon coord
        # which is GCRS, and that is what we want.
        moon_separation = moon.separation(targets)
        illumination = moon_illumination(times)
        min_dist = self.min_dist.value + (self.max_dist.value - self.min_dist.value) * illumination
        mask = min_dist <= moon_separation.degree
        return mask


def get_twin(ax):
    """
    Retrieves a twin Y axis for a given matplotlib axis. This is useful when we have two axes one placed at each side
    of the plot.
    @param ax: the known matplotlib axis.
    @return: the twin axis.
    """
    for other_ax in ax.figure.axes:
        if other_ax is ax:
            continue
        if other_ax.bbox.bounds == ax.bbox.bounds:
            return other_ax
    return None


def get_offset(lat, lng, datetime):
    """
    returns a location's time zone offset from UTC in minutes.
    """
    tf = TimezoneFinder()
    tz_target = timezone(tf.certain_timezone_at(lng=lng, lat=lat))
    if tz_target is None:
        return None
    today_target = tz_target.localize(datetime)
    today_utc = utc.localize(datetime)
    return (today_utc - today_target).total_seconds() / 3600


def create_observation_observables(object_id, object_dir, since, name, epoch, epoch_low_err, epoch_up_err, period,
                                   period_low_err, period_up_err, duration,
                                   observatories_file, timezone, latitude, longitude, altitude,
                                   max_days, min_altitude, moon_min_dist, moon_max_dist, transit_fraction, baseline,
                                   error_alert=True, time_unit='jd'):
    """

    @param object_id: the candidate id
    @param object_dir: the candidate directory
    @param since: starting plan date
    @param name: the name given to the candidate
    @param epoch: the candidate epoch
    @param epoch_low_err: the candidate epoch's lower error
    @param epoch_up_err: the candidate epoch's upper error
    @param period: the candidate period
    @param period_low_err: the candidate period's lower error
    @param period_up_err: the candidate period's upper error
    @param duration: the candidate duration
    @param observatories_file: the file containing the observatories file (csv format)
    @param timezone: the timezone of the observatory (if observatories_file=None)
    @param latitude: the latitude of the observatory (if observatories_file=None)
    @param longitude: the longitude of the observatory (if observatories_file=None)
    @param altitude: the altitude of the observatory (if observatories_file=None)
    @param max_days: the maximum number of days to compute the observables
    @param min_altitude: the minimum altitude of the target above the horizon
    @param moon_min_dist: the minimum moon distance for moon illumination = 0
    @param moon_max_dist: the minimum moon distance for moon illumination = 1
    @param transit_fraction: the minimum transit observability (0.25 for at least ingress/egress, 0.5 for ingress/egress
    + midtime, 1 for ingress, egress and midtime).
    @param baseline: the required baseline in hours.
    @param error_alert: whether to create the alert date to signal imprecise observations
    @param time_unit: the unit of the light curve data
    @return: the generated data and target folders
    """
    if observatories_file is not None:
        observatories_df = pd.read_csv(observatories_file, comment='#')
    else:
        observatories_df = pd.DataFrame(columns=['name', 'tz', 'lat', 'long', 'alt'])
        observatories_df = observatories_df.append("Obs-1", timezone, latitude, longitude, altitude)
    # TODO probably convert epoch to proper JD
    primary_eclipse_time = Time(epoch, format=time_unit, scale="tdb")
    target = FixedTarget(SkyCoord(coords, unit=(u.deg, u.deg)))
    n_transits = int(max_days // period)
    system = EclipsingSystem(primary_eclipse_time=primary_eclipse_time, orbital_period=u.Quantity(period, unit="d"),
                             duration=u.Quantity(duration, unit="h"), name=name)
    observables_df = pd.DataFrame(columns=['observatory', 'timezone', 'start_obs', 'end_obs', 'ingress', 'egress',
                                           'midtime', "midtime_up_err_h", "midtime_low_err_h", 'twilight_evening',
                                           'twilight_morning', 'observable', 'moon_phase', 'moon_dist'])
    plan_dir = object_dir + "/plan"
    images_dir = plan_dir + "/images"
    if os.path.exists(plan_dir):
        shutil.rmtree(plan_dir, ignore_errors=True)
    os.mkdir(plan_dir)
    if os.path.exists(images_dir):
        shutil.rmtree(images_dir, ignore_errors=True)
    os.mkdir(images_dir)
    alert_date = None
    for index, observatory_row in observatories_df.iterrows():
        observer_site = Observer(latitude=observatory_row["lat"], longitude=observatory_row["lon"],
                                 elevation=u.Quantity(observatory_row["alt"], unit="m"))
        midtransit_times = system.next_primary_eclipse_time(since, n_eclipses=n_transits)
        ingress_egress_times = system.next_primary_ingress_egress_time(since, n_eclipses=n_transits)
        constraints = [AtNightConstraint.twilight_nautical(), AltitudeConstraint(min=min_altitude * u.deg),
                       MoonIlluminationSeparationConstraint(min_dist=moon_min_dist * u.deg,
                                                            max_dist=moon_max_dist * u.deg)]
        moon_for_midtransit_times = get_moon(midtransit_times)
        moon_dist_midtransit_times = moon_for_midtransit_times.separation(
            SkyCoord(star_df.iloc[0]["ra"], star_df.iloc[0]["dec"], unit="deg"))
        moon_phase_midtransit_times = np.round(astroplan.moon_illumination(midtransit_times), 2)
        transits_since_epoch = np.round((midtransit_times - primary_eclipse_time).jd / period)
        midtransit_time_low_err = np.round(
            (((transits_since_epoch * period_low_err) ** 2 + epoch_low_err ** 2) ** (1 / 2)) * 24, 2)
        midtransit_time_up_err = np.round(
            (((transits_since_epoch * period_up_err) ** 2 + epoch_up_err ** 2) ** (1 / 2)) * 24, 2)
        low_err_delta = TimeDelta(midtransit_time_low_err * 3600, format='sec')
        up_err_delta = TimeDelta(midtransit_time_up_err * 3600, format='sec')
        i = 0
        for midtransit_time in midtransit_times:
            twilight_evening = observer_site.twilight_evening_nautical(midtransit_time)
            twilight_morning = observer_site.twilight_morning_nautical(midtransit_time)
            ingress = ingress_egress_times[i][0]
            egress = ingress_egress_times[i][1]
            lowest_ingress = ingress - low_err_delta[i]
            highest_egress = egress + up_err_delta[i]
            if error_alert and (highest_egress - lowest_ingress).jd > 0.33:
                alert_date = midtransit_time \
                    if (alert_date is None) or (alert_date is not None and alert_date >= midtransit_time) \
                    else alert_date
                break
            else:
                baseline_low = lowest_ingress - baseline * u.hour
                baseline_up = highest_egress + baseline * u.hour
                transit_times = baseline_low + (baseline_up - baseline_low) * np.linspace(0, 1, 100)
                observable_transit_times = astroplan.is_event_observable(constraints, observer_site, target,
                                                                   times=transit_times)[0]
                observable_transit_times_true = np.argwhere(observable_transit_times)
                observable = len(observable_transit_times_true) / 100
                if observable < transit_fraction:
                    i = i + 1
                    continue
                start_obs = transit_times[observable_transit_times_true[0]][0]
                end_obs = transit_times[observable_transit_times_true[len(observable_transit_times_true) - 1]][0]
                start_plot = baseline_low
                end_plot = baseline_up
                #TODO check whether twilight evening happens before twilight morning, if not, the check is different
                if twilight_evening > start_obs:
                    start_obs = twilight_evening
                if twilight_morning < end_obs:
                    end_obs = twilight_morning
            moon_dist = round(moon_dist_midtransit_times[i].degree)
            moon_phase = moon_phase_midtransit_times[i]
            # TODO get is_event_observable for several parts of the transit (ideally each 5 mins) to get the proper observable percent. Also with baseline
            if observatory_row["tz"] is not None and not np.isnan(observatory_row["tz"]):
                observer_timezone = observatory_row["tz"]
            else:
                observer_timezone = get_offset(observatory_row["lat"], observatory_row["lon"],
                                               midtransit_time.datetime)
            observables_df = observables_df.append({"observatory": observatory_row["name"],
                                                    "timezone": observer_timezone, "ingress": ingress.isot,
                                                    "start_obs": start_obs.isot, "end_obs": end_obs.isot,
                                                    "egress": egress.isot, "midtime": midtransit_time.isot,
                                                    "midtime_up_err_h":
                                                        str(int(midtransit_time_up_err[i] // 1)) + ":" +
                                                        str(int(midtransit_time_up_err[i] % 1 * 60)).zfill(2),
                                                    "midtime_low_err_h":
                                                        str(int(midtransit_time_low_err[i] // 1)) + ":" +
                                                        str(int(midtransit_time_low_err[i] % 1 * 60)).zfill(2),
                                                    "twilight_evening": twilight_evening.isot,
                                                    "twilight_morning": twilight_morning.isot,
                                                    "observable": observable, "moon_phase": moon_phase,
                                                    "moon_dist": moon_dist}, ignore_index=True)
            plot_time = start_plot + (end_plot - start_plot) * np.linspace(0, 1, 100)
            plt.tick_params(labelsize=6)
            airmass_ax = plot_airmass(target, observer_site, plot_time, brightness_shading=False, altitude_yaxis=True)
            airmass_ax.axvspan(twilight_morning.plot_date, end_plot.plot_date, color='white')
            airmass_ax.axvspan(start_plot.plot_date, twilight_evening.plot_date, color='white')
            airmass_ax.axvspan(twilight_evening.plot_date, twilight_morning.plot_date, color='gray')
            airmass_ax.axhspan(1. / np.cos(np.radians(90 - min_altitude)), 5.0, color='green')
            airmass_ax.get_figure().gca().set_title("")
            airmass_ax.get_figure().gca().set_xlabel("")
            airmass_ax.get_figure().gca().set_ylabel("")
            airmass_ax.set_xlabel("")
            airmass_ax.set_ylabel("")
            xticks = []
            xticks_labels = []
            xticks.append(start_obs.plot_date)
            hour_min_sec_arr = start_obs.isot.split("T")[1].split(":")
            xticks_labels.append("T1_" + hour_min_sec_arr[0] + ":" + hour_min_sec_arr[1])
            plt.axvline(x=start_obs.plot_date, color="violet")
            xticks.append(end_obs.plot_date)
            hour_min_sec_arr = end_obs.isot.split("T")[1].split(":")
            xticks_labels.append("T1_" + hour_min_sec_arr[0] + ":" + hour_min_sec_arr[1])
            plt.axvline(x=end_obs.plot_date, color="violet")
            if start_plot < lowest_ingress < end_plot:
                xticks.append(lowest_ingress.plot_date)
                hour_min_sec_arr = lowest_ingress.isot.split("T")[1].split(":")
                xticks_labels.append("T1_" + hour_min_sec_arr[0] + ":" + hour_min_sec_arr[1])
                plt.axvline(x=lowest_ingress.plot_date, color="red")
            if start_plot < ingress < end_plot:
                xticks.append(ingress.plot_date)
                hour_min_sec_arr = ingress.isot.split("T")[1].split(":")
                xticks_labels.append("T1_" + hour_min_sec_arr[0] + ":" + hour_min_sec_arr[1])
                plt.axvline(x=ingress.plot_date, color="orange")
            if start_plot < midtransit_time < end_plot:
                xticks.append(midtransit_time.plot_date)
                hour_min_sec_arr = midtransit_time.isot.split("T")[1].split(":")
                xticks_labels.append("T0_" + hour_min_sec_arr[0] + ":" + hour_min_sec_arr[1])
                plt.axvline(x=midtransit_time.plot_date, color="black")
            if start_plot < egress < end_plot:
                xticks.append(egress.plot_date)
                hour_min_sec_arr = egress.isot.split("T")[1].split(":")
                xticks_labels.append("T4_" + hour_min_sec_arr[0] + ":" + hour_min_sec_arr[1])
                plt.axvline(x=egress.plot_date, color="orange")
            if start_plot < highest_egress < end_plot:
                xticks.append(highest_egress.plot_date)
                hour_min_sec_arr = highest_egress.isot.split("T")[1].split(":")
                xticks_labels.append("T4_" + hour_min_sec_arr[0] + ":" + hour_min_sec_arr[1])
                plt.axvline(x=highest_egress.plot_date, color="red")
            airmass_ax.xaxis.set_tick_params(labelsize=5)
            airmass_ax.set_xticks([])
            airmass_ax.set_xticklabels([])
            degrees_ax = get_twin(airmass_ax)
            degrees_ax.yaxis.set_tick_params(labelsize=6)
            degrees_ax.set_yticks([1., 1.55572383, 2.])
            degrees_ax.set_yticklabels([90, 50, 30])
            fig = matplotlib.pyplot.gcf()
            fig.set_size_inches(1.25, 0.75)
            plt.savefig(plan_dir + "/images/" + observatory_row["name"] + "_" + str(midtransit_time.isot)[:-4] + ".png",
                        bbox_inches='tight')
            plt.close()
            i = i + 1
    observables_df = observables_df.sort_values(["midtime", "observatory"], ascending=True)
    observables_df.to_csv(plan_dir + "/observation_plan.csv", index=False)
    print("Observation plan created in directory: " + object_dir)
    return observatories_df, observables_df, alert_date, plan_dir, images_dir


if __name__ == '__main__':
    ap = ArgumentParser(description='Planning of observations from Sherlock objects of interest')
    ap.add_argument('--object_dir',
                    help="If the object directory is not your current one you need to provide the ABSOLUTE path",
                    required=False)
    ap.add_argument("--observatories", help="Csv file containing the observatories coordinates", required=False)
    ap.add_argument('--lat', help="Observer latitude", required=False)
    ap.add_argument('--lon', help="Observer longitude", required=False)
    ap.add_argument('--alt', help="Observer altitude", required=False)
    ap.add_argument('--tz', help="Time zone (in hours offset from UTC)", required=False)
    ap.add_argument('--min_altitude', help="Minimum altitude of the target to be observable", default=23,
                    required=False)
    ap.add_argument('--moon_min_dist', help="Minimum required moon distance for moon minimum illumination.", default=30,
                    required=False)
    ap.add_argument('--moon_max_dist', help="Minimum required moon distance for moon maximum illumination.", default=55,
                    required=False)
    ap.add_argument('--max_days', help="Maximum number of days for the plan to take.", type=int, default=365, required=False)
    ap.add_argument('--transit_fraction', help="Minimum transit fraction to be observable.", type=float, default=0.5,
                    required=False)
    ap.add_argument('--baseline', help="Required baseline (in hours) for the observation.", type=float, default=0.5,
                    required=False)
    ap.add_argument('--since', help="yyyy-mm-dd date since when you want to start the plan (defaults to today).",
                    type=str, default=None,
                    required=False)
    ap.add_argument('--error_sigma', help="Sigma to be used for epoch and period errors.", type=int, default=2,
                    required=False)
    ap.add_argument('--no_error_alert', help="Will not block imprecise observations to be plotted.",
                    action='store_true', required=False)
    ap.add_argument('--time_unit', help="Time unit to be used for the light curve measurements.", default=None,
                    required=False)
    args = ap.parse_args()
    if args.observatories is None and (args.lat is None or args.lon is None or args.alt is None):
        raise ValueError("You either need to set the 'observatories' property or the lat, lon and alt.")
    object_dir = os.getcwd() if args.object_dir is None else args.object_dir
    ns_derived_file = object_dir + "/results/ns_derived_table.csv"
    ns_file = object_dir + "/results/ns_table.csv"
    if not os.path.exists(ns_derived_file) or not os.path.exists(ns_file):
        raise ValueError("Bayesian fit posteriors files {" + ns_file + ", " + ns_derived_file + "} not found")
    star_df = pd.read_csv(object_dir + "/params_star.csv")
    object_id = star_df.iloc[0]["obj_id"]
    ra = star_df.iloc[0]["ra"]
    dec = star_df.iloc[0]["dec"]
    coords = str(ra) + " " + str(dec)
    fit_derived_results = pd.read_csv(object_dir + "/results/ns_derived_table.csv")
    fit_results = pd.read_csv(object_dir + "/results/ns_table.csv")
    candidates_count = len(fit_results[fit_results["#name"].str.contains("_period")])
    alles = allesfitter.allesclass(object_dir)
    since = Time.now() if args.since is None else Time(args.since, scale='utc')
    percentile = 99.7 if args.error_sigma == 3 else 95 if args.error_sigma == 2 else 68
    for i in np.arange(0, candidates_count):
        period_row = fit_results[fit_results["#name"].str.contains("_period")].iloc[i]
        period = period_row["median"]
        period_distribution = alles.posterior_params[period_row["#name"]]
        period_low_err = period - np.percentile(period_distribution, 50 - percentile / 2)
        period_up_err = np.percentile(period_distribution, 50 + percentile / 2) - period
        name = object_id + "_" + period_row["#name"].replace("_period", "")
        epoch_row = fit_results[fit_results["#name"].str.contains("_epoch")].iloc[i]
        epoch = epoch_row["median"].item()
        epoch_distribution = alles.posterior_params[epoch_row["#name"]]
        epoch_low_err = epoch - np.percentile(epoch_distribution, 50 - percentile / 2)
        epoch_up_err = np.percentile(epoch_distribution, 50 + percentile / 2) - epoch
        duration_row = fit_derived_results[fit_derived_results["#property"].str.contains("Total transit duration")].iloc[i]
        duration = duration_row["value"].item()
        duration_low_err = float(duration_row["lower_error"])
        duration_up_err = float(duration_row["upper_error"])
        depth_row = fit_derived_results[fit_derived_results["#property"].str.contains("depth \(dil.\)")].iloc[i]
        depth = depth_row["value"] * 1000
        depth_low_err = depth_row["lower_error"] * 1000
        depth_up_err = depth_row["upper_error"] * 1000
        mission, mission_prefix, id_int = LcBuilder().parse_object_info(object_id)
        if args.time_unit is None and mission == "TESS":
            time_unit = 'btjd'
        elif args.time_unit is None and mission == "Kepler" or mission == "K2":
            time_unit = 'bkjd'
        elif args.time_unit is not None:
            time_unit = args.time_unit
        else:
            time_unit = 'jd'
        observatories_df, observables_df, alert_date, plan_dir, images_dir = create_observation_observables(object_id, object_dir,
                                                                                                since, name, epoch,
                                                            epoch_low_err, epoch_up_err, period, period_low_err,
                                                            period_up_err, duration, args.observatories, args.tz, args.lat,
                                                            args.lon, args.alt, args.max_days, args.min_altitude,
                                                            args.moon_min_dist, args.moon_max_dist, args.transit_fraction,
                                                            args.baseline, not args.no_error_alert, time_unit)
        report = ObservationReport(observatories_df, observables_df, alert_date, object_id, name, plan_dir, ra, dec,
                                   epoch, epoch_low_err, epoch_up_err, period, period_low_err, period_up_err, duration,
                                   duration_low_err, duration_up_err, depth, depth_low_err, depth_up_err,
                                   args.transit_fraction, args.moon_min_dist, args.moon_max_dist, args.min_altitude,
                                   args.max_days, star_df.iloc[0]["v"], star_df.iloc[0]["j"], star_df.iloc[0]["h"],
                                   star_df.iloc[0]["k"])
        report.create_report()
        shutil.rmtree(images_dir, ignore_errors=True)
