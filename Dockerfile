# 使用官方 Python 3.11 镜像作为基础镜像 (arm64 架构)
FROM python:3.11-slim-buster

# 设置工作目录
WORKDIR /app

# 更新 apt 包管理器并安装 curl
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# 复制 requirements.txt 文件到容器中
COPY requirements.txt .

# 安装依赖 (使用 --no-cache-dir 选项减小镜像大小)
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码到容器中
COPY . .

EXPOSE 6688

# 启动命令 (使用 uvicorn 作为 ASGI 服务器)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "6688"]