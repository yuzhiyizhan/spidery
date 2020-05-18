import os
import sys
import threading
from multiprocessing import Process
from Commom.Confs import confs
from Commom.Verify import verify
from Commom.spiders_all import start_blspider

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

if __name__ == '__main__':
    proces = threading.Thread(target=verify)
    proces.start()
    for conf in confs:
        process = Process(target=start_blspider, args=(conf.get('spider_name'), conf.get('frequency', 0)))
        process.start()
