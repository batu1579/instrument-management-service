from typing import Optional

from datetime import datetime, timezone

from pydantic import BaseConfig, Field
from pydantic import BaseModel as __BaseModel

from snowflake.client import get_guid


class BaseModel(__BaseModel):
    class Config(BaseConfig):
        json_encoders = {
            datetime: lambda dt: (
                dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
            )
        }


class DataBaseModel(BaseModel):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class SnowFlakeID(BaseModel):
    id: int = Field(default_factory=get_guid)
