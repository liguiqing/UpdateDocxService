from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
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

@router.post("/upload-docx/")
async def upload_docx(file: UploadFile = File(...)):
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .docx files are allowed.")
    
    file_id = str(uuid4())
    temp_file_path = os.path.join(TEMP_DIR, f"{file_id}.docx")
    
    try:
        logger.info(f"Saving uploaded file to {temp_file_path}")
        await save_file(file, temp_file_path)
        
        # 标记文件正在更新
        file_update_status[file_id] = "updating"
        
        logger.info(f"Updating TOC for file {temp_file_path}")
        await toc_updater.update_toc(temp_file_path)
        
        # 标记文件更新完成
        file_update_status[file_id] = "updated"
        
        logger.info(f"File {temp_file_path} updated successfully")
        return {"uuid": file_id}
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        file_update_status[file_id] = "error"
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download-docx/{file_id}")
async def download_docx(file_id: str):
    updated_file_path = os.path.join(TEMP_DIR, f"{file_id}.docx")
    
    # 等待文件更新完成
    timeout = 30  # 超时时间（秒）
    for _ in range(timeout):
        if file_update_status.get(file_id) == "updated":
            break
        elif file_update_status.get(file_id) == "error":
            raise HTTPException(status_code=500, detail="File update failed")
        await asyncio.sleep(1)
    else:
        raise HTTPException(status_code=408, detail="File update timeout")
    
    if not os.path.exists(updated_file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(updated_file_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=f"{file_id}.docx")

@router.delete("/delete-docx/{file_id}")
async def delete_docx(file_id: str):
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
        return {"message": "File deleted successfully"}
    except Exception as e:
        logger.error(f"An error occurred while deleting file: {e}")
        raise HTTPException(status_code=500, detail=str(e))