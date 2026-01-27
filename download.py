from urllib.parse import urlparse, parse_qs
from curl_cffi import Response, requests
from service.logic import XhsLogic
from typing import Optional
from loguru import logger
from random import choice
from tqdm import tqdm
import typer
import time
import os


def parse_url_params(url: str) -> dict:
    """
    解析 URL 参数
    :param url: GET请求URL
    :return: 参数字典
    """
    parsed = urlparse(url)
    params = parse_qs(parsed.query, keep_blank_values=True)
    return {k: v[0] if len(v) == 1 else v for k, v in params.items()}


class Download(object):
    def __init__(self, proxy: str = None, save_dir: str = "downloads") -> None:
        """
        XHS下载工具
        :param proxy: 设置代理，例：http://127.0.0.1:7897
        :param save_dir: 文件保存目录
        """
        self.headers: dict = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"
        }
        self.xhs_logic: XhsLogic = XhsLogic(proxy=proxy)
        self.save_dir: str = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def note_veideo(self, url: str) -> None:
        """
        下载笔记原画视频
        :param url: 笔记完整URL，例：https://www.xiaohongshu.com/explore/64565216000000002702b26b?xsec_token=ABcnmyqK0A3I-Ij84SirZ0QbSVnd9SuWIv0Y00JRvMm4s=&xsec_source=pc_feed
        :return:
        """
        params: dict = parse_url_params(url)
        result_json: dict = self.xhs_logic.get_note_by_html(
            note_id=url.split("?")[0].split("/")[-1],
            xsec_token=params.get("xsec_token"),
            xsec_source=params.get("xsec_source")
        )
        # 提取视频键值
        note_info: dict = result_json.get("noteData", {})
        video_key: str = note_info.get("video", {}).get("consumer", {}).get("originVideoKey", "")
        if not video_key:
            logger.error("笔记中未找到视频！")
            return None
        logger.info(f"【{note_info.get('title')}】已获取到笔记数据，正在下载视频...")
        response: Response = requests.get(
            url="http://sns-video-hs.xhscdn.com/" + video_key,
            headers=self.headers,
            timeout=600,  # 10分钟超时，适合大文件
            stream=True   # 启用流式下载
        )
        if response.status_code != 200:
            logger.error(f"视频下载失败，状态码：{response.status_code}")
            return None
        # 获取文件总大小
        total_size = int(response.headers.get('content-length', 0))
        save_dir: str = os.path.join(self.save_dir, "video")
        os.makedirs(save_dir, exist_ok=True)
        nickname: str = note_info.get("user", {}).get("nickName", "NONE")  # 作者
        save_path: str = os.path.join(save_dir, f"【{nickname}】{note_info.get('title')}.mp4")
        # 使用tqdm显示下载进度
        with open(save_path, "wb") as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="下载进度") as pbar:
                for chunk in response.iter_content(chunk_size=8192):  # 每次读取8KB
                    if chunk:  # 过滤掉空的chunks
                        f.write(chunk)
                        pbar.update(len(chunk))  # 更新进度条
        logger.success(f"作者：{nickname}【{note_info.get('title')}】视频保存成功：{os.path.abspath(save_path)}")

    def note_images(self, url: str) -> None:
        """
        下载笔记无水印图片
        :param url: 笔记完整URL，例：https://www.xiaohongshu.com/explore/64565216000000002702b26b?xsec_token=ABcnmyqK0A3I-Ij84SirZ0QbSVnd9SuWIv0Y00JRvMm4s=&xsec_source=pc_feed
        :return:
        """
        params: dict = parse_url_params(url)
        result_json: dict = self.xhs_logic.get_note_by_html(
            note_id=url.split("?")[0].split("/")[-1],
            xsec_token=params.get("xsec_token"),
            xsec_source=params.get("xsec_source")
        )
        # 获取图片URL列表
        note_info: dict = result_json.get("noteData", {})
        image_urls: list = [image.get("url", "") for image in note_info.get("imageList", [])]
        nickname: str = note_info.get("user", {}).get("nickName", "NONE")  # 作者
        save_dir: str = os.path.join(self.save_dir, "image", nickname)
        os.makedirs(save_dir, exist_ok=True)
        logger.info(f"作者：{nickname}【{note_info.get('title')}】已获取到笔记数据，开始下载图片...")
        for index, image_url in enumerate(image_urls, 1):
            response: Response = requests.get(
                url=image_url,
                headers=self.headers
            )
            if response.status_code != 200:
                logger.warning(f"第 {index} 张图片下载失败！")
                continue
            save_path: str = os.path.join(save_dir, f"【{index}】{note_info.get('title')}.jpg")
            with open(save_path, "wb") as f:
                f.write(response.content)
            logger.info(f"作者：{nickname}【{note_info.get('title')}】第 {index} 张图片保存成功：{os.path.abspath(save_path)}")
        logger.success(f"作者：{nickname}【{note_info.get('title')}】图片下载完毕：{os.path.abspath(save_dir)}")


