import os

# 获取程序执行的目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 定义临时文件存储目录
TEMP_DIR = os.path.join(BASE_DIR, "temp")

# 创建临时目录（如果不存在）
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)