from __future__ import annotations

from typing import (
    Any,
    Callable,
    Generic,
    Generator,
    Type,
    TypeVar,
    TypeAlias,
)

from abc import abstractmethod

_ValidatedT = TypeVar("_ValidatedT", bound="Validated")

ValueT = TypeVar("ValueT", bound="Any")
Validator: TypeAlias = Callable[[ValueT], _ValidatedT]
ValidatorGenerator: TypeAlias = Generator[Validator[Any, _ValidatedT], None, None]


class Validated(Generic[_ValidatedT]):
    @classmethod
    @abstractmethod
    def __get_validators__(
        cls: Type[_ValidatedT],
    ) -> ValidatorGenerator[_ValidatedT]:
        ...

    @classmethod
    @abstractmethod
    def __modify_schema__(cls: Type[_ValidatedT], field_schema: dict[str, Any]) -> None:
        ...


_ValidSelfT = TypeVar("_ValidSelfT", bound="ValidatedValue")


class ValidatedValue(Validated[_ValidSelfT]):
    """用来给 Pydantic 验证自定义类型的父类，继承了 Validated 接口

    Args:
        Validated (_ValidSelfT): 一个 TypeVar 需要绑定为继承的子类自身

    Raises:
        TypeError: 验证失败时抛出此异常
    """

    @classmethod
    @abstractmethod
    def __modify_schema__(cls: Type[_ValidatedT], field_schema: dict[str, Any]) -> None:
        ...

    @classmethod
    @abstractmethod
    def __validator__(cls: Type[_ValidSelfT], value: Any) -> _ValidSelfT | None:
        ...

    @classmethod
    def __validator_wrapper__(cls: Type[_ValidSelfT], value: Any) -> _ValidSelfT:
        if isinstance(value, cls):
            return value

        self_obj = cls.__validator__(value)

        if self_obj is not None:
            return self_obj

        raise TypeError(
            f"{type(value).__name__} can not be converted to {cls.__name__}"
        )

    @classmethod
    def __get_validators__(
        cls: Type[_ValidSelfT],
    ) -> ValidatorGenerator[_ValidSelfT]:
        yield cls.__validator_wrapper__
