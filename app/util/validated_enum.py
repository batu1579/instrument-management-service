from typing import TypeVar, Type, Any

from enum import Enum as _StandardEnum

from app.model.validator import ValidatedValue

_EnumT = TypeVar("_EnumT", bound="ValidatedEnum")


class ValidatedEnum(ValidatedValue[_EnumT], _StandardEnum):
    @classmethod
    def __validator__(cls: Type[_EnumT], value: Any) -> _EnumT | None:
        if isinstance(value, int):
            if value in [i.value for i in cls]:
                return cls(value)
            raise ValueError(f"{value} is not a valid {cls.__name__} value.")
        if isinstance(value, str):
            if value in cls.__members__:
                return cls[value]
            raise ValueError(f"{value} is not a valid key of {cls.__name__}")
        return None

    @classmethod
    def __modify_schema__(cls: Type[_EnumT], field_schema: dict[str, Any]) -> None:
        keys, [example_item, *_] = zip(*cls.__members__.items())
        field_schema.update(
            {
                "type": "string",
                "examples": [
                    example_item.name,
                    example_item.value,
                ]
                if isinstance(example_item, cls)
                else [],
                "enum": keys,
            }
        )
