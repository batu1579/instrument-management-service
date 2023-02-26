from fastapi import HTTPException, status


def resource_not_found(resource_name: str) -> HTTPException:
    """生成资源不存在异常对象

    Args:
        resource_name (str): 未找到的资源名称

    Returns:
        HTTPException: 生成的 HTTP 异常对象
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"{resource_name} not found."
    )


def resource_exists(resource_name: str) -> HTTPException:
    """生成资源已存在异常对象

    Args:
        resource_name (str): 已存在的资源名称

    Returns:
        HTTPException: 生成的 HTTP 异常对象
    """
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail=f"{resource_name} already exists."
    )


def field_invalid(arg_name: str, except_info: str) -> HTTPException:
    """生成请求参数不合法异常对象

    Args:
        arg_name (str): 错误参数名称
        except_info (str): 期望的参数信息（提示信息）

    Returns:
        HTTPException: 生成的 HTTP 异常对象
    """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Arguments {arg_name} is invalid. {except_info}",
    )
