from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from starlette.exceptions import HTTPException
from starlette.datastructures import CommaSeparatedStrings
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from app.api import root_router
from app.database import DB
from app.exception import handler
from app.util import env
from app.util.log import LOG
from app.util.guid import init_snowflake_client

app = FastAPI(
    title=env.TITLE,
    version="0.1.0",
    docs_url=env.DOCS_URL,
    redoc_url=env.REDOCS_URL,
)

# 注册中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=CommaSeparatedStrings(env.ORIGINS),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=env.GZIP_MIN_SIZE)

if env.USE_HTTPS_ONLY:
    app.add_middleware(HTTPSRedirectMiddleware)

# 注册事件

# 启动事件
app.add_event_handler("startup", LOG.start_logging)
app.add_event_handler("startup", DB.connect_database)
app.add_event_handler("startup", init_snowflake_client)
# 结束事件
app.add_event_handler("shutdown", DB.disconnect_database)
app.add_event_handler("shutdown", LOG.stop_logging)

# 注册异常处理
app.add_exception_handler(RequestValidationError, handler.invalid_param_handler)
app.add_exception_handler(HTTPException, handler.http_exception_handler)
app.add_exception_handler(Exception, handler.other_exception_handler)

# 注册路由
app.include_router(router=root_router)