app = typer.Typer(help="XHS下载工具 - UodRad")


@app.command(name="video")
def download_video(
    url: str = typer.Argument(..., help="笔记完整URL，例：https://www.xiaohongshu.com/explore/64565216000000002702b26b?xsec_token=ABcnmyqK0A3I-Ij84SirZ0QbSVnd9SuWIv0Y00JRvMm4s=&xsec_source=pc_feed"),
    proxy: Optional[str] = typer.Option(None, help="设置代理，例：http://127.0.0.1:7897"),
    save_dir: str = typer.Option("downloads", help="文件保存目录")
):
    """
    下载笔记原画视频
    """
    try:
        Download(proxy=proxy, save_dir=save_dir).note_veideo(url)
    except Exception:
        import traceback
        logger.error(f"下载失败，报错信息：{traceback.format_exc()}")


@app.command(name="batch-video")
def download_batch_video(
    url_file: str = typer.Argument(..., help="笔记URL列表TXT文件，每行一个笔记URL，例：https://www.xiaohongshu.com/explore/64565216000000002702b26b?xsec_token=ABcnmyqK0A3I-Ij84SirZ0QbSVnd9SuWIv0Y00JRvMm4s=&xsec_source=pc_feed"),
    proxy: Optional[str] = typer.Option()
):
    """
    批量下载笔记原画视频
    """
    try:
        with open(url_file, "r", encoding="utf-8") as f:
            urls: list = [url.strip() for url in f.readlines()]
        for url in urls:
            logger.info(f"开始下载：{url}")
            try:
                Download(proxy=proxy).note_veideo(url)
            except Exception:
                import traceback
                logger.error(f"当前笔记下载失败，待会重新跑一次试试，笔记URL：{url}\n报错信息：{traceback.format_exc()}")
                continue
            logger.info("防止过度采集，随机休眠1-3秒...")
            time.sleep(choice([1, 3]))  # 随机休眠1-3秒
            print()
    except Exception:
        logger.error("读取笔记URL列表文件失败，请检查文件路径或内容是否正确！")
        return None


@app.command(name="images")
def download_images(
    url: str = typer.Argument(..., help="笔记完整URL，例：https://www.xiaohongshu.com/explore/64565216000000002702b26b?xsec_token=ABcnmyqK0A3I-Ij84SirZ0QbSVnd9SuWIv0Y00JRvMm4s=&xsec_source=pc_feed"),
    proxy: Optional[str] = typer.Option(None, help="设置代理，例：http://127.0.0.1:7897"),
    save_dir: str = typer.Option("downloads", help="文件保存目录")
):
    """
    下载笔记无水印图片
    """
    try:
        Download(proxy=proxy, save_dir=save_dir).note_images(url)
    except Exception:
        logger.error("下载失败，重新跑一次试试，嘿嘿~")


@app.command(name="batch-images")
def download_batch_images(
    url_file: str = typer.Argument(..., help="笔记URL列表TXT文件，每行一个笔记URL，例：https://www.xiaohongshu.com/explore/64565216000000002702b26b?xsec_token=ABcnmyqK0A3I-Ij84SirZ0QbSVnd9SuWIv0Y00JRvMm4s=&xsec_source=pc_feed"),
    proxy: Optional[str] = typer.Option()
):
    """
    批量下载笔记无水印图片
    """
    try:
        with open(url_file, "r", encoding="utf-8") as f:
            urls: list = [url.strip() for url in f.readlines()]
        for url in urls:
            logger.info(f"开始下载：{url}")
            try:
                Download(proxy=proxy).note_images(url)
            except Exception:
                logger.error(f"当前笔记下载失败，待会重新跑一次试试，笔记URL：{url}")
                continue
            logger.info("防止过度采集，随机休眠1-3秒...")
            time.sleep(choice([1, 3]))  # 随机休眠1-3秒
            print()
    except Exception:
        logger.error("读取笔记URL列表文件失败，请检查文件路径或内容是否正确！")
        return None


if __name__ == "__main__":
    app()
