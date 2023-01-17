# -*- coding: utf-8 -*-
from parallel_text_aligner import beam_search, noise
from parallel_text_aligner.alignment_search import anchors


class Searcher:
    """ """

    def __init__(self) -> None:
        ...


class SearcherFactory:
    """ """

    def __init__(self, config) -> None:
        ...

    def get_searcher(self) -> Searcher:
        return Searcher()


def get_searcher(config) -> Searcher:
    factory = SearcherFactory(config)
    return factory.get_searcher()
