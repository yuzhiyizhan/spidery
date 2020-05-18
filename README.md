1.先进行配置:
    到BearCat2.settings.py设置如下:
    
    爬取延迟
    
    DOWNLOAD_DELAY = 2
    
    爬取目标网站(验证的网站)
    
    VERIFICATION_URL = 'https://www.baidu.com'
    
    爬取目标使用的请求头(根据需要修改)
    
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
    
    REDIS_DB = 1
    
    redis最大连接数
    
    REDIS_MAXCONNECTIONS = 100
    
    redis超时时间
    
    REDIS_CONNECT_TIMEOUT = 1


​    
2.安装依赖:

    cd 到项目目录BearCat2
    
    pip3 install -r requirements.txt -i https://pypi.douban.com/simple/
    
    pip3 install --upgrade -r requirements.txt -i https://pypi.douban.com/simple/


​    
3.安装数据库

    安装(linux)
    
    第一种:下载，解压，编译Redis
    
    $ wget http://download.redis.io/releases/redis-5.0.5.tar.gz
    
    $ tar xzf redis-5.0.5.tar.gz
    
    $ cd redis-5.0.5
    
    $ make
    
    进入到解压后的 src 目录，通过如下命令启动Redis：
    
    $ src/redis-server
    
    您可以使用内置的客户端与Redis进行互动：
    
    $ src/redis-cli
    
    第二种:
    ubuntu
    sudo apt-get install redis
    redis-server
    
    manjaro
    sudo pacman -S redis
    redis-server
    
    windows
    
    下载地址
    https://github.com/microsoftarchive/redis/releases
    安装过程自行百度(其实就是解压后点redis-server)


4.给cmd_APl.py执行权限(不需要)

    sudo chmod +x cmd_APl.py
    
    python3 cmd_APl.py


5.启动cmd_APl.py(注意可能是python cmd_API.py)

    python3 cmd_APl.py


6.启动runall.py(注意可能是python runall.py)

    python3 runall.py


​    
7.windowns启动

    与linux一样


​    
8.可在web查看可用代理数量

    查看https代理:
    
    http://127.0.0.1:5555/count/https
    
    查看http代理:
    
    http://127.0.0.1:5555/count/http
    
    随机取出https代理:
    
    http://127.0.0.1:5555/https
    
    随机取出http代理:
    
    http://127.0.0.1:5555/http

9.添加端口在cmd_APl.py


10.过一会便能看到可用代理

    ps:这个不想关,不然太无聊了


​    
11.加代理方法

    cd进入BearCat2.spiders
    
    scrapy genspider [爬虫名] [爬虫的域名]
    
    爬虫名不可与之前的重复


​    
12.添加代理的方法

    参考任一爬虫

以下是参考例子

```
# -*- coding: utf-8 -*-
import redis
import scrapy
import threadpool
from BearCat2.LOG import log
from BearCat2.settings import REDIS_DB
from BearCat2.settings import REDIS_HOST
from BearCat2.settings import REDIS_PORT
from BearCat2.settings import THREADPOOL
from BearCat2.settings import REDIS_PARAMS
from BearCat2.settings import REDIS_MAXCONNECTIONS
from BearCat2.settings import REDIS_CONNECT_TIMEOUT
from BearCat2.Commom import parse_pool


class A66ipSpider(scrapy.Spider):
    pool_redis = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS,
                                      decode_responses=True,
                                      max_connections=REDIS_MAXCONNECTIONS,
                                      socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
    r = redis.Redis(connection_pool=pool_redis)
    pool = threadpool.ThreadPool(THREADPOOL)
    name = 'a66ip'
    allowed_domains = ['www.66ip.cn/']

    # start_urls = ['http://www.66ip.cn/']
    def start_requests(self):
        for num in range(1, 11):
            url = (f'http://www.66ip.cn/{num}.html')
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        log(f'{self.name}抓取代理成功')
        proxies_list = []
        proxy = response.xpath('//tr')[1:]
        for i in proxy:
            http = i.xpath('./td/text()')[3].get()
            if '高匿' in http:
                ip = i.xpath('./td/text()')[0].get()
                host = i.xpath('./td/text()')[1].get()
                save = ip, host
                proxies = save[0] + ':' + save[1]
                proxies_list.append(proxies)
        proxies_lists = [[self.name, i] for i in proxies_list]
        theading = threadpool.makeRequests(parse_pool, proxies_lists)
        for i in theading:
            self.pool.putRequest(i)
        self.pool.wait()
```

在Confs添加爬虫名即可