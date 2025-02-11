import logging
import os
from logging.handlers import TimedRotatingFileHandler


# 获取程序执行的目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 定义临时文件存储目录
TEMP_DIR = os.path.join(BASE_DIR, "temp")

# 创建临时目录（如果不存在）
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


# 创建日志目录
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 配置日志记录器
logger = logging.getLogger("UpdateDocxService")
logger.setLevel(logging.INFO)

# 创建一个处理器，按日期写入日志文件
handler = TimedRotatingFileHandler(
    filename=os.path.join(LOG_DIR, "service.log"),
    when="midnight",
    interval=1,
    backupCount=30
)
handler.suffix = "%Y-%m-%d"
handler.setLevel(logging.INFO)

# 创建日志格式，包含文件名
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(message)s')
handler.setFormatter(formatter)

# 添加处理器到日志记录器
logger.addHandler(handler)