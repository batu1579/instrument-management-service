from typing import Optional

from datetime import datetime

from pydantic import Field

from app.util.type.guid import GUID
from app.model.response import Success
from app.model.base import DataModel, InCreateModel


class _BaseInstrumentRecord(DataModel):
    located_cabinet: GUID = Field(..., title="存放器械的存储柜")
    instrument_category: GUID = Field(..., title="器械类别")
    expire_time: Optional[datetime] = Field(
        None,
        title="过期时间",
        description="用于记录器械消毒过期的时间，创建时不需主动设置。",
    )


class InstrumentRecord(_BaseInstrumentRecord):
    pass


class InstrumentRecordInCreate(InCreateModel, _BaseInstrumentRecord):
    pass


class InstrumentRecordInResponse(Success):
    data: list[InstrumentRecord]
