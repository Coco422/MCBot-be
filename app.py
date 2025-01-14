from dotenv import load_dotenv
# 在程序启动时加载 .env 文件
load_dotenv()

from fastapi import FastAPI
import uvicorn
from routers.api_router import api_router
from fastapi.middleware.cors import CORSMiddleware

# 初始化 FastAPI 应用
app = FastAPI()

# 配置 CORS TODO
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源的请求，也可以指定具体的域名，如 ["https://example.com"]
    allow_credentials=True,  # 允许携带凭证（如 cookies）
    allow_methods=["*"],  # 允许所有 HTTP 方法，也可以指定具体的方法，如 ["GET", "POST"]
    allow_headers=["*"],  # 允许所有请求头，也可以指定具体的请求头
)

# 将路由器添加到应用
app.include_router(api_router)

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=5575)