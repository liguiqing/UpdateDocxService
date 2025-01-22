import win32com.client as win32
import logging

class TocUpdater:
    def __init__(self):
        self.word_app = win32.Dispatch("Word.Application")
        self.word_app.Visible = False

    async def update_toc(self, file_path):
        try:
            doc = self.word_app.Documents.Open(file_path)
            for toc in doc.TablesOfContents:
                toc.Update()
            doc.Save()
            doc.Close()
            
            logging.info(f"成功更新目录: {file_path}")
            return file_path
        except Exception as e:
            logging.error(f"更新目录失败: {file_path}, 错误: {e}")
            raise e

    def delete_temp_files(self, file_paths):
        import os

        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)