import os
import sys
import winreg
from wallwapper.LogConfig import logger as log
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QComboBox, QPushButton, QCheckBox, QVBoxLayout, QWidget, \
    QSystemTrayIcon, QMenu, QAction, qApp, QApplication
from wallwapper.CleanUpRegularly import CleanUpRegularly
from wallwapper.WallWapperUpdater import WallpaperUpdater

TIME_OPTIONS = {
    "5分钟": 300,
    "10分钟": 600,
    "20分钟": 1200,
    "30分钟": 1800,
    "1小时": 3600,
    "2小时": 7200,
    "24小时": 86400
}

key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
def close_and_exit():
    qApp.quit()


def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = None
        self.interval = 600
        self.settings = None
        self.tray_menu = None
        self.tray_icon = None
        self.auto_start = False
        self.is_running = False
        self.quit_action = None
        self.restore_action = None
        self.interval_combo = None
        self.use_online_image = False
        self.wallpaper_updater = None
        self.start_stop_button = None
        self.clean_up_regularly = None
        self.auto_start_checkbox = None
        self.use_online_checkbox = None

        self.initialization()

    def initialization(self):
        self.setWindowTitle("自动更新壁纸")
        self.setFixedSize(400, 300)
        self.wallpaper_updater = WallpaperUpdater()
        self.clean_up_regularly = CleanUpRegularly()
        self.settings = self.load_settings()
        self.create_ui()
        self.start_clean()
        self.start_update()

    def load_settings(self):
        config_path = os.path.abspath(os.path.join(os.getcwd(), "resource/config/config.ini"))
        settings = QSettings(config_path, QSettings.IniFormat)
        log.info("当前配置文件路径："+config_path)
        # 如果配置文件不存在，则创建
        if not os.path.exists(config_path):
            settings.setValue("Settings/Interval", 600)
            settings.setValue("Settings/UseOnlineImage", False)
            settings.setValue("Settings/IsRunning", False)

        self.interval = settings.value("Settings/Interval", type=int)
        self.use_online_image = settings.value("Settings/UseOnlineImage", type=bool)
        self.is_running = settings.value("Settings/IsRunning", type=bool)

        return settings

    def save_settings(self, interval, use_online_image, is_running):
        self.settings.setValue("Settings/Interval", interval)
        self.settings.setValue("Settings/UseOnlineImage", use_online_image)
        self.settings.setValue("Settings/IsRunning", is_running)

    def start_stop_update(self):
        if self.is_running:
            self.is_running = False
            self.start_stop_button.setText("开始")
            self.stop_update()
        else:
            self.is_running = True
            self.start_stop_button.setText("暂停")
            self.start_update()

    def start_update(self):
        self.interval = TIME_OPTIONS[self.interval_combo.currentText()]
        self.wallpaper_updater.interval = self.interval
        self.wallpaper_updater.use_online = self.use_online_image
        self.wallpaper_updater.running = self.is_running
        self.save_settings(self.interval, self.use_online_image, self.is_running)
        if self.is_running:
            self.wallpaper_updater.start()

    def stop_update(self):
        self.wallpaper_updater.running = self.is_running
        self.save_settings(self.interval, self.use_online_image, self.is_running)

    def start_clean(self):
        self.use_online_image = self.use_online_checkbox.isChecked()
        self.save_settings(self.interval, self.use_online_image, self.is_running)
        if self.use_online_image:
            self.clean_up_regularly.use_online = self.use_online_image
            self.clean_up_regularly.start()
        else:
            self.clean_up_regularly.use_online = self.use_online_image


    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()
        elif reason == QSystemTrayIcon.Context:
            self.tray_menu.show()

    def on_auto_start_checkbox_state_changed(self):
        if self.auto_start is not True:
            app_path = sys.executable
            winreg.SetValueEx(key, "WallpaperUpdater", 0, winreg.REG_SZ, app_path)
            self.auto_start = True
        else:
            winreg.DeleteValue(key, "WallpaperUpdater")
            self.auto_start = False

    def check_auto_start_key_exist(self):
        try:
            value = winreg.QueryValueEx(key, "WallpaperUpdater")
            if value is not None:
                self.auto_start = True
        except FileNotFoundError:
            self.auto_start = False
        return self.auto_start

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("自动更新壁纸", "已最小化到系统托盘")

    def find_interval_str(self):
       for key,val in TIME_OPTIONS.items():
           if val == self.interval:
               return key
       return None


    def create_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        self.layout.setAlignment(Qt.AlignCenter)

        info_label = QLabel("请选择壁纸更新间隔和图片来源", self)
        self.layout.addWidget(info_label)

        interval_label = QLabel("间隔时间:", self)
        self.layout.addWidget(interval_label)

        self.interval_combo = QComboBox(self)
        self.interval_combo.addItems(TIME_OPTIONS.keys())
        self.interval_combo.setCurrentText(self.find_interval_str())
        self.layout.addWidget(self.interval_combo)

        self.use_online_checkbox = QCheckBox("使用在线图片", self)
        self.use_online_checkbox.setChecked(self.use_online_image)
        self.layout.addWidget(self.use_online_checkbox)
        self.use_online_checkbox.stateChanged.connect(self.start_clean)

        self.start_stop_button = QPushButton(("开始","暂停")[self.is_running is True], self)
        self.layout.addWidget(self.start_stop_button)
        self.start_stop_button.clicked.connect(self.start_stop_update)

        self.auto_start_checkbox = QCheckBox("开机自启动", self)
        self.layout.addWidget(self.auto_start_checkbox)
        self.auto_start_checkbox.setChecked(self.check_auto_start_key_exist())
        self.auto_start_checkbox.stateChanged.connect(self.on_auto_start_checkbox_state_changed)

        self.setWindowIcon(QIcon(resource_path("resource/icon/umbrella-outline.png")))

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(resource_path("resource/icon/umbrella-outline.png")))
        self.tray_icon.setToolTip("自动更新壁纸")
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        self.tray_menu = QMenu(self)
        self.restore_action = QAction("还原", self)
        self.restore_action.triggered.connect(self.showNormal)
        self.tray_menu.addAction(self.restore_action)

        self.quit_action = QAction("退出", self)
        self.quit_action.triggered.connect(close_and_exit)
        self.tray_menu.addAction(self.quit_action)

        self.tray_icon.setContextMenu(self.tray_menu)

        log.info("UI Initialization successfully")

