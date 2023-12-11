from wallwapper.MainWindow import run
from wallwapper.LogConfig import logger as log

if __name__ == "__main__":
    try:
        log.info("start...")
        run()
        log.info("end...")
    except Exception as e:
        log.error(e)