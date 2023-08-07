import logging

import foldedleastsquares
import numpy as np
from lcbuilder.helper import LcbuilderHelper


class ToolWithCandidate:
    def __init__(self, is_candidate_from_search, candidates_df) -> None:
        super().__init__()
        self.is_candidate_from_search = is_candidate_from_search
        self.search_candidates_df = candidates_df

    def mask_previous_candidates(self, time, flux, flux_err, candidate_id):
        if self.is_candidate_aware():
            for index in np.arange(0, candidate_id - 1):
                candidate_row = self.search_candidates_df.iloc[index]
                period = candidate_row["period"]
                duration = candidate_row["duration"]
                duration = duration / 60 / 24
                t0 = candidate_row["t0"]
                logging.info("Masking candidate number %.0f with P=%.3fd, T0=%.2f and D=%.2fd", index + 1, period, t0,
                             duration)
                time, flux, flux_err = LcbuilderHelper.mask_transits(time, flux, period, duration * 2, t0, flux_err)
        return time, flux, flux_err


    def is_candidate_aware(self):
        return self.is_candidate_from_search