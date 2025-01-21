from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from services.toc_updater import TocUpdater
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

toc_updater = TocUpdater()

@app.post("/upload-docx/")
async def upload_docx(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    temp_file_path = f"temp/{file_id}.docx"
    
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    updated_file_path = await toc_updater.update_toc(temp_file_path)
    
    os.remove(temp_file_path)  # Clean up the temporary file
    
    return FileResponse(updated_file_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=f"updated_{file_id}.docx")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)