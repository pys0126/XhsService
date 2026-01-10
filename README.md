# XhsService - 小红书采集API服务

🔥【XHS采集服务】支持API、代码调用和命令行下载，采集方法完全解耦，可扩展、集成。

## 功能特性

- 🔐 自动签名和自动获取Cookie
- 🛡️ FastAPI框架支持
- 📝 代码即拆即用
- 💾 命令行下载

## 技术栈

- Python 3.8+
- FastAPI
- curl_cffi
- uvicorn
- orjson
- DrissionPage
- DrissionRecord
- pyexecjs
- typer

## 安装依赖

### Python依赖
```bash
pip install -r requirements.txt
```

### Node.js依赖
```bash
npm install
```

## 快速开始

### 1. 启动API服务

#### 开发模式（带自动重载，可调试）
```bash
python main.py dev
```

#### 生产模式
```bash
python main.py pro
```

服务默认运行在 `http://0.0.0.0:6868`

#### 接口列表

- ✅发送手机验证码
- ✅手机号登录
- ✅获取用户笔记列表
- ✅获取笔记详情（从手机端HTML中拿，无需Cookie，好像也不会风控）
- ✅获取笔记详情
- ✅获取评论列表
- ✅获取子评论列表

更多接口文档可访问 `http://127.0.0.1:6868/docs` ，返回的数据结构查看 `structure` 文件夹中的JSON文件。

**注意：每个接口都支持传入 `proxy` 参数，用于设置代理。**

### 2. 使用代码调用

```python
from service.logic import XhsLogic

xhs_logic = XhsLogic()  # 采集方法都封装在该类中

# 获取用户笔记列表
response = xhs_logic.get_user_notes(
    user_id="60ae2ccd000000000101c7bd", 
    xsec_token="ABWmyxguRSEPAC9GK04l453BxNIXXt4eqJfc9W1mc1fc4="
)
print(response.get("notes", []))

# 获取笔记详情
response = xhs_logic.get_note_by_id(
    note_id="6809bac8000000000b01ee79", 
    xsec_token="AB7lrCWslhUrZJqf-QuwYLVPL_B26kNuPVyoooytH9UDI="
)
print(response)

# 获取评论列表
response = xhs_logic.get_comment_list(
    note_id="6954bbec0000000022033432", 
    xsec_token="ABUN_1XSqLnjriCqCbVauqogsQ7WUawkzwAIqmfpI8Jfo="
)
print(response.get("comments", []))
```

### 3. 使用命令行下载

#### 下载笔记视频（原画质）
使用 `python` 执行 `download.py` 脚本（依赖 `typer` 库）

#### 可选参数

- `--proxy`：设置代理，例如 `--proxy http://127.0.0.1:7897`
- `--save-dir`：指定保存目录，默认为 `./downloads`

**完整示例：**
```bash
# 使用代理下载视频（原画）到指定目录
python download.py video "笔记完整URL" --proxy http://127.0.0.1:7897 --save-dir my_videos

# 使用代理下载图片（无水印）到指定目录
python download.py images "笔记完整URL" --proxy http://127.0.0.1:7897 --save-dir my_images
```

**说明：**
- 视频文件保存在：`{save_dir}/video/` 目录下
- 图片文件保存在：`{save_dir}/image/{笔记标题}/` 目录下
- 下载的视频为原画质，图片为无水印版本


## 配置文件

### cookies.json
用于存储小红书登录后的Cookie信息，cookie格式样例：
```json
{
    "a1": "19b979bfaccv9xzo6lown20n129b5ztl398ci2v9q40000101067",
    "web_session": "030037ae6d4fc6ce64de253d182e4a169405cf",
    "webId": "ebb32022c8f9a9f13ea4a00c03445b40"
}
```

**注意：如果通过手机号登录接口获取会自动保存到该文件中。**

### 代理配置
可在调用API时传入 `proxy` 参数；如果使用代码调用，参考：
```python
xhs_logic = XhsLogic(proxy="http://127.0.0.1:7897")
```

## 开发说明

`XhsLogic` 类封装专用请求内置的请求方法 `_reuqest`，自动生成签名和请求逻辑，可自行添加更多方法。

`service/utils.py` 中的 `refresh_cookie` 函数可以调用 `DrissionPage` 去自动获取Cookie，并保存到 `cookies.json` 文件中。

## 注意事项

⚠️ **请遵守相关法律法规，合理使用本工具**

- 仅用于学习和研究目的
- 不要进行大规模或高频次的数据抓取
- 遵守小红书的使用条款和服务协议
- 注意保护个人隐私信息

## 借鉴引用

- [xhs](https://github.com/ReaJason/xhs)
- [Spider_XHS](https://github.com/cv-cat/Spider_XHS)
- [xhshow](https://github.com/Cloxl/xhshow)
