from parallel_text_aligner import beam_search, noise
from parallel_text_aligner.alignment_search import anchors
from parallel_text_aligner.pairwise_score.scorer import get_scorer


class Searcher:
    """ """

    def __init__(self, scorer) -> None:
        self.scorer = scorer
        ...


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
