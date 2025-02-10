@echo off
REM filepath: /e:/temp/UpdateDocxService/start_service.bat

REM 激活虚拟环境（如果有）
REM call path\to\your\venv\Scripts\activate

REM 设置 PYTHONPATH 环境变量
set PYTHONPATH=%cd%\src

REM 安装依赖项
pip install -r requirements.txt

:loop
REM 启动服务
start /b python src/main.py
set SERVICE_PID=%!

REM 等待服务启动
timeout /t 10

REM 读取 SERVER_INSTANCE_ID
set /p SERVER_INSTANCE_ID=<server_instance_id.txt

:check
REM 测试 API

for /f "tokens=2 delims=:,{} " %%i in ('curl -s -F "file=@test.docx" http://%SERVER_INSTANCE_ID%/api/upload-docx/ ^| findstr /i "uuid"') do set uuid=%%i
curl -X DELETE -H "X-Server-Instance-ID: %SERVER_INSTANCE_ID%" http://%SERVER_INSTANCE_ID%/api/delete-docx/%uuid%

set /p status=<status.txt
if %status% geq 500 (
    taskkill /f /pid %SERVICE_PID%
    goto loop
)

REM 等待一分钟
timeout /t 60
goto check

pause