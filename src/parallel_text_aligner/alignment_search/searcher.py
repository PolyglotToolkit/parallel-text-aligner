from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
from dynaconf import Dynaconf

from parallel_text_aligner import beam_search, noise
from parallel_text_aligner.alignment_search import anchors
from parallel_text_aligner.data.structures.bitext import Bitext
from parallel_text_aligner.data.structures.grid import Grid
from parallel_text_aligner.pairwise_score.scorer import get_scorer


class Searcher:
    """ """

    def __init__(self, scorer: Callable[[str, str], float], config: Dynaconf) -> None:
        self.scorer = scorer

        ...

    def naive_beam_search(
        self, grid: Grid, bitext: Bitext
    ) -> Tuple[
        List[Tuple[int, int]], Dict[Tuple[int, int], float], Dict[str, float]
    ]:  
        """
        
        """
        alignment: List[Tuple[int, int]] = []
        scores: Dict[Tuple[int, int], float] = {}
        metrics: Dict[str, float] = {}

        i, j = 0, 0
        imax, jmax = grid.shape()
        while (i < imax) and (j < jmax):
            pairs = [bitext[i,j], bitext[i:i+2, j], bitext[i, j:j+2], bitext[i, j+1], bitext[i+1, j]]

            scores = list(map(self.scorer, [pairs]))
            best = np.argmax(scores)
            # TODO
        

    def anchored_beam_search(
        self, grid: Grid, bitext: Bitext, anchors: List[Tuple[int, int]]
    ) -> Tuple[
        List[Tuple[int, int]], Dict[Tuple[int, int], float], Dict[str, float]
    ]:  # last one is for some custom metrics; quantities and details TBD
        anchors, scores = self.find_anchors(grid, bitext)
        
        alignment: List[Tuple[int, int]] = []
        scores: Dict[Tuple[int, int], float] = {}
        metrics: Dict[str, float] = {}

        # alignment loop between anchors
        for (a1, b1), (a2, b2) in zip(anchors[:-1], anchors[1:]):
            subgrid = grid[a1:a2, b1:b2]
            subbitext = bitext[a1:a2, b1:b2]
            subalignment, subscores, _ = self.naive_beam_search(subgrid, subbitext)
            alignment.extend(subalignment)

        alignment = sorted(list(set(alignment)))
        
        return alignment, scores, metrics

    def find_anchors(
        self, bitext: Bitext, max_anchors: Optional[int] = None, score_weights: dict[str, float] = {}
    ) -> Tuple[List[Tuple[int, int]], np.ndarray]:
        anchors: List[Tuple[int, int]] = ...
        original_scores: np.ndarray = Grid.from_bitext(bitext)
        scores = original_scores.padded(padding=1, method="default")
        center = scores[1:-1, 1:-1]
        west = scores[:-2, 1:-1]  * score_weights.get("west",  1.0)
        east = scores[2:, 1:-1]   * score_weights.get("east",  1.0)
        north = scores[1:-1, :-2] * score_weights.get("north", 1.0)
        south = scores[1:-1, 2:]  * score_weights.get("south", 1.0)
        ne = scores[2:, :-2]      * score_weights.get("ne",    1.0)
        nw = scores[:-2, :-2]     * score_weights.get("nw",    1.0)
        se = scores[2:, 2:]       * score_weights.get("se",    1.0)
        sw = scores[:-2, 2:]      * score_weights.get("sw",    1.0)

        diffed = center + nw + se - west - east - north - south - ne - sw
        diffed = diffed - np.minimum(diffed) * original_scores.get_fat_mask()
        vals = np.flatten(diffed)
        cutoff = ... # get values more than h SDs above mean
        cutoff = min(sorted(list(set(vals * (vals >= cutoff))))[-(max_anchors or 9999):])
        anchors = list(zip(np.where(diffed > cutoff)[0]))
        scores = [original_scores[i, j] for i, j in anchors]

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
