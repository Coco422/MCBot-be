# 使用 ARM 架构的 Python 3.11 镜像
FROM arm64v8/python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录到容器的工作目录
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置容器启动命令
CMD ["python", "app.py"]

# 暴露容器的端口
EXPOSE 6689