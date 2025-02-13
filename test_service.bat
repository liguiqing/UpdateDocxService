@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

REM 设置测试目录和目标目录
set TEST_DIR=E:\temp\sample-docx
set DOWNLOAD_DIR=E:\temp\download-docx

REM 读取 SERVER_INSTANCE_ID
set /p HOST=<server_instance_id.txt

REM 创建下载目录（如果不存在）
if not exist "%DOWNLOAD_DIR%" mkdir "%DOWNLOAD_DIR%"

REM 上传文件并记录 UUID 和原始文件名
echo Uploading %TEST_DIR% files to %HOST%...
echo . 
echo . 
for /f "delims=" %%F in ('dir /b /s "%TEST_DIR%\*.docx"') do (
    echo Uploading %%F to %HOST%...
    REM curl -X GET -H "X-Server-Instance-ID: %HOST%" http://%HOST%/api/test 
    REM 上传文件并提取 UUID
    for /f "tokens=2 delims=:,{} " %%i in ('curl -s -F "file=@%%F" http://%HOST%/api/upload-docx/') do (
        set response=%%i
        set uuid=!response:~1,-1!
        echo File UUID: !uuid!
    )
    timeout /t 5 >nul
    echo .    
    echo Get status for UUID: !uuid!
    curl -X GET -H "X-Server-Instance-ID: %HOST%" http://%HOST%/api/status-docx/!uuid! 
    echo .    
    REM 下载文件
    echo Downloading  UUID: !uuid!
    curl -X GET -H "X-Server-Instance-ID: %HOST%" http://%HOST%/api/download-docx/!uuid! -o "%DOWNLOAD_DIR%\!uuid!.docx"
    echo .
    REM 删除文件
    echo Deleting  UUID: !uuid!
    REM curl -X DELETE -H "X-Server-Instance-ID: %HOST%" http://%HOST%/api/delete-docx/!uuid!    
    echo .
    echo ------------------------------------------------------------------------------------------------------ 
    echo .
    echo .
)

echo Test completed.

pause