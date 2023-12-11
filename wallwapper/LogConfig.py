import logging
import os
import sys
from logging.handlers import *

def setup_logging(filename='log/run.log', level=logging.INFO):
    setting_workdir()
    """
    设置日志格式
    :param filename: 日志文件名
    :param level: 日志级别
    :return:
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s %(levelname)-5.5s [%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 设置日志轮转
    timed_handler = TimedRotatingFileHandler(filename, when='midnight', interval=1, backupCount=7)
    timed_handler.setFormatter(formatter)
    logger.addHandler(timed_handler)
    return logger

def setting_workdir():
    # sys.args[0]获取文件的真实路径，其他方法获取的会是cmd的路径
    path = sys.argv[0]
    # 获取工作目录
    work_path = os.path.dirname(path)
    # 切换工作目录，不切换执行程序.exe的目录还是cmd的路径
    os.chdir(work_path)

logger = setup_logging()

