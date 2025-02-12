import win32com.client as win32
from config import logger  # 导入日志记录器

class TocUpdater:
    def __init__(self):
        self.word_app = win32.Dispatch("Word.Application")
        self.word_app.Visible = False

    def update_toc(self, file_path):
        try:
            doc = self.word_app.Documents.Open(file_path)
            for toc in doc.TablesOfContents:
                toc.Update()
            doc.Save()
            doc.Close()
            
            logger.info(f"成功更新目录: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"更新目录失败: {file_path}, 错误: {e}")
            raise e
