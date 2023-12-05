import logging
import os
from logging.handlers import *

def setup_logging(filename='log/run.log', level=logging.INFO):
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

logger = setup_logging()

