@echo off

REM 设置 PYTHONPATH 环境变量
set PYTHONPATH=%cd%\src

REM 安装依赖项
pip install -r requirements.txt

:loop
REM 启动服务
start /b python src/main.py

REM 等待服务启动
timeout /t 10 >nul

set /p SERVICE_PID=<pid.txt
echo Server PID: %SERVICE_PID%

REM 读取 SERVER_INSTANCE_ID
set /p SERVER_INSTANCE_ID=<server_instance_id.txt
echo Server Instance ID: %SERVER_INSTANCE_ID%

:check
REM 测试 API
REM for /f "tokens=2 delims=:,{} " %%i in ('curl -s -F "file=@test.docx" http://%SERVER_INSTANCE_ID%/api/upload-docx/ ^| findstr /i "uuid"') do set uuid=%%i
REM curl -X DELETE -H "X-Server-Instance-ID: %SERVER_INSTANCE_ID%" http://%SERVER_INSTANCE_ID%/api/delete-docx/%uuid%

set /p status=<status.txt
echo Server Status: %status%

if %status% geq 500 (
    echo Restarting service...
    timeout /t 1 >nul
    taskkill /F /T /PID %SERVICE_PID%
    timeout /t 3 >nul
    goto loop
)

REM 等待1秒
timeout /t 1 >nul
goto check

pause
