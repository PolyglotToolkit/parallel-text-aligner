from typing import Iterable, Protocol

import numpy as np


class ModelProto(Protocol):
    """ """

    def __call__(self, input_array: Iterable[np.array]) -> float:
        ...

    def get_params(self) -> np.array:
        ...

    def read_params(self) -> None:
        ...

    def save_params(self) -> None:
        ...


class ParamsProto(Protocol):
    ...
