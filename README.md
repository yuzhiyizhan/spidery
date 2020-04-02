1.先进行配置:
    到BearCat2.settings.py设置如下:
    爬取延迟
    DOWNLOAD_DELAY = 2
    爬取目标网站
    VERIFICATION_URL = 'https://www.baidu.com'
    爬取目标使用的请求头
    VERIFICATION_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'User-Agent': UserAgent().random,
    }
    代理类型
    PROXIES_MOD = 'HTTPS'
    redis服务配置
    redis主机名
    REDIS_HOST = '127.0.0.1'
    redis端口
    REDIS_PORT = '6379'
    redis密码
    REDIS_PARAMS = ''
    redis db
    REDIS_DB = 0
    redis最大连接数
    REDIS_MAXCONNECTIONS = 100
    redis超时时间
    REDIS_CONNECT_TIMEOUT = 1
    
2.安装依赖:
    cd 到项目目录BearCat2
    pip3 install -r requirements.txt -i https://pypi.douban.com/simple/
    pip3 install --upgrade -r requirements.txt -i https://pypi.douban.com/simple/
    
3.安装数据库
    安装(linux)
    下载，解压，编译Redis
    $ wget http://download.redis.io/releases/redis-5.0.5.tar.gz
    $ tar xzf redis-5.0.5.tar.gz
    $ cd redis-5.0.5
    $ make
    进入到解压后的 src 目录，通过如下命令启动Redis：
    $ src/redis-server
    您可以使用内置的客户端与Redis进行互动：
    $ src/redis-cli
    windows(请先自行百度后续会添加)
    
4.给cmd_APl.py执行权限
    sudo chmod +x cmd_APl.py
    python3 cmd_APl.py
    
5.启动cmd_APl.py
    python3 cmd_APl.py
    
6.给run.sh执行权限(linux)
    sudo chmod +x run.sh
    启动run.sh
    ./run.sh
    
7.windowns启动(测试中)
    /start run.bat
    
8.可在web查看可用代理数量
    查看https代理:
    http://127.0.0.1:5555/count/https
    查看http代理:
    http://127.0.0.1:5555/count/http
    随机取出https代理:
    http://127.0.0.1:5555/https
    随机取出http代理:
    http://127.0.0.1:5555/http
9.启动代理池
    scrapy crawlall
    
10.过一会便能看到可用代理
    ps:这个不想关,不然太无聊了
    
11.加代理方法
    cd进入BearCat2.spiders
    scrapy genspider [爬虫名] [爬虫的域名]
    爬虫名不可与之前的重复
    
# 导入库
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
# 创建爬虫类继承scrapy.Spider
class Ip3366Spider(scrapy.Spider):
    # 创建redis连接
    pool_redis = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS,
                                      decode_responses=True,
                                      max_connections=REDIS_MAXCONNECTIONS,
                                      socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
    r = redis.Redis(connection_pool=pool_redis)
    proxies = []
    pool = threadpool.ThreadPool(THREADPOOL)
    # 爬虫名不可与之前的爬虫名重复
    name = 'ip3366'
    # 限制的域名
    allowed_domains = ['www.ip3366.net/free/']
    # 初始url
    def start_requests(self):
        while True:
            for num in range(1, 8):
                url = (f'http://www.ip3366.net/free/?stype=1&page={num}')
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
    # 爬取代理逻辑
    def parse(self, response):
        proxy = response.xpath('//tr')[1:]
        for i in proxy:
            http = i.xpath('./td/text()')[2].get()
            if '高匿' in http:
                ip = i.xpath('./td/text()')[0].get()
                host = i.xpath('./td/text()')[1].get()
                save = ip, host
                proxies = save[0] + ':' + save[1]
                self.proxies.append(proxies)
        # 将代理列表放入
        theading = threadpool.makeRequests(self.parse_pool, self.proxies)
        for i in theading:
            self.pool.putRequest(i)
        self.pool.wait()
        
    # 验证逻辑
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
run.sh 新增爬虫启动的命令