from starlette.requests import Request
from starlette.responses import JSONResponse

from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError as RequestInvalid

from app.model.response import Error

# TODO(batu1579): 添加记录异常日志


async def invalid_param_handler(req: Request, exc: RequestInvalid) -> JSONResponse:
    """非法请求参数异常处理器

    Args:
        req (Request): 请求原文
        exc (RequestInvalid): 引发的异常对象

    Returns:
        JSONResponse: 响应数据
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            Error(
                **{
                    "code": 422,
                    "msg": "The request arguments are invalid.",
                    "info": {"detail": exc.errors(), "body": exc.body},
                }
            )
        ),
    )


async def http_exception_handler(req: Request, exc: HTTPException) -> JSONResponse:
    """HTTP 异常处理器

    Args:
        req (Request): 请求原文
        exc (HTTPException): 引发的异常对象

    Returns:
        JSONResponse: 响应数据
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            Error(
                **{
                    "code": exc.status_code,
                    "msg": exc.detail,
                    "info": "https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status",
                }
            )
        ),
    )


async def other_exception_handler(req: Request, exc: Exception) -> JSONResponse:
    """其他异常处理器

    Args:
        req (Request): 请求原文
        exc (Exception): 引发的异常对象

    Returns:
        JSONResponse: 响应数据
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            Error(
                **{
                    "code": 500,
                    "msg": "Unknown server exception",
                    "info": "Please contact administrator to report this error.",
                }
            )
        ),
    )
