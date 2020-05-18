import time
from scrapy import cmdline
from multiprocessing import Process


def start_blspider(spider_name, frequency):
    args = ['scrapy', 'crawl', spider_name]
    while True:
        p = Process(target=cmdline.execute, args=(args,))
        p.start()
        p.join()
        time.sleep(frequency)
