from loguru import logger
from traceback import format_exc
from service.controller import router
from starlette.requests import Request
from fastapi_offline import FastAPIOffline
from service.response import FAIL, ResponseUtil

app: FastAPIOffline = FastAPIOffline(title="XHS采集API - UodRad")
app.include_router(prefix="", router=router)


async def low_exception_handler(request: Request, exception: Exception):
    """
    自定义异常处理器
    :param request: 请求对象
    :param exception: 异常类
    :return:
    """
    logger.error(format_exc())
    return ResponseUtil(*FAIL).fail()


# 全局异常处理
app.add_exception_handler(exc_class_or_status_code=Exception, handler=low_exception_handler)