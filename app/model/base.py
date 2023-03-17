from typing import Optional

from datetime import datetime, timezone

from pydantic import BaseConfig, Field
from pydantic import BaseModel as __BaseModel

from app.util.type.guid import GUID


class BaseModel(__BaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: (
                dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
            ),
            GUID: lambda guid: guid.to_string(),
        }


class DataModel(__BaseModel):
    id: GUID = Field(
        ...,
        title="记录 ID",
        description="数据库中的记录 ID ，也是表中的主键。使用雪花算法生成的全局唯一识别码，依赖于 pysnowflake 。",
    )
    created_at: Optional[datetime] = Field(
        ...,
        title="记录创建时间",
        description="数据库中的记录创建时间。",
    )
    updated_at: Optional[datetime] = Field(
        ...,
        title="记录更新时间",
        description="数据库中的记录最后的更新时间。",
    )

    class Config(BaseConfig):
        orm_mode = True
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: (
                dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
            ),
            GUID: lambda guid: guid.to_string(),
        }


class InCreateModel(__BaseModel):
    id: Optional[GUID | str] = Field(
        default_factory=GUID.generate,
        title="记录 ID",
        description="数据库中的记录 ID ，也是表中的主键。使用雪花算法生成的全局唯一识别码，依赖于 pysnowflake 。",
    )

    class Config(BaseConfig):
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: (
                dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
            ),
            GUID: lambda guid: guid.guid,
        }


class InUpdateModel(__BaseModel):
    def dict(self, *args, **kwargs) -> dict:
        kwargs.update({"exclude_unset": True})
        return super().dict(*args, **kwargs)

    class Config(BaseConfig):
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: (
                dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
            ),
            GUID: lambda guid: guid.guid,
        }
