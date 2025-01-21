from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from uuid import uuid4
import os
from services.toc_updater import TocUpdater
from utils.file_handler import save_file, delete_temp_files

router = APIRouter()
toc_updater = TocUpdater()

@router.post("/upload-docx/")
async def upload_docx(file: UploadFile = File(...)):
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .docx files are allowed.")
    
    file_id = str(uuid4())
    temp_file_path = f"temp/{file_id}.docx"
    
    try:
        await save_file(file, temp_file_path)
        updated_file_path = await toc_updater.update_toc(temp_file_path)
        return FileResponse(updated_file_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=f"updated_{file.filename}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        delete_temp_files(temp_file_path)