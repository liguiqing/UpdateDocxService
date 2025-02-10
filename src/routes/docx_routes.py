from fastapi import APIRouter, File, UploadFile, HTTPException, Request, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from uuid import uuid4
import os
from services.toc_updater import TocUpdater
from utils.file_handler import save_file, delete_temp_files
from config import TEMP_DIR
import logging
import asyncio

router = APIRouter()
toc_updater = TocUpdater()
logger = logging.getLogger(__name__)

# 跟踪文件更新状态
file_update_status = {}

async def process_file(file_id, file_path):
    try:
        logger.info(f"Updating TOC for file {file_path}")
        toc_updater.update_toc(file_path)
        # 标记文件更新完成
        file_update_status[file_id] = "updated"
        logger.info(f"File {file_path} updated successfully")
    except Exception as e:
        file_update_status[file_id] = "error"
        logger.error(f"An error occurred while updating file: {e}")
        # 将状态码写入文件
        with open("status.txt", "w") as f:
            f.write(500)


@router.post("/upload-docx/")
async def upload_docx(background_tasks: BackgroundTasks, file: UploadFile = File(...)):

    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .docx files are allowed.")
    
    file_id = str(uuid4())
    temp_file_path = os.path.join(TEMP_DIR, f"{file_id}.docx")
    
    try:
        logger.info(f"Saving uploaded file to {temp_file_path}")
        await save_file(file, temp_file_path)
        
        # 标记文件正在更新
        file_update_status[file_id] = "updating"
        background_tasks.add_task(process_file, file_id, temp_file_path)
        return JSONResponse(content={"uuid": file_id})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        file_update_status[file_id] = "error"
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download-docx/{file_id}")
async def download_docx(request: Request, file_id: str):
    server_instance_id = request.headers.get("X-Server-Instance-ID")
    logger.info(f"GET: /download-docx X-Server-Instance-ID: {server_instance_id}")

    updated_file_path = os.path.join(TEMP_DIR, f"{file_id}.docx")
    
    # 检查文件状态
    status = file_update_status.get(file_id)
    if status == "updating":
        response = JSONResponse(content={"status": "updating"}, status_code=202)
        response.headers["X-Server-Instance-ID"] = server_instance_id
        return response
    elif status == "error":
        raise HTTPException(status_code=500, detail="File update failed")
    elif status != "updated":
        raise HTTPException(status_code=404, detail="File not found")
    
    if not os.path.exists(updated_file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    response = FileResponse(updated_file_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=f"{file_id}.docx")
    response.headers["X-Server-Instance-ID"] = server_instance_id
    return response

@router.delete("/delete-docx/{file_id}")
async def delete_docx(request: Request, file_id: str):
    server_instance_id = request.headers.get("X-Server-Instance-ID")
    logger.info(f"DELETE /delete-docx X-Server-Instance-ID: {server_instance_id}")

    file_path = os.path.join(TEMP_DIR, f"{file_id}.docx")
    
    # 检查文件是否正在操作
    if file_update_status.get(file_id) == "updating":
        raise HTTPException(status_code=400, detail="File is being updated")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        delete_temp_files(file_path)
        logger.info(f"File {file_path} deleted successfully")
        file_update_status.pop(file_id, None)  # 删除状态跟踪
        return JSONResponse(content={"message": "File deleted successfully", "server_instance_id": server_instance_id})
    except Exception as e:
        logger.error(f"An error occurred while deleting file: {e}")
        raise HTTPException(status_code=500, detail=str(e))