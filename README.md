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
    
    
7.windowns启动

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
    
9.添加端口在cmd_APl.py


10.过一会便能看到可用代理

    ps:这个不想关,不然太无聊了
    
    
11.加代理方法

    cd进入BearCat2.spiders
    
    scrapy genspider [爬虫名] [爬虫的域名]
    
    爬虫名不可与之前的重复
    
    
12.添加代理的方法

    参考任一爬虫

run.sh 新增爬虫启动的命令(还未解决同时启动爬虫实际只能启动2个的问题)

以下是参考例子

import requests

url = 'https://www.baidu.com'

headers = {}

proxy = requests.get(url='http://127.0.0.1:5555/https')

proxies = {'https':f'https://{proxy}'}

response = requests.get(url=url, headers=headers, proxies=proxies)
