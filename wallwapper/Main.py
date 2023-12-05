import os
import sys
from wallwapper.MainWindow import run
from wallwapper.LogConfig import logger as log

def main():
    # sys.args[0]获取文件的真实路径，其他方法获取的会是cmd的路径
    path = sys.argv[0]
    # 获取工作目录
    work_path = os.path.dirname(path)
    # 切换工作目录，不切换执行程序.exe的目录还是cmd的路径
    os.chdir(work_path)
    #运行程序
    run()

if __name__ == "__main__":
    try:
        log.info("start...")
        main()
        log.info("end...")
    except Exception as e:
        log.error(e)