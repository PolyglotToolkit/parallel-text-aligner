from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Callable, List, Literal, Optional, Tuple

import numpy as np
import pandas as pd

from parallel_text_aligner.data.structures.bitext import Bitext


@dataclass
class BeamOp:
    def simple(i: int, j: int) -> List[Tuple[int, int]]:
        return (i + 1, j + 1)

    def concat_row(i: int, j: int) -> List[Tuple[int, int]]:
        return (i + 1, j)

    def concat_col(i: int, j: int) -> List[Tuple[int, int]]:
        return (i, j + 1)

    def skip_row(i: int, j: int) -> List[Tuple[int, int]]:
        return (i + 2, j + 1)

    def skip_col(i: int, j: int) -> List[Tuple[int, int]]:
        return (i + 1, j + 2)

    def skip_row_concat_col(i: int, j: int) -> List[Tuple[int, int]]:
        return (i + 2, j)

    def skip_col_concat_row(i: int, j: int) -> List[Tuple[int, int]]:
        return (i, j + 2)

    def transpose_row(
        i: int, j: int
    ) -> List[
        Tuple[int, int]
    ]:  # need logic to ensure that this is only allowed following a skipped row?
        return (i - 1, j)

    def transpose_col(
        i: int, j: int
    ) -> List[
        Tuple[int, int]
    ]:  # need logic to ensure that this is only allowed following a skipped column?
        return (i, j - 1)


class Grid:
    """
    Class to hold information regarding the Cartesian product of two tokenized
      texts. Handles most of the relatively low-level operations related to
      subgrids (grid defined by two anchor points)
    """

    def __init__(self, length1: int, length2: int, mask_type: Literal["fat", "thin"] = "thin", padding: Optional[int] = None) -> None:
        self.length1 = length1
        self.length2 = length2
        self.mask = self.get_fat_mask(padding=padding) if mask_type == "fat" else self.get_thin_mask(padding=padding)
        self.grid = np.zeros((self.length1, self.length2), dtype="float")

    def get_fat_mask(self, padding: Optional[int] = 3) -> np.ndarray:
        """
        
        """
        rows, cols = self.length1, self.length2
        mask = np.zeros((rows, cols), dtype="int")

        if padding is None:
            padding = ...  # logarithmic?
        diff = rows - cols
        tall_surplus = diff * (rows > cols)
        wide_surplus = diff * (rows < cols)

        if tall_surplus:
            for i, j in product(range(rows), range(cols)):
                mask[i, j] = int((i - padding) < j < (i + tall_surplus + padding))
                    
        else:
            for i, j in product(range(rows), range(cols)):
                mask[i, j] = int((j - padding) < i < (j + tall_surplus + padding))

        return mask
    '''
        def condition(i: int, j: int) -> bool:
            return abs(j - i) <= padding

        for i, j in filter(
            lambda pair: condition(*pair), product(range(rows), range(cols))
        ):
            mask[i, j] = 1
            mask[
                min(rows - 1, i + tall_correction), min(cols - 1, j + wide_correction)
            ] = 1

        return mask
    '''
    def get_thin_mask(self, padding: Optional[int] = 3) -> np.ndarray:
        """
        
        """
        rows, cols = self.length1, self.length2
        mask = np.zeros((rows, cols), dtype="int")
        ratio = rows / cols

        if padding is None:
            padding = ...  # logarithmic?

        pairs_by_col = list(
            map(
                lambda j: (min(range(rows), key=lambda i: abs(j * ratio - i)), j),
                range(cols),
            )
        )
        pairs_by_row = list(
            map(
                lambda i: (i, min(range(cols), key=lambda j: abs(i / ratio - j))),
                range(rows),
            )
        )
        for i, j in pairs_by_col + pairs_by_row:
            mask[i, j] = 1
        for k in range(1, padding):
            mask[k:] += mask[:-k]
            mask[:, k:] += mask[:, :-k]
        return np.minimum(mask, 1)

    # def beam_simple(self, current_indices: Tuple[int, int]) -> Callable[[Bitext], Tuple[str]]:
    #     ...


# g = Grid(10, 13)
# m = g.get_fat_mask()
# m2 = g.get_thin_mask()
# print(m)
# print(m2)
