import time
from loguru import logger

<<<<<<< HEAD
logger.level("PASS", no=38, color="<green>")
=======
gger.level("PASS", no=38, color="<green>")
>>>>>>> a20685c0e20555a8cf1e9f98dd41d009298ce447

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
<<<<<<< HEAD
        raise Exception("log函数没设置布尔值或DEBUG")
=======
        raise Exception("log函数没设置布尔值或INFO")
>>>>>>> a20685c0e20555a8cf1e9f98dd41d009298ce447
