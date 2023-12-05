import datetime
import os
from PyQt5.QtCore import QThread, QEventLoop, QTimer
from wallwapper.LogConfig import logger as log


class CleanUpRegularly(QThread):
    def __init__(self):
        super().__init__()
        self.use_online = False
        # 指定时间间隔，例如清理前2天的文件
        self.time_delta = datetime.timedelta(days=2)
        self.interval = 86400

    def clear_previous_files(self):
        while self.use_online:
            current_time = datetime.datetime.now()
            previous_time = current_time - self.time_delta
            # 创建保存图片的目录
            image_directory = os.path.join(os.getcwd(), "File")
            os.makedirs(image_directory, exist_ok=True)
            for filename in os.listdir(image_directory):
                file_path = os.path.join(image_directory, filename)
                if os.path.isfile(file_path):
                    modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                    if modified_time < previous_time:
                        os.remove(file_path)
            # 等待指定时间
            log.info("Cleanup task executed successfully")
            event_loop = QEventLoop()
            QTimer.singleShot(self.interval * 1000, event_loop.quit)
            event_loop.exec_()

    def run(self):
        self.clear_previous_files()



