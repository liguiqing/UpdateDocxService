@echo off

REM 设置测试目录和目标目录
set TEST_DIR=E:\temp\test-docx
set DOWNLOAD_DIR=E:\temp\download-docx

REM 创建下载目录（如果不存在）
if not exist "%DOWNLOAD_DIR%" mkdir "%DOWNLOAD_DIR%"

REM 上传文件并记录 UUID 和原始文件名
echo Uploading files...
for %%F in ("%TEST_DIR%\*.docx") do (
    echo Uploading %%F...
    curl -X POST "http://localhost:8000/api/upload-docx/" -F "file=@%%F" -o temp_response.json
    for /f "tokens=2 delims=:,{} " %%i in ('findstr /i "uuid" temp_response.json') do set UUID=%%i
    echo Uploaded %%F with UUID: %UUID%
    echo %UUID% %%~nxF >> uploaded_files.txt
)

REM 下载文件
echo Downloading files...
for /f "tokens=1,2" %%i in (uploaded_files.txt) do (
    echo Downloading file with UUID: %%i...
    curl -X GET "http://localhost:8000/api/download-docx/%%i" -o "%DOWNLOAD_DIR%\%%j"
)

REM 删除文件
echo Deleting files...
for /f "tokens=1" %%i in (uploaded_files.txt) do (
    echo Deleting file with UUID: %%i...
    curl -X DELETE "http://localhost:8000/api/delete-docx/%%i"
)

REM 清理临时文件
del temp_response.json
del uploaded_files.txt

echo Test completed.
pause