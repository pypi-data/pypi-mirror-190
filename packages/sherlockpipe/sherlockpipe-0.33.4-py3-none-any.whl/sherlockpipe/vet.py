import logging
import yaml
from argparse import ArgumentParser
import sys
import pandas as pd
import os
from watson.watson import Watson

from sherlockpipe.tool_with_candidate import ToolWithCandidate


class Vetter(ToolWithCandidate):
    watson = None

    def __init__(self, object_dir, is_candidate_from_search, candidates_df) -> None:
        super().__init__(is_candidate_from_search, candidates_df)
        self.watson = Watson(object_dir)

    def run(self, cpus, **kwargs):
        self.watson.vetting_with_data(kwargs['candidate'], kwargs['star_df'], kwargs['transits_df'],
                                      cpus, transits_mask=kwargs["transits_mask"])

    def object_dir(self):
        return self.watson.object_dir


def run_vet(object_dir, candidate, properties, cpus=os.cpu_count() - 1):
    object_dir = os.getcwd() if object_dir is None else object_dir
    candidates = pd.read_csv(object_dir + "/candidates.csv")
    vetter = Vetter(object_dir, candidate is not None, candidates)
    file_dir = vetter.watson.object_dir + "/vetting.log"
    if os.path.exists(file_dir):
        os.remove(file_dir)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()
    while len(logger.handlers) > 0:
        logger.handlers.pop()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler = logging.FileHandler(file_dir)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logging.info("Starting vetting")
    star_df = pd.read_csv(vetter.object_dir() + "/params_star.csv")
    transits_df = None
    if candidate is None:
        user_properties = yaml.load(open(properties), yaml.SafeLoader)
        candidate = pd.DataFrame(columns=['id', 'period', 'depth', 't0', 'sectors', 'number', 'lc'])
        candidate = candidate.append(user_properties, ignore_index=True)
        candidate['id'] = star_df.iloc[0]["obj_id"]
    else:
        candidate_selection = int(candidate)
        if candidate_selection < 1 or candidate_selection > len(candidates.index):
            raise SystemExit("User selected a wrong candidate number.")
        candidates = candidates.rename(columns={'Object Id': 'id'})
        candidate = candidates.iloc[[candidate_selection - 1]]
        candidate['number'] = [candidate_selection]
        transits_df_file = vetter.object_dir() + "/transits_stats.csv"
        if os.path.exists(transits_df_file):
            transits_df = pd.read_csv(vetter.object_dir() + "/transits_stats.csv")
            transits_df = transits_df[transits_df["candidate"] == candidate_selection - 1]
        # watson.data_dir = watson.object_dir
        logging.info("Selected signal number " + str(candidate_selection))
    transits_mask = []
    for i in range(0, int(candidate['number']) - 1):
        transits_mask.append({"P": candidates.iloc[i]["period"], "T0": candidates.iloc[i]["t0"],
                              "D": candidates.iloc[i]["duration"] * 2})
    vetter.run(cpus, candidate=candidate, star_df=star_df.iloc[0], transits_df=transits_df, transits_mask=transits_mask)


if __name__ == '__main__':
    ap = ArgumentParser(description='Vetting of Sherlock objects of interest')
    ap.add_argument('--object_dir', help="If the object directory is not your current one you need to provide the "
                                         "ABSOLUTE path", required=False)
    ap.add_argument('--candidate', type=int, default=None, help="The candidate signal to be used.", required=False)
    ap.add_argument('--properties', help="The YAML file to be used as input.", required=False)
    ap.add_argument('--cpus', type=int, default=None, help="The number of CPU cores to be used.", required=False)
    args = ap.parse_args()
    run_vet(args.object_dir, args.candidate, args.properties, args.cpus)
