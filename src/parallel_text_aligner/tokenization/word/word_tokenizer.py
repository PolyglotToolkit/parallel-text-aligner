from typing import Any


class WordTokenizer():
    """

    """

    def __init__(self) -> None:
        ...

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        ...


class WordTokenizerFactory():
    """

    """

    def __init__(self, config) -> None:
        ...

    def get_word_tokenizer(self, config) -> WordTokenizer:
        return WordTokenizer()


def get_word_tokenizer(config) -> WordTokenizer:
    """

    """
    factory = WordTokenizerFactory(config)
    return factory.get_word_tokenizer()
