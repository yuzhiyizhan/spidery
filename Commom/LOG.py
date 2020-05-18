from loguru import logger


def log(prints, Boolean=True):
    if Boolean == True:
        logger.level("PASS", no=38, color="<green>", icon="🐍")
        logger.log("PASS", str(prints))

    elif Boolean == False:
        logger.level("FALSE", no=38, color="<red>", icon="🐍")
        logger.log("FALSE", str(prints))

    elif Boolean == "INFO":
        logger.level("INFO", no=38, color="<blue>", icon="")
        logger.log("INFO", str(prints))

    else:
        raise "log函数没设置布尔值或INFO"
