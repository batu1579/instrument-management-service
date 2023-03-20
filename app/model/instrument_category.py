from typing import Optional

from pydantic import Field, HttpUrl

from app.model.response import Success
from app.model.base import DataModel, InCreateModel, InUpdateModel
from app.util.regex_pattern import NAME_PATTERN
from app.util.string_length import SHORT_LENGTH, LONG_LENGTH, URL_LENGTH


class _BaseInstrumentCategory(DataModel):
    category_name: str = Field(
        ...,
        regex=NAME_PATTERN,
        max_length=SHORT_LENGTH,
        title="器械分类名称",
        description="用来区分器械类别，只能使用中文、大小写字母、数字、下划线、中划线，默认为 Unnamed Category",
    )
    category_comment: Optional[str] = Field(
        None,
        max_length=LONG_LENGTH,
        title="器械分类备注",
        example="A Category Comment",
    )
    category_image_url: Optional[HttpUrl] = Field(
        None,
        max_length=URL_LENGTH,
        title="器械分类图片的 URL",
        example="https://example.com/image.png",
    )
    expire_duration_MS: Optional[int] = Field(
        None,
        gt=60000,
        title="过期时长",
        description="""
        记录此分类的器械经过多久会过期，单位为毫秒。最小值为 60 * 1000 （一分钟），设置为空则表示永不过期。
        默认为永不过期（ None ），可以在设置中修改。
        """,
    )


class InstrumentCategory(_BaseInstrumentCategory):
    pass


class InstrumentCategoryInCreate(InCreateModel, _BaseInstrumentCategory):
    pass


class InstrumentCategoryInUpdate(InUpdateModel, _BaseInstrumentCategory):
    category_name: Optional[str] = Field(
        None,
        regex=NAME_PATTERN,
        max_length=SHORT_LENGTH,
        title="器械分类名称",
        description="用来区分器械类别，只能使用中文、大小写字母、数字、下划线、中划线，默认为 Unnamed Category",
    )


class InstrumentCategoryInResponse(Success):
    data: list[InstrumentCategory]
