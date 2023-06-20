from pathlib import Path
from typing import List, Tuple, Union


class Text:
    def __init__(self, text_path: Path, pretokenized: bool = False) -> None:
        self.raw = ...
        self.sentences_orig = ...
        self._sentences: List[str] = ...
        self.current2orig: List[
            Tuple[int, int]
        ] = ...  # mappings from current tokenization to original tokenization

    def __getitem__(self, __index: int) -> str:
        return self._sentences[__index]

    def split_sentence_by_pos(self, sentence_index: int, split_position: int) -> None:
        ...


class Bitext:
    def __init__(self, path1: Path, path2: Path, pretokenized: bool = False) -> None:
        self.text1 = Text(path1, pretokenized=pretokenized)
        self.text2 = Text(path2, pretokenized=pretokenized)

    def __getitem__(self, __key: Union[Tuple[int, int], int]) -> Tuple[str, str]:
        i, j = (__key, __key) if isinstance(__key, tuple) else __key
        return (self.text1[i], self.text2[j])
