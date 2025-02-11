import asyncio
import logging
import socket
import os
import multiprocessing
import subprocess
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.docx_routes import router as docx_router
from utils.status_manager import write_status
app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(docx_router, prefix="/api")

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_available_port(start_port=48000):
    """找到一个可用端口"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        for port in range(start_port, 65535):
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No available ports found.")

def get_host_ip():
    """获取本机 IP"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(('10.254.254.254', 1))
            return s.getsockname()[0]
        except Exception:
            return '127.0.0.1'

host = get_host_ip()
port = find_available_port()
SERVER_INSTANCE_ID = f"{host}:{port}"

@app.middleware("http")
async def add_server_instance_id_header(request: Request, call_next):
    """添加服务器实例 ID 到响应头"""
    response = await call_next(request)
    response.headers["X-Server-Instance-ID"] = SERVER_INSTANCE_ID
    return response

def run_server(host, port):
    """在子进程中运行 Uvicorn"""
    os.environ["SERVER_INSTANCE_ID"] = f"{host}:{port}"
    
    with open("server_instance_id.txt", "w") as f:
        f.write(os.environ["SERVER_INSTANCE_ID"])

    # 在同步函数中执行异步操作
    asyncio.run(write_status("200"))

    subprocess.run([
        "uvicorn", "main:app",
        "--host", host,
        "--port", str(port),
        "--log-level", "info"
    ], check=True)

if __name__ == "__main__":
    logger.info(f"Starting server on {SERVER_INSTANCE_ID}")

    # 启动子进程运行服务器
    process = multiprocessing.Process(target=run_server, args=(host, port))
    process.start()
    
    # 确保获取到 PID
    time.sleep(1)
    
    if process.pid:
        with open("pid.txt", "w") as f:
            f.write(str(process.pid))
        logger.info(f"Uvicorn server started with PID: {process.pid}")
    else:
        logger.error("Failed to retrieve process PID.")
