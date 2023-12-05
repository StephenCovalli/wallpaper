from PyQt5.QtCore import QEventLoop, QTimer, QThread
from PyQt5.QtWidgets import QDesktopWidget
from wallwapper.LogConfig import logger as log
import requests
import urllib3
import os
import time
import ctypes

urllib3.disable_warnings()

class WallpaperUpdater(QThread):
    def __init__(self):
        super().__init__()
        self.image_index = 0
        self.interval = 0
        self.use_online = False
        self.running = False

    def set_wallpaper(self, image_path):
        # # 打开图片并调整大小以适应屏幕
        # img = Image.open(image_path)
        # screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        # screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        # resized_img = img.resize((screen_width, screen_height))
        # # 保存调整大小后的图片
        # temp_path = os.path.join(os.path.dirname(image_path), "resized_wallpaper.jpg")
        # resized_img.save(temp_path)
        # 设置壁纸
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        # 删除临时文件
        # os.remove(temp_path)

    def update_wallpaper(self):
        while self.running:
            if self.use_online:
                #获取当前电脑屏幕分辨率
                screen = QDesktopWidget().screenGeometry()
                width = screen.width()
                height = screen.height()
                # 在线图片URL
                url = "https://picsum.photos/{}/{}".format(width,height)
                # 下载图片
                response = requests.get(url,verify=False)
                if response.status_code == 200:
                    # 获取当前工作目录
                    current_directory = os.getcwd()
                    # 创建保存图片的目录
                    image_directory = os.path.join(current_directory, "File")
                    os.makedirs(image_directory, exist_ok=True)
                    # 生成唯一的文件名
                    timestamp = int(time.time())
                    filename = f"wallpaper_{timestamp}.jpg"
                    # 图片保存路径
                    image_path = os.path.join(image_directory, filename)
                    with open(image_path, "wb") as f:
                        f.write(response.content)
                    # 设置壁纸
                    self.set_wallpaper(image_path)
            else:
                # 离线图片目录
                image_directory = os.path.join(os.getcwd(), "File")
                # 获取图片文件列表
                image_files = os.listdir(image_directory)
                if len(image_files) > 0:
                    # 获取当前图片的索引
                    current_index = self.image_index % len(image_files)
                    # 获取图片路径
                    image_path = os.path.join(image_directory, image_files[current_index])
                    # 设置壁纸
                    self.set_wallpaper(image_path)
                    # 更新图片索引
                    self.image_index += 1
            log.info("wallpaper change successfully")
            # 等待指定时间
            event_loop = QEventLoop()
            QTimer.singleShot(self.interval * 1000, event_loop.quit)
            event_loop.exec_()

    def run(self):
        self.update_wallpaper()
