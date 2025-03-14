from dotenv import load_dotenv
# 在程序启动时加载 .env 文件
load_dotenv(override=True)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from routers.api_router import api_router
from routers.dev_router import dev_router
from routers.lg_router import lg_router # Import the new router
from fastapi.middleware.cors import CORSMiddleware

# 初始化 FastAPI 应用
app = FastAPI(
    openapi_tags=[
        {
            "name": "Dev",
            "description": "这是开发环境相关的 API，用于测试和调试。请不要直接在系统中使用dev下的接口"
        },
        {
            "name": "LG",
            "description": "这是 LG 系统的 API，用于获取 LG 系统的数据"
        }
    ],
    docs_url=f"/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None

    )

# 配置 CORS TODO
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源的请求，也可以指定具体的域名，如 ["https://example.com"]
    allow_credentials=True,  # 允许携带凭证（如 cookies）
    allow_methods=["*"],  # 允许所有 HTTP 方法，也可以指定具体的方法，如 ["GET", "POST"]
    allow_headers=["*"],  # 允许所有请求头，也可以指定具体的请求头
)

# 健康检查接口
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# 将路由器添加到应用
app.include_router(api_router)

# 开发路由
app.include_router(dev_router)

app.include_router(lg_router)  # Add the new router

# 挂载静态文件目录到根路径
app.mount("/", StaticFiles(directory="html", html=True), name="static")

app.mount("/miniai", StaticFiles(directory="html/miniai", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6688)