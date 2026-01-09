from service.logic import XhsLogic, get_xhs_logic
from fastapi.responses import ORJSONResponse
from fastapi import Query, Depends, APIRouter
from service.response import ResponseUtil, SUCCESS


router: APIRouter = APIRouter(prefix="")


@router.get("/send_phone_code", summary="发送手机验证码")
def send_phone_code(phone: str, xhs_logic: XhsLogic = Depends(get_xhs_logic)) -> ORJSONResponse:
    return ResponseUtil(*SUCCESS, data=xhs_logic.send_phone_code(phone)).success()


@router.get("/phone_login", summary="手机号登录")
def phone_login(phone: str, code: str, xhs_logic: XhsLogic = Depends(get_xhs_logic)) -> ORJSONResponse:
    return ResponseUtil(*SUCCESS, data=xhs_logic.phone_login(phone, code)).success()


@router.get("/get_user_notes", summary="获取用户笔记列表",
            description="数据示例：{'cursor':'','has_more':false,notes:[]}")
def get_user_notes(user_id: str, xsec_token: str, xsec_source: str = Query(default="pc_note"),
                   cursor: str = Query(default="", description="游标，首页为''，后续用返回数据的cursor字段填充"),
                   xhs_logic: XhsLogic = Depends(get_xhs_logic)) -> ORJSONResponse:
    return ResponseUtil(*SUCCESS, data=xhs_logic.get_user_notes(user_id, xsec_token, xsec_source, cursor)).success()


@router.get("/get_note_by_id", summary="获取笔记详情")
def get_note_by_id(note_id: str, xsec_token: str, xsec_source: str = Query(default="pc_user"),
                   xhs_logic: XhsLogic = Depends(get_xhs_logic)) -> ORJSONResponse:
    return ResponseUtil(*SUCCESS, data=xhs_logic.get_note_by_id(note_id, xsec_token, xsec_source)).success()


@router.get("/get_comment_list", summary="获取评论列表",
            description="数据示例：{"
                        "'cursor':'',"
                        "'has_more':false,"
                        "'time':1767926762050,"
                        "'user_id':'6432b3eb000000001002a725',"
                        "'xsec_token':'ABTykFBOaHZH02_-StM7QSgOlQgI5vtdFrFUz4KUvhpJ0=',"
                        "comments:[]}")
def get_comment_list(note_id: str, xsec_token: str,
                     cursor: str = Query(default="", description="游标，首页为''，后续用返回数据的cursor字段填充"),
                     xhs_logic: XhsLogic = Depends(get_xhs_logic)) -> ORJSONResponse:
    return ResponseUtil(*SUCCESS, data=xhs_logic.get_comment_list(note_id, xsec_token, cursor)).success()


@router.get("/get_sub_comment_list", summary="获取子评论列表",
            description="数据示例：{"
                        "'cursor':'',"
                        "'has_more':false,"
                        "'time':1767926762050,"
                        "'user_id':'6432b3eb000000001002a725',"
                        "'xsec_token':'ABTykFBOaHZH02_-StM7QSgOlQgI5vtdFrFUz4KUvhpJ0=',"
                        "comments:[]}")
def get_sub_comment_list(note_id: str, comment_id: str, xsec_token: str,
                        cursor: str = Query(default="", description="游标，首页为''，后续用返回数据的cursor字段填充"),
                        xhs_logic: XhsLogic = Depends(get_xhs_logic)) -> ORJSONResponse:
    params: list = [note_id, comment_id, xsec_token, cursor]
    return ResponseUtil(*SUCCESS, data=xhs_logic.get_sub_comment_list(*params)).success()