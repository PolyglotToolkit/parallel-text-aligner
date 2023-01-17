# -*- coding: utf-8 -*-
from typing import Any

from parallel_text_aligner.pairwise_score import models, tokenizers


class Scorer:
    """ """

    def __init__(self) -> None:
        ...

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        ...


class ScorerFactory:
    """ """

    def __init__(self, config) -> None:
        ...

    def get_scorer(self, config) -> Scorer:
        return Scorer()


def get_scorer(config) -> Scorer:
    """ """
    factory = ScorerFactory(config)
    return factory.get_scorer()
