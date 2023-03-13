from typing import Callable, TypeVar, Generator
from typing_extensions import Protocol

V, T = TypeVar("V"), TypeVar("T")
Validator = Generator[
    Callable[
        [
            V,
        ],
        T,
    ],
    None,
    None,
]


class Validated(Protocol):
    @classmethod
    def __get_validators__(
        cls,
    ) -> Validator[V, T]:
        ...
