<h1 align="center">Welcome to instrument-management-service 👋</h1>

> 为爬虫项目提供登录好的浏览器上下文

## 🎉 特性

- 使用 Fast API 构建 Restful 风格的 API 。
- 使用 Pydantic 校验数据
- 使用 SQLAlchemy 进行 ORM

## 🏠 克隆仓库

> 使用 SSH 地址克隆仓库，可以实现免密操作。具体配置方法见 [Gitlab 密钥配置说明] 。
> 文档中所有以 `<>` 包围的内容都需要替换为相应的值。

```bash
# 使用 SSH 克隆
git clone git@github.com:batu1579/instrument-management-service.git

# 使用 HTTPS 克隆
git clone https://github.com/batu1579/instrument-management-service.git
```

克隆完成后需要设置项目级别的用户信息

```bash
# 进入项目目录
cd ./instrument-management-service

# 设置和 gitlab 上相同的用户名和 Email
git config --local user.name "username"
git config --local user.email "email@example.com"
```

## 🐋 安装依赖

> 推荐使用 pipenv 新建一个虚拟环境来管理 pip 包，防止依赖冲突。具体使用方法见 [Pipenv 使用说明] 。

```bash
# 使用 pipenv 安装依赖并创建虚拟环境
# 安装完成后需要在 VS Code 中选择虚拟环境
pipenv install
pipenv install --dev

# 使用 pip 直接在本地环境安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## ⚙️ 环境变量

> 请将敏感数据存放在根目录的 `.env` 文件中（需要手动创建）

用到的环境变量参见 [环境配置示例]

## ⚠️ 注意事项

- 请不要使用 uvicorn 的 `reload` 参数，可能会导致日志分文件时出现错误
- 如果 VS Code 终端自动启动虚拟环境显示不能执行脚本，可以使用如下指令修改设置：

    ```bash
    # 需要以管理员权限启动 PowerShell
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```

- 如果在碰到类型检查误报，在保证代码可运行的前提下可以在行尾添加注释暂时禁用类型检查：

    ```python
    with self._session_factory() as session:  # type: ignore
        yield session
    ```

- 在调试前需要在打开了虚拟环境的终端中使用指令启动一个 pysnowflake 服务，用来生成数据库所需的 ID ，指令的具体使用方法见 [pysnowflake 官方文档] ：

    ```shell
    snowflake_start_server [--port=PORT]
    ```

    > 请保证指定的端口与 `.env` 文件中 `ID_SERVICE_PORT` 的值一致

- 默认的调试信息将显示在调试控制台中，如果没有显示可以使用 `Ctrl + Shift + Y` 快捷键打开，也可以手动修改为使用内置终端显示：

    1. 打开项目目录下的 `.vscode/launch.json` 文件
    2. 修改其中 `console` 的值为 `integratedTerminal` 即可

## 🧩 所需插件

- [Python] 提供 Python 提示和类型检查。
- [git-commit-plugin] 用于生成 Commit 。

## 📋 更新日志

查看 [更新日志]

## 📄 相关文档

- [Git 简单使用说明]
- [Gitlab 工作流程]
- [Fast API 官方文档]
- [Pydantic 官方文档]
- [SQLAlchemy 官方文档]

<!-- Links -->

[环境配置示例]: ./.env.example
[更新日志]: ./CHANGELOG.md

[Pipenv 使用说明]: ./docs/pipenv-useages.md
[Gitlab 密钥配置说明]: ./docs/gitlab-key-generate.md
[Git 简单使用说明]: ./docs/git-useages.md
[Gitlab 工作流程]: ./docs/gitlab-workflow.md

[Python]: https://marketplace.visualstudio.com/items?itemName=ms-python.python
[git-commit-plugin]: https://marketplace.visualstudio.com/items?itemName=redjue.git-commit-plugin

[Fast API 官方文档]: https://fastapi.tiangolo.com/zh/
[Pydantic 官方文档]: https://pydantic-docs.helpmanual.io/
[SQLAlchemy 官方文档]: https://docs.sqlalchemy.org/en/14/
[pysnowflake 官方文档]: https://pysnowflake.readthedocs.io/en/latest/
