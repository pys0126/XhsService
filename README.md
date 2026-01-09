# XhsService - 小红书采集API服务

🔥【XHS采集API服务】使用FastAPI编写接口，采集方法完全解耦，可以自行调用。

## 功能特性

- 🔐 自动签名和自动获取Cookie
- 🛡️ FastAPI框架支持

## 技术栈

- Python 3.8+
- FastAPI
- curl_cffi
- uvicorn
- orjson
- DrissionPage
- pyexecjs

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

#### 开发模式（带自动重载）
```bash
python main.py dev
```

#### 生产模式
```bash
python main.py pro
```

服务默认运行在 `http://0.0.0.0:6868`

### 2. 使用示例

#### 在代码中直接使用
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

## 已有 API 接口

接口详细文档可访问 `http://127.0.0.1:6868/docs`

**注意：每个接口都支持传入 `proxy` 参数，用于设置代理。**

### 发送手机验证码
```
GET /send_phone_code?phone={phone_number}
```

### 手机号登录
```
GET /phone_login?phone={phone_number}&code={verification_code}
```

### 获取用户笔记列表
```
GET /get_user_notes?user_id={user_id}&xsec_token={xsec_token}[&xsec_source=pc_note][&cursor={cursor}]
```

### 获取笔记详情
```
GET /get_note_by_id?note_id={note_id}&xsec_token={xsec_token}[&xsec_source=pc_user]
```

### 获取评论列表
```
GET /get_comment_list?note_id={note_id}&xsec_token={xsec_token}[&cursor={cursor}]
```

### 获取子评论列表
```
GET /get_sub_comment_list?note_id={note_id}&comment_id={comment_id}&xsec_token={xsec_token}[&cursor={cursor}]
```


## 配置文件

### cookies.json
用于存储小红书登录后的Cookie信息，可自行修改。

**注意：如果通过手机号登录接口获取会自动保存到该文件中。**

### 代理配置
可在调用时传入 `proxy` 参数，例如：
```python
xhs_logic = XhsLogic(proxy="http://127.0.0.1:7897")
```

## 开发说明

`XhsLogic` 类封装专用请求内置的请求方法 `_reuqest`，自动生成签名和请求逻辑，可自行添加更多方法。


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
