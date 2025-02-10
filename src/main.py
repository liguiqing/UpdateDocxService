import logging
import socket
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.docx_routes import router as docx_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(docx_router, prefix="/api")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_available_port(start_port=48000):
    port = start_port
    host = get_host_ip()
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex((host, port)) != 0:
                return port
            port += 1

def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    import uvicorn
    port = find_available_port()
    host = get_host_ip()
    SERVER_INSTANCE_ID = f"{host}:{port}"
    logger.info(f"Starting server on {SERVER_INSTANCE_ID}")
    
    # 将 SERVER_INSTANCE_ID 写入文件
    with open("server_instance_id.txt", "w") as f:
        f.write(SERVER_INSTANCE_ID)

    @app.middleware("http")
    async def add_server_instance_id_header(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Server-Instance-ID"] = SERVER_INSTANCE_ID
        return response

    uvicorn.run(app, host=host, port=port)