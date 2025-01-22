@echo off
REM filepath: /e:/temp/UpdateDocxService/start_service.bat

REM 激活虚拟环境（如果有）
REM call path\to\your\venv\Scripts\activate

REM 设置 PYTHONPATH 环境变量
set PYTHONPATH=%cd%\src

REM 安装依赖项
pip install -r requirements.txt

REM 启动服务
python src/main.py

pause