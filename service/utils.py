from service.encryption import generate_headers, splice_str
from DrissionPage import Chromium, ChromiumOptions
from typing import Optional
from loguru import logger
import json
import os
import re


def format_json_dict(data: dict) -> str:
    """
    格式化JSON字典
    :param data: JSON字典
    :return: 格式化后的JSON字符串
    """
    return json.dumps(data, separators=(", ", ": "), ensure_ascii=False, indent=4)


def parse_cookie(cookies: list) -> dict:
    """
    将CookieList转为字典
    :param cookies: cookie字符串
    :return:
    """
    result: dict = {}
    for cookie in cookies:
        result[cookie["name"]] = cookie["value"]
    return result


def read_cookie(path: str = "cookies.json") -> Optional[dict]:
    """
    读取Cookie
    :param path: Cookie文件路径
    :return:
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            json_str: str = f.read()
    except FileNotFoundError:
        return None
    # 判断json_str是否为空
    if not json_str: return None
    return json.loads(json_str)


def refresh_cookie(proxy: str = None, cookies_path: str = "cookies.json", browser_path: str = None) -> dict:
    """
    使用无头浏览器获取新的Cookie（会替换cookies.json中的cookie）
    :param proxy: 代理，示例：http://127.0.0.1:7897
    :param cookies_path: cookies.json文件路径
    :param browser_path: 浏览器执行路径，为空则自动查找
    :return: cookie字典
    """
    options: ChromiumOptions = ChromiumOptions()
    options.set_browser_path(browser_path)
    options.headless(True)
    if proxy:
        logger.warning("【DrissionPage】注意已使用代理：{proxy}")
        options.set_proxy(proxy)
    logger.info("【DrissionPage】启动无头浏览器...")
    try:
        browse = Chromium(ChromiumOptions().set_browser_path(browser_path))
    except Exception:  # 找不到chrome，尝试使用brave-browser
        logger.warning("【DrissionPage】未找到Chrome浏览器，尝试使用Brave浏览器...")
        browse = Chromium(ChromiumOptions().set_browser_path("brave-browser"))
    tab = browse.latest_tab
    logger.info("【DrissionPage】访问小红书主页，获取Cookie...")
    tab.get("https://www.xiaohongshu.com")
    cookies: dict = parse_cookie(tab.cookies())
    logger.info(f"【DrissionPage】Cookie获取成功：{cookies}")
    with open(cookies_path, "w", encoding="utf-8") as f:
        f.write(format_json_dict(cookies))
        logger.info(f"【DrissionPage】Cookie已写入文件：{os.path.abspath(cookies_path)}")
    return cookies


def sign(uri: str, cookies: dict, data: dict = None, params: dict = None, method: str = "POST") -> dict:
    """
    参数签名
    :param uri: 请求路由
    :param data: 请求JSON（POST请求）
    :param params: 请求参数（GET请求）
    :param cookies: cookies字典
    :param method: 请求方式
    :return:
    """
    if method == "GET":
        headers, _ = generate_headers(a1=cookies.get("a1"), api=splice_str(api=uri, params=params), method=method)
    elif method == "POST":
        headers, _ = generate_headers(a1=cookies.get("a1"), api=uri, data=data, method=method)
    else:
        raise Exception("请求方式错误")
    return headers


def parse_note_html(html: str) -> Optional[dict]:
    """
    解析HTML帖子详情
    :param html: 帖子HTML源码
    :return:
    """
    match = re.search(r"window\.__SETUP_SERVER_STATE__\s*=\s*(.*?)</script>", html, re.DOTALL | re.IGNORECASE)
    if match:
        return json.loads(match.group(1)).get("LAUNCHER_SSR_STORE_PAGE_DATA", {})
    else:
        logger.warning("HTML中未找到帖子信息！")
        return None
