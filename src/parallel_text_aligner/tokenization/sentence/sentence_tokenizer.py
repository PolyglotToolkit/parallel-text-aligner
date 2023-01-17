# -*- coding: utf-8 -*-
from typing import Any


class SentenceTokenizer:
    """ """

    def __init__(self) -> None:
        ...

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        ...


class SentenceTokenizerFactory:
    """ """

    def __init__(self, config) -> None:
        ...

    def get_sentence_tokenizer(self, config) -> SentenceTokenizer:
        return SentenceTokenizer()


def get_sentence_tokenizer(config) -> SentenceTokenizer:
    """ """
    factory = SentenceTokenizerFactory(config)
    return factory.get_sentence_tokenizer()
