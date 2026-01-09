from service.utils import sign, refresh_cookie, format_json_dict, read_cookie
from curl_cffi import requests, Response
from typing import Optional
from fastapi import Query
import json


class XhsLogic:
    def __init__(self, proxy: str = None, cookies_path: str = "cookies.json") -> None:
        """
        XHS接口封装
        :param proxy: 代理，示例：http://127.0.0.1:7897
        :param cookies_path: Cookie文件路径
        """
        self.proxy: str = proxy
        self.cookies_path: str = cookies_path
        self.cookies: dict = read_cookie(path=cookies_path) or refresh_cookie(cookies_path=cookies_path,
                                                                              proxy=self.proxy)
        self.base_host: str = "https://edith.xiaohongshu.com"

    def _request(self, method: str, uri: str, params: dict = None, data: dict = None, cookies: dict = None,
                 proxy: str = None) -> dict:
        """
        内部请求封装
        :param method: 请求方法GET或POST
        :param uri: 请求接口
        :param params: GET查询参数
        :param data: POST JSON参数
        :param cookies: 自定义cookie，为空则使用内置cookie
        :param proxy: 代理，示例：http://127.0.0.1:7897
        :return: 返回JSON字典
        """
        if method.upper() == "GET":
            sign_header: dict = sign(cookies=cookies or self.cookies, uri=uri, params=params, method=method)
            url: str = self.base_host + uri + "?" + "&".join([f"{k}={v}" for k, v in params.items()])
            response: Response = requests.get(url, headers=sign_header, cookies=cookies or self.cookies, verify=False,
                                              quote=False, proxy=proxy)
        elif method.upper() == "POST":
            sign_header: dict = sign(cookies=cookies or self.cookies, uri=uri, method=method, data=data)
            sign_header.update({"Content-Type": "application/json"})
            response: Response = requests.post(url=self.base_host + uri,
                                               data=json.dumps(data, separators=(",", ":"), ensure_ascii=False),
                                               headers=sign_header, cookies=cookies or self.cookies, proxy=proxy)
        else:
            raise RuntimeError("请求方法错误！")
        return response.json()

    def set_web_session(self) -> None:
        """
        请求设置web_session到cookie
        :return:
        """
        uri: str = "/api/sns/web/v1/login/activate"
        self._request(method="POST", uri=uri, data={})
        # 写入cookies.json
        with open(self.cookies_path, "w", encoding="utf-8") as f:
            f.write(format_json_dict(self.cookies))

    def send_phone_code(self, phone: str) -> dict:
        """
        发送手机验证码
        :param phone: 手机号
        :return:
        """
        uri: str = "/api/sns/web/v2/login/send_code"
        params: dict = {"phone": phone, "zone": "86", "type": "login"}
        result_json: dict = self._request(method="GET", uri=uri, params=params)
        if not result_json.get("success"):
            raise RuntimeError(format_json_dict(result_json))
        return result_json

    def phone_login(self, phone: str, code: str) -> dict:
        """
        手机号登录（会写入cookies.json）
        :param phone: 手机号
        :param code: 验证码
        :return:
        """
        # 检查验证码
        uri: str = "/api/sns/web/v1/login/check_code"
        params: dict = {"phone": phone, "zone": "86", "code": code}
        result_json: dict = self._request(method="GET", uri=uri, params=params)
        if not result_json.get("success"):
            raise RuntimeError(format_json_dict(result_json))
        # 登录
        mobile_token: str = result_json.get("data", {}).get("mobile_token", "")
        uri = "/api/sns/web/v1/login/code"
        data: dict = {"mobile_token": mobile_token, "zone": "86", "phone": phone}
        result_json: dict = self._request(method="POST", uri=uri, data=data)
        # 写入cookies.json
        with open(self.cookies_path, "w", encoding="utf-8") as f:
            f.write(format_json_dict(self.cookies))
        return result_json

    def get_user_notes(self, user_id: str, xsec_token: str, xsec_source: str = "pc_note", cursor: str = "") -> dict:
        """
        获取用户笔记列表
        :param user_id: 用户ID
        :param xsec_token: xsec_token
        :param xsec_source: xsec_source
        :param cursor: 游标，首页为""
        :return:
        """
        uri: str = "/api/sns/web/v1/user_posted"
        params: dict = {
            "num": "30",
            "cursor": cursor,
            "user_id": user_id,
            "image_formats": "jpg,webp,avif",
            "xsec_token": xsec_token,
            "xsec_source": xsec_source
        }
        result_json: dict = self._request(method="GET", uri=uri, params=params)
        return result_json.get("data", {})

    def get_note_by_id(self, note_id: str, xsec_token: str, xsec_source: str = "pc_user") -> dict:
        """
        获取笔记详情
        :param note_id: 笔记ID
        :param xsec_token: xsec_token
        :param xsec_source: xsec_source
        :return:
        """
        data: dict = {
            "source_note_id": note_id,
            "image_formats": [
                "jpg",
                "webp",
                "avif"
            ],
            "extra": {
                "need_body_topic": "1"
            },
            "xsec_source": xsec_source,
            "xsec_token": xsec_token
        }
        result_json: dict = self._request(uri="/api/sns/web/v1/feed", data=data, method="POST")
        return result_json

    def get_comment_list(self, note_id: str, xsec_token: str, cursor: str = "") -> dict:
        """
        获取评论列表
        :param note_id: 笔记ID
        :param xsec_token: xsec_token
        :param cursor: 游标，首页为""
        :return:
        """
        uri: str = "/api/sns/web/v2/comment/page"
        params: dict = {
            "note_id": note_id,
            "cursor": cursor,
            "top_comment_id": "",
            "image_formats": "jpg,webp,avif",
            "xsec_token": xsec_token
        }
        result_json: dict = self._request(method="GET", uri=uri, params=params)
        return result_json.get("data", {})

    def get_sub_comment_list(self, note_id: str, comment_id: str, xsec_token: str, cursor: str = "") -> dict:
        """
        获取子评论列表
        :param note_id: 笔记ID
        :param comment_id: 评论ID
        :param xsec_token: xsec_token
        :param cursor: 游标，首页为""
        :return:
        """
        uri: str = "/api/sns/web/v2/comment/sub/page"
        params: dict = {
            "note_id": note_id,
            "root_comment_id": comment_id,
            "num": "10",
            "cursor": cursor,
            "image_formats": "jpg,webp,avif",
            "top_comment_id": "",
            "xsec_token": xsec_token
        }
        result_json: dict = self._request(method="GET", uri=uri, params=params)
        return result_json.get("data", {})


def get_xhs_logic(proxy: Optional[str] = Query(default=None,
                                               description="代理，示例：http://127.0.0.1:7897")) -> XhsLogic:
    """
    获取XhsLogic对象
    :param proxy: GET请求中的proxy参数
    :return:
    """
    return XhsLogic(proxy=proxy)
