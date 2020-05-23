import time
from loguru import logger


def log(prints, Boolean=True):
    if Boolean == True:
        try:
            logger.level("PASS", no=38, color="<green>", icon="🐍")
            logger.log("PASS", str(prints))
        except:
            print(f"\033[0;32;40m{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m",
                  "\033[0;32;40mPASS\033[0m", f"\033[0;32;40m{prints}\033[0m")

    elif Boolean == False:
        try:
            logger.level("FALSE", no=38, color="<red>", icon="🐍")
            logger.log("FALSE", str(prints))
        except:
            print(f"\033[0;32;40m{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m",
                  "\033[0;31;40mFALSE\033[0m", f"\033[0;31;40m{prints}\033[0m")

    elif Boolean == "INFO":
        try:
            logger.level("INFO", no=38, color="<blue>", icon="")
            logger.log("INFO", str(prints))
        except:
            print(f"\033[0;32;40m{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m",
                  "\033[0;34;40mINFO\033[0m", f"\033[0;34;40m{prints}\033[0m")

    else:
        raise "log函数没设置布尔值或INFO"
