import aiofiles
import os

async def save_file(upload_file, destination_path):
    async with aiofiles.open(destination_path, 'wb') as out_file:
        content = await upload_file.read()
        await out_file.write(content)

def delete_temp_files(*file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)

def return_updated_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()