from typing import Optional

from pathlib import Path

from uvicorn import run as uvicorn_run

from typer import Typer, Option

from pydantic import validate_arguments

from app.util.env import SETTINGS

app = Typer(help="Instrument management service")


@app.command()
@validate_arguments
def run(
    host: str = Option("localhost", help="启动服务的主机名"),
    port: int = Option(8081, help="启动服务的端口"),
    env_file: Optional[Path] = Option(None, help="手动指定环境变量文件位置"),
):
    """启动服务"""
    if env_file is not None:
        SETTINGS.set_env_files_path(env_file)

    keyfile_path = SETTINGS.service.keyfile_path
    if keyfile_path is not None:
        keyfile_path = keyfile_path.as_posix()

    certfile_path = SETTINGS.service.certfile_path
    if certfile_path is not None:
        certfile_path = certfile_path.as_posix()

    uvicorn_run(
        app="app.main:app",
        host=host if host else SETTINGS.service.host,
        port=port if port else SETTINGS.service.port,
        ssl_keyfile=keyfile_path,
        ssl_certfile=certfile_path,
    )


@app.command()
@validate_arguments
def test():
    """运行服务测试"""
    print("Start testing...")


if __name__ == "__main__":
    app()
