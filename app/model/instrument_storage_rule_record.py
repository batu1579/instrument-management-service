from typing import Optional

from pydantic import Field

from app.model.response import Success
from app.model.base import DataModel, InCreateModel, InUpdateModel
from app.util.type.guid import GUID
from app.database.table.instrument_storage_rule_record import StorageLocationType


class _BaseStorageRuleRecord(DataModel):
    storage_rule: GUID = Field(
        ...,
        title="所属的存储规则",
    )
    storage_location_type: StorageLocationType = Field(
        ...,
        title="存储位置类型",
        description="""
        可选的存储位置类型有：
        
            - ROOM      (0): 房间类型
            - CABINET   (1): 存储柜类型
            
        新建立的规则记录默认为房间类型（ ROOM ），可以在设置中修改。""",
    )
    storage_location: GUID = Field(
        ...,
        title="规则涉及到的存储存储",
    )
    instrument_catrgory: GUID = Field(
        ...,
        title="规则涉及到的器械类别",
    )


class StorageRuleRecord(_BaseStorageRuleRecord):
    pass


class StorageRuleRecordInCreate(InCreateModel, _BaseStorageRuleRecord):
    storage_location_type: Optional[StorageLocationType] = Field(
        StorageLocationType.ROOM,
        title="存储位置类型",
        description="""
        可选的存储位置类型有：
        
            - ROOM      (0): 房间类型
            - CABINET   (1): 存储柜类型
            
        新建立的规则记录默认为房间类型（ ROOM ），可以在设置中修改。""",
    )


class StorageRuleRecordInUpdate(InUpdateModel):
    storage_rule: Optional[GUID] = Field(
        None,
        title="所属的存储规则",
    )
    storage_location_type: Optional[StorageLocationType] = Field(
        None,
        title="存储位置类型",
        description="""
        可选的存储位置类型有：
        
            - ROOM      (0): 房间类型
            - CABINET   (1): 存储柜类型
            
        新建立的规则记录默认为房间类型（ ROOM ），可以在设置中修改。""",
    )
    storage_location: Optional[GUID] = Field(
        None,
        title="规则涉及到的存储存储",
    )
    instrument_catrgory: Optional[GUID] = Field(
        None,
        title="规则涉及到的器械类别",
    )


class StorageRuleRecordInResponse(Success):
    data: list[StorageRuleRecord]
