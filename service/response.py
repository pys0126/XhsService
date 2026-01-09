from starlette import status
from typing import Any, Optional
from fastapi.responses import ORJSONResponse
from fastapi.encoders import jsonable_encoder

# 状态码
SUCCESS: tuple[int, str] = (2000, "SUCCESS！")
FAIL: tuple[int, str] = (4000, "FAIL！")
NOT_FOUND: tuple[int, str] = (4040, "NOT_FOUND！")
SERVER_ERROR: tuple[int, str] = (5000, "服务异常，请稍后再试！")
MISSING_PARAM: tuple[int, str] = (4001, "缺少必填参数！")
PARAM_ERROR: tuple[int, str] = (4002, "参数格式错误！")



class ResponseUtil:
    """
    返回Response类
    """
    def __init__(self, code: int, message: str, data: Optional[Any] = None):
        """
        构造方法
        :param code: 状态码
        :param data: 返回数据
        :param message: 返回信息
        """
        self.code: int = code
        self.data: Optional[Any] = data
        self.message: str = message

    def success(self) -> ORJSONResponse:
        """
        成功Response
        :return: Response对象
        """
        response: dict = dict(code=self.code, data=self.data, message=self.message)
        return ORJSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response))

    def fail(self) -> ORJSONResponse:
        """
        失败Response
        :return: Response对象
        """
        response: dict = dict(code=self.code, data=self.data, message=self.message)
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(response))