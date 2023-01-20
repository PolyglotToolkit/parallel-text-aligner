from pathlib import Path

from parallel_text_aligner.tokenization.sentence.sentence_tokenizer import (
    SentenceTokenizer,
    get_sentence_tokenizer,
)
from parallel_text_aligner.tokenization.word.word_tokenizer import (
    WordTokenizer,
    get_word_tokenizer,
)


class DataHandler:
    """ """

    def __init__(
        self,
        data_dir,
        sentence_tokenizer: SentenceTokenizer,
        word_tokenizer: WordTokenizer,
    ) -> None:
        ...

    def load() -> None:
        ...


class DataHandlerFactory:
    """ """

    def __init__(self, config) -> None:
        ...

    def get_data_handler(self) -> DataHandler:
        data_dir = Path("")
        sentence_tokenizer = get_sentence_tokenizer(self.config)
        word_tokenizer = get_word_tokenizer(self.config)
        ...
        return DataHandler(data_dir, sentence_tokenizer, word_tokenizer)


def get_data_handler(config) -> DataHandler:
    """ """
    factory = DataHandlerFactory(config)
    return factory.get_data_handler()
