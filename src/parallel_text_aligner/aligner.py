# -*- coding: utf-8 -*-
import hydra

from parallel_text_aligner.alignment_search.searcher import get_searcher
from parallel_text_aligner.common.config import CONFIG
from parallel_text_aligner.common.locations import Locations
from parallel_text_aligner.data_handling.data_handler import get_data_handler


class Aligner:
    """ """

    def __init__(self, cfg) -> None:
        self.cfg = cfg
        self.locations = Locations
        self.dh = get_data_handler(cfg)
        self.searcher = get_searcher(cfg)

        self.dh.load()

    def align(self) -> None:
        ...

    def save(self) -> None:
        ...


class AlignerFactory:
    ...


@hydra.main(version_base=None, config_path=Locations.DIR_CONFIG, config_name="default")
def get_aligner():
    ...


# alignment approach:
# 1) across all weight intersections +- k, compute scores
# 2) keep as "anchors" the highest-scoring (relative to neighbors)
# 3) use beam search to find best paths
