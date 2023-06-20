from typing import Callable, Dict, List, Tuple

import numpy as np
from dynaconf import Dynaconf

from parallel_text_aligner import beam_search, noise
from parallel_text_aligner.alignment_search import anchors
from parallel_text_aligner.data.structures.bitext import Bitext
from parallel_text_aligner.data.structures.grid import Grid
from parallel_text_aligner.pairwise_score.scorer import get_scorer


class Searcher:
    """ """

    def __init__(self, scorer: Callable[[str], float], config: Dynaconf) -> None:
        self.scorer = scorer
        ...

    def naive_beam_search(
        self, grid: Grid, bitext: Bitext
    ) -> Tuple[
        List[Tuple[int, int]], Dict[Tuple[int, int], float], Tuple[float, float, float]
    ]:  # last one is for scores; quantities and details TBD
        ...

    def anchored_beam_search(
        self, grid: Grid, bitext: Bitext, anchors: List[Tuple[int, int]]
    ) -> Tuple[
        List[Tuple[int, int]], Dict[Tuple[int, int], float], Dict[str, float]
    ]:  # last one is for some custom metrics; quantities and details TBD
        anchors, scores = self.find_anchors(grid, bitext)
        # TODO
        alignment: List[Tuple[int, int]] = ...
        scores: Dict[Tuple[int, int], float] = ...
        metrics: Dict[str, float] = ...
        return alignment, scores, metrics

    def find_anchors(
        self, grid: Grid, bitext: Bitext
    ) -> Tuple[List[Tuple[int, int]], np.ndarray]:
        anchors: List[Tuple[int, int]] = ...
        scores: np.ndarray = ...
        return anchors, scores


class SearcherFactory:
    """ """

    def __init__(self, config) -> None:
        self.scorer = get_scorer(config)
        ...

    def get_searcher(self) -> Searcher:
        return Searcher(self.scorer)


def get_searcher(config) -> Searcher:
    factory = SearcherFactory(config)
    return factory.get_searcher()
