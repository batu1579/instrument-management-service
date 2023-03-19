from typing import Optional

from pydantic import Field

from app.model.response import Success
from app.model.base import DataModel, InCreateModel, InUpdateModel
from app.util.regex_pattern import NAME_PATTERN
from app.util.string_length import SHORT_LENGTH, LONG_LENGTH
from app.database.table.instrument_storage_rule import RuleStatus, RuleType


class _BaseStorageRule(DataModel):
    rule_name: str = Field(
        ...,
        max_length=SHORT_LENGTH,
        regex=NAME_PATTERN,
        title="存储规则名称",
        description="用来区分存储规则，只能使用中文、大小写字母、数字、下划线、中划线，默认为 Unnamed Storage Rule",
    )
    rule_status: RuleStatus = Field(
        ...,
        title="存储规则状态",
        description="""
        用来控制存储规则是否生效，可选择状态有：
        
            - DISABLED   (0): 禁用规则
            - ENABLED    (1): 启用规则
            
        默认新建立的存储规则为启用（ ENABLED ），可以在设置中修改。
        """,
    )
    rule_type: RuleType = Field(
        ...,
        title="存储规则类型",
        description="""
        用来设置存储规则类型，可选的存储规则类型有：
        
            - ALL_FORBID   (0): 禁止任何存储
            - BLACK_LIST   (1): 黑名单规则（只有指定位置不能存放）
            - WHITE_LIST   (2): 白名单规则（除了指定位置其他地方不能存放）
            
        默认新建立的存储规则类型为禁止任何存储（ ALL_FORBID ），可以在设置中修改。
        """,
    )
    rule_comment: Optional[str] = Field(
        None,
        max_length=LONG_LENGTH,
        title="存储规则备注",
        example="A rule comment",
    )


class StorageRule(_BaseStorageRule):
    pass


class StorageRuleInCreate(InCreateModel, _BaseStorageRule):
    rule_name: str = Field(
        "Unnamed Storage Rule",
        max_length=SHORT_LENGTH,
        regex=NAME_PATTERN,
        title="存储规则名称",
        description="用来区分存储规则，只能使用中文、大小写字母、数字、下划线、中划线，默认为 Unnamed Storage Rule",
    )
    rule_status: RuleStatus = Field(
        RuleStatus.DISABLED,
        title="存储规则状态",
        description="""
        用来控制存储规则是否生效，可选择状态有：
        
            - DISABLED   (0): 禁用规则
            - ENABLED    (1): 启用规则
            
        默认新建立的存储规则为禁用（ DISABLED ），可以在设置中修改。
        """,
    )
    rule_type: RuleType = Field(
        RuleType.ALL_FORBID,
        title="存储规则类型",
        description="""
        用来设置存储规则类型，可选的存储规则类型有：
        
            - ALL_FORBID   (0): 禁止任何存储
            - BLACK_LIST   (1): 黑名单规则（只有指定位置不能存放）
            - WHITE_LIST   (2): 白名单规则（除了指定位置其他地方不能存放）
            
        默认新建立的存储规则类型为禁止任何存储（ ALL_FORBID ），可以在设置中修改。
        """,
    )


class StorageRuleInUpdate(InUpdateModel, _BaseStorageRule):
    rule_name: Optional[str] = Field(
        None,
        max_length=SHORT_LENGTH,
        regex=NAME_PATTERN,
        title="存储规则名称",
        description="用来区分存储规则，只能使用中文、大小写字母、数字、下划线、中划线，默认为 Unnamed Storage Rule",
    )
    rule_status: Optional[RuleStatus] = Field(
        None,
        title="存储规则状态",
        description="""
        用来控制存储规则是否生效，可选择状态有：
        
            - DISABLED   (0): 禁用规则
            - ENABLED    (1): 启用规则
            
        默认新建立的存储规则为禁用（ DISABLED ），可以在设置中修改。
        """,
    )
    rule_type: Optional[RuleType] = Field(
        None,
        title="存储规则类型",
        description="""
        用来设置存储规则类型，可选的存储规则类型有：
        
            - ALL_FORBID   (0): 禁止任何存储
            - BLACK_LIST   (1): 黑名单规则（只有指定位置不能存放）
            - WHITE_LIST   (2): 白名单规则（除了指定位置其他地方不能存放）
            
        默认新建立的存储规则类型为禁止任何存储（ ALL_FORBID ），可以在设置中修改。
        """,
    )


class StorageRuleInResponse(Success):
    data: list[StorageRule]
