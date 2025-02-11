import asyncio
import logging

logger = logging.getLogger(__name__)

STATUS_FILE = "status.txt"
_lock = asyncio.Lock()  # 防止并发写入冲突

async def write_status(status: str):
    """异步写入状态文件"""
    try:
        async with _lock:
            with open(STATUS_FILE, "w", encoding="utf-8") as f:
                f.write(status)
                f.flush()  # 立刻写入，防止数据丢失
        logger.info(f"Status updated: {status}")
    except Exception as e:
        logger.error(f"Failed to write status file: {e}")

def read_status():
    """同步读取状态文件的首行"""
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            status = f.readline().strip()
        logger.info(f"Status read: {status}")
        return status
    except Exception as e:
        logger.error(f"Failed to read status file: {e}")
        return "200"
# async def write_status(status: str):
#     """异步写入状态文件，避免 I/O 竞争"""
#     try:
#         async with _lock:  # 确保多个任务不会同时写入
#             async with await asyncio.to_thread(open, STATUS_FILE, "w", encoding="utf-8") as f:
#                 await asyncio.to_thread(f.write, status)
#                 await asyncio.to_thread(f.flush)
#         logger.info(f"Status updated: {status}")
#     except Exception as e:
#         logger.error(f"Failed to write status file: {e}")
