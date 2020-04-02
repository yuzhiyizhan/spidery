# -*- coding: utf-8 -*-
from time import strftime, localtime
import threading
import scrapy
import threadpool
import redis
import requests
from BearCat2.settings import VERIFICATION_URL
from BearCat2.settings import VERIFICATION_HEADERS
from BearCat2.settings import PROXIES_MOD
from BearCat2.settings import REDIS_HOST
from BearCat2.settings import REDIS_PORT
from BearCat2.settings import REDIS_PARAMS
from BearCat2.settings import REDIS_DB
from BearCat2.settings import REDIS_MAXCONNECTIONS
from BearCat2.settings import REDIS_CONNECT_TIMEOUT
from BearCat2.settings import THREADPOOL


# logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


class JiangxianliSpider(scrapy.Spider):
    pool_redis = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS,
                                      decode_responses=True,
                                      max_connections=REDIS_MAXCONNECTIONS,
                                      socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
    r = redis.Redis(connection_pool=pool_redis)
    pool = threadpool.ThreadPool(THREADPOOL)
    name = 'jiangxianli'

    # allowed_domains = ['ip.jiangxianli.com/?page=2']
    def start_requests(self):
        while True:
            for num in range(1, 8):
                url = (f'https://ip.jiangxianli.com/?page={num}&anonymity=2')
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print('免费代理有启动')
        proxies_list = []
        proxy = response.xpath('//tr')[1:]
        for i in proxy:
            http = i.xpath('./td/text()')[2].get()
            if '高匿' in http:
                ip = i.xpath('./td/text()')[0].get()
                host = i.xpath('./td/text()')[1].get()
                save = ip, host
                proxies = save[0] + ':' + save[1]
                proxies_list.append(proxies)
        theading = threadpool.makeRequests(self.parse_pool, proxies_list)
        for i in theading:
            self.pool.putRequest(i)
        self.pool.wait()

    def parse_pool(self, proxy):
        def xici():
            try:
                xici = {'https': 'https://' + proxy}
                response = requests.get(url='https://www.xicidaili.com/nn/', headers=VERIFICATION_HEADERS, proxies=xici,
                                        timeout=2)
                if response.status_code == 200:
                    print(f'西刺代理:{proxy}入库')
                    self.r.sadd('xici', proxy)
                    self.r.expire('xici', 600)
            except:
                pass

        def xila():
            try:
                xila = {'http': 'http://' + proxy}
                response = requests.get(url='http://www.xiladaili.com/gaoni/', headers=VERIFICATION_HEADERS,
                                        proxies=xila,
                                        timeout=2)
                if response.status_code == 200:
                    print(f'西拉代理:{proxy}入库')
                    self.r.sadd('xila', proxy)
                    self.r.expire('xila', 600)
            except:
                pass

        def nima():
            try:
                nima = {'http': 'http://' + proxy}
                response = requests.get(url='http://www.nimadaili.com/gaoni/', headers=VERIFICATION_HEADERS,
                                        proxies=nima,
                                        timeout=2)
                if response.status_code == 200:
                    print(f'尼玛代理:{proxy}入库')
                    self.r.sadd('nima', proxy)
                    self.r.expire('nima', 600)
            except:
                pass

        def kuai():
            try:
                kuai = {'https': 'https://' + proxy}
                response = requests.get(url='https://www.kuaidaili.com/free/inha/', headers=VERIFICATION_HEADERS,
                                        proxies=kuai,
                                        timeout=2)
                if response.status_code == 200:
                    print(f'快代理:{proxy}入库')
                    self.r.sadd('kuai', proxy)
                    self.r.expire('kuai', 600)
            except:
                pass

        def jiangxianli():
            try:
                jiangxianli = {'https': 'https://' + proxy}
                response = requests.get(url='https://ip.jiangxianli.com/?page=1&anonymity=2',
                                        headers=VERIFICATION_HEADERS,
                                        proxies=jiangxianli,
                                        timeout=2)
                if response.status_code == 200:
                    print(f'免费代理:{proxy}入库')
                    self.r.sadd('jiangxianli', proxy)
                    self.r.expire('jiangxianli', 600)
            except:
                pass

        def ip3366():
            try:
                ip3366 = {'http': 'http://' + proxy}
                response = requests.get(url='http://www.ip3366.net/free/?stype=1&page=1', headers=VERIFICATION_HEADERS,
                                        proxies=ip3366,
                                        timeout=2)
                if response.status_code == 200:
                    print(f'ip3366代理:{proxy}入库')
                    self.r.sadd('ip3366', proxy)
                    self.r.expire('ip3366', 600)
            except:
                pass

        xici = threading.Thread(target=xici)
        xila = threading.Thread(target=xila)
        nima = threading.Thread(target=nima)
        kuai = threading.Thread(target=kuai)
        jiangxianli = threading.Thread(target=jiangxianli)
        ip3366 = threading.Thread(target=ip3366)
        thread = [xici, xila, nima, kuai, jiangxianli, ip3366]
        for i in thread:
            i.start()
        if PROXIES_MOD == 'HTTPS':
            proxies = {'https': 'https://' + proxy}
            error = 0
            while True:
                try:
                    response = requests.get(url=VERIFICATION_URL, headers=VERIFICATION_HEADERS, proxies=proxies,
                                            timeout=2)
                    if response.status_code == 200:
                        print(strftime("%Y-%m-%d %H:%M:%S", localtime()),
                              f'\033[1;32;40m可用ip:{proxy}重试过{error}次,代理来自{self.name}\033[0m')
                        self.r.sadd('https', proxy)
                        break
                except:
                    error = error + 1
                    if error > 3:
                        print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'无效ip:{proxy}')
                        break
                    else:
                        print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'重试ip{error}次:{proxy}')
                        continue
        if PROXIES_MOD == 'HTTP':
            proxies = {'http': 'http://' + proxy}
            error = 0
            while True:
                try:
                    response = requests.get(url=VERIFICATION_URL, headers=VERIFICATION_HEADERS, proxies=proxies,
                                            timeout=2)
                    if response.status_code == 200:
                        print(strftime("%Y-%m-%d %H:%M:%S", localtime()),
                              f'\033[1;32;40m可用ip:{proxy}重试过{error}次,代理来自{self.name}\033[0m')
                        self.r.sadd('http', proxy)
                        break
                except:
                    error = error + 1
                if error > 3:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'无效ip:{proxy}')
                    break
                else:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'重试ip{error}次:{proxy}')
                    continue
