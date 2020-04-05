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
from BearCat2.settings import DOWNLOAD_TIMEOUT


# logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


class Ip3366Spider(scrapy.Spider):
    pool_redis = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS,
                                      decode_responses=True,
                                      max_connections=REDIS_MAXCONNECTIONS,
                                      socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
    r = redis.Redis(connection_pool=pool_redis)
    pool = threadpool.ThreadPool(THREADPOOL)
    name = 'ip3366'
    allowed_domains = ['www.ip3366.net/free/']

    def start_requests(self):
        while True:
            for num in range(1, 8):
                url = (f'http://www.ip3366.net/free/?stype=1&page={num}')
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print(f'{self.name}抓取代理成功')
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
        def hailiangip():
            try:
                hailiangip = {'http': 'http://' + proxy}
                response = requests.get(url='http://www.hailiangip.com/freeAgency/1', headers=VERIFICATION_HEADERS,
                                        proxies=hailiangip,
                                        timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'hailiangip代理:{proxy}入库')
                    self.r.sadd('hailiangip', proxy)
                    self.r.expire('hailiangip', 600)
            except:
                pass

        def jisu():
            try:
                jisu = {'http': 'http://' + proxy}
                response = requests.get(url='http://www.superfastip.com/welcome/freeip/', headers=VERIFICATION_HEADERS,
                                        proxies=jisu,
                                        timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'jisu代理:{proxy}入库')
                    self.r.sadd('jisu', proxy)
                    self.r.expire('jisu', 600)
            except:
                pass

        def xsdaili():
            try:
                xsdaili = {'http': 'http://' + proxy}
                response = requests.get(url='http://www.xsdaili.com/', headers=VERIFICATION_HEADERS, proxies=xsdaili,
                                        timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'xsdaili代理:{proxy}入库')
                    self.r.sadd('xsdaili', proxy)
                    self.r.expire('xsdaili', 600)
            except:
                pass

        def ihuan():
            try:
                ihuan = {'http': 'http://' + proxy}
                response = requests.get(url='http://ip.ihuan.me/', headers=VERIFICATION_HEADERS, proxies=ihuan,
                                        timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'ihuan代理:{proxy}入库')
                    self.r.sadd('ihuan', proxy)
                    self.r.expire('ihuan', 600)
            except:
                pass

        def a66ip():
            try:
                a66ip = {'https': 'https://' + proxy}
                response = requests.get(url='http://www.66ip.cn/1.html', headers=VERIFICATION_HEADERS, proxies=a66ip,
                                        timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'a66ip代理:{proxy}入库')
                    self.r.sadd('a66ip', proxy)
                    self.r.expire('a66ip', 600)
            except:
                pass

        def xici():
            try:
                xici = {'https': 'https://' + proxy}
                response = requests.get(url='https://www.xicidaili.com/nn/', headers=VERIFICATION_HEADERS, proxies=xici,
                                        timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'西刺代理:{proxy}入库')
                    self.r.sadd('xici', proxy)
                    self.r.expire('xici', 600)
            except:
                pass

        def xila():
            try:
                xila = {'http': 'http://' + proxy}
                response = requests.get(url='http://www.xiladaili.com/gaoni/', headers=VERIFICATION_HEADERS,
                                        proxies=xila,
                                        timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'西拉代理:{proxy}入库')
                    self.r.sadd('xila', proxy)
                    self.r.expire('xila', 600)
            except:
                pass

        def nima():
            try:
                nima = {'http': 'http://' + proxy}
                response = requests.get(url='http://www.nimadaili.com/gaoni/', headers=VERIFICATION_HEADERS,
                                        proxies=nima,
                                        timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'尼玛代理:{proxy}入库')
                    self.r.sadd('nima', proxy)
                    self.r.expire('nima', 600)
            except:
                pass

        def kuai():
            try:
                kuai = {'https': 'https://' + proxy}
                response = requests.get(url='https://www.kuaidaili.com/free/inha/', headers=VERIFICATION_HEADERS,
                                        proxies=kuai,
                                        timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'快代理:{proxy}入库')
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
                                        timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'免费代理:{proxy}入库')
                    self.r.sadd('jiangxianli', proxy)
                    self.r.expire('jiangxianli', 600)
            except:
                pass

        def ip3366():
            try:
                ip3366 = {'http': 'http://' + proxy}
                response = requests.get(url='http://www.ip3366.net/free/?stype=1&page=1', headers=VERIFICATION_HEADERS,
                                        proxies=ip3366,
                                        timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'ip3366代理:{proxy}入库')
                    self.r.sadd('ip3366', proxy)
                    self.r.expire('ip3366', 600)
            except:
                pass

        hailiangip = threading.Thread(target=hailiangip)
        jisu = threading.Thread(target=jisu)
        xsdaili = threading.Thread(target=xsdaili)
        ihuan = threading.Thread(target=ihuan)
        xici = threading.Thread(target=xici)
        xila = threading.Thread(target=xila)
        nima = threading.Thread(target=nima)
        kuai = threading.Thread(target=kuai)
        jiangxianli = threading.Thread(target=jiangxianli)
        ip3366 = threading.Thread(target=ip3366)
        a66ip = threading.Thread(target=a66ip)
        thread = [xici, xila, nima, kuai, jiangxianli, ip3366, a66ip, ihuan, xsdaili, jisu, hailiangip]
        for i in thread:
            i.start()
            i.join()
        if PROXIES_MOD == 'HTTPS':
            proxies = {'https': 'https://' + proxy}
            error = 0
            while True:
                try:
                    response = requests.get(url=VERIFICATION_URL, headers=VERIFICATION_HEADERS, proxies=proxies,
                                            timeout=DOWNLOAD_TIMEOUT)
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
                                            timeout=DOWNLOAD_TIMEOUT)
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
