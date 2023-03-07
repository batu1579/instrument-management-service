from typing import Optional

from pydantic import Field

from app.model.response import Success
from app.model.base import BaseModel, DataModel, InDBModel
from app.util.string_length import SHORT_LENGTH, LONG_LENGTH
from app.database.table.setting import SettingValueType


class _BaseSetting(DataModel):
    value_type: SettingValueType
    setting_key: str = Field(max_length=SHORT_LENGTH)
    setting_value: Optional[str] = Field(None, max_length=LONG_LENGTH)
    setting_comment: Optional[str] = Field(None, max_length=LONG_LENGTH)


class Setting(_BaseSetting):
    pass


class SettingInDB(InDBModel, _BaseSetting):
    pass


class SettingInCreate(_BaseSetting):
    pass


class SettingInUpdate(BaseModel):
    setting_value: Optional[str] = Field(None, max_length=LONG_LENGTH)


class SettingInResponse(Success):
    data: Setting


class SettingListInResponse(Success):
    data: list[Setting]
