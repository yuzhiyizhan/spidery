import time
from loguru import logger

logger.level("PASS", no=38, color="<green>")

def log(prints, Boolean=True):
    if Boolean == True:
        try:
            logger.log("PASS", str(prints))
        except:
            print(f"\033[0;32;40m{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m",
                  "\033[0;32;40mPASS\033[0m", f"\033[0;32;40m{prints}\033[0m")

    elif Boolean == False:
        try:
            logger.error(str(prints))
        except:
            print(f"\033[0;32;40m{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m",
                  "\033[0;31;40mFALSE\033[0m", f"\033[0;31;40m{prints}\033[0m")

    elif Boolean == "DEBUG":
        try:
            logger.debug(str(prints))
        except:
            print(f"\033[0;32;40m{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m",
                  "\033[0;34;40mINFO\033[0m", f"\033[0;34;40m{prints}\033[0m")

    else:
        raise Exception("log函数没设置布尔值或DEBUG")
