from typing import Optional, TypeAlias

from pydantic import Field, validator

from app.model.response import Success
from app.model.base import DataModel, InCreateModel, InUpdateModel
from app.database.table.setting import SettingValueType
from app.util.string_length import SHORT_LENGTH, LONG_LENGTH

ParsedValue: TypeAlias = str | int | float | bool


class _BaseSetting(DataModel):
    value_type: SettingValueType = Field(
        ...,
        title="设置项数据的类型",
        description="""
        用来规定设置项数据的类型，目前可选的类型有：

            - STRING    (0): 字符串
            - INTEGER   (1): 整数
            - FLOAT     (2): 浮点数
            - BOOLEAN   (3): 布尔值

        默认为字符串（ STRING ）类型，可以在设置中修改。
        其他类型数值（例如数组）请使用字符串类型并编写对应的解析和校验方法。""",
    )
    setting_key: str = Field(
        ...,
        max_length=SHORT_LENGTH,
        regex=r"^[0-9A-Z_]*$",
        title="设置项键名",
        description="所有设置项键名都只能由数字，大写字母和下划线组成",
        example="EXAMPLE_SETTING_KEY",
    )
    setting_value: str = Field(
        ...,
        max_length=LONG_LENGTH,
        title="设置项值",
        description="设置项的值，必须与 value_type 字段对应，如果不能直接强制转换则会抛出一个 ValueError 异常。",
        example="EXAMPLE_SETTING_VALUE",
    )
    value: Optional[ParsedValue] = Field(
        None,
        title="解析后的设置项值",
        description="辅助字段，用于记录转换类型后的设置项值。创建时不需包含此字段，序列化时也不会包含此字段。",
        exclude=True,
    )
    setting_comment: Optional[str] = Field(
        None,
        max_length=LONG_LENGTH,
        title="设置项备注",
        example="A setting comment",
    )

    @validator("value", always=True)
    def check_value(cls, _: str, values: dict) -> ParsedValue:
        """校验设置值

        Args:
            values (dict): 全部字段

        Raises:
            ValueError: 当类型与值不匹配时抛出异常

        Returns:
            ParsedValue: 转换类型后的设置值
        """
        value_type: SettingValueType | None = values.get("value_type")
        raw_value: str | None = values.get("setting_value")

        assert value_type is not None, "value_type is required"
        assert raw_value is not None, "setting_value is required"

        try:
            if value_type == SettingValueType.INTEGER:
                return int(raw_value)
            if value_type == SettingValueType.FLOAT:
                return float(raw_value)
            if value_type == SettingValueType.BOOLEAN:
                if raw_value.lower() == "true":
                    return True
                if raw_value.lower() == "false":
                    return False
                raise ValueError
            return raw_value  # 默认类型不需要转换
        except ValueError as err:
            raise ValueError(
                f"Setting value doesn't match the type: {value_type}"
            ) from err


class Setting(_BaseSetting):
    pass


class SettingInCreate(InCreateModel, _BaseSetting):
    value_type: Optional[SettingValueType] = Field(
        SettingValueType.STRING,
        title="设置项数据的类型",
        description="""
        用来规定设置项数据的类型，目前可选的类型有：

            - STRING    (0): 字符串
            - INTEGER   (1): 整数
            - FLOAT     (2): 浮点数
            - BOOLEAN   (3): 布尔值

        默认为字符串（ STRING ）类型，可以在设置中修改。
        其他类型数值（例如数组）请使用字符串类型并编写对应的解析和校验方法。""",
    )


class SettingInUpdate(InUpdateModel):
    setting_value: str = Field(
        ...,
        max_length=LONG_LENGTH,
        title="设置项值",
        description="设置项的值，必须与 value_type 字段对应，如果不能直接强制转换则会抛出一个 ValueError 异常。",
        example="EXAMPLE_SETTING_VALUE",
    )


class SettingInResponse(Success):
    data: list[Setting]
