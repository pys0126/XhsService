from argparse import ArgumentParser, Namespace
import uvicorn


# 创建 ArgumentParser 对象
parser: ArgumentParser = ArgumentParser(description="启动ASGI服务器")
# 添加参数
parser.add_argument("start_mode", type=str, choices=["pro", "dev"],
                    help="启动模式: [pro：生产模式，dev：开发模式（自动重载、调试）]")
# 解析命令行参数
args: Namespace = parser.parse_args()


if __name__ == "__main__":
    # 定义Web API参数
    params: dict = {
        "app": "service:app",
        "host": "0.0.0.0",
        "port": 6868
    }
    # 开发模式加重载参数
    if args.start_mode == "dev":
        params.update(reload=True)
    elif args.start_mode == "pro":
        params.update(workers=4)
    uvicorn.run(**params)
