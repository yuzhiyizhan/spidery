# -*- coding: utf-8 -*-
import redis
import scrapy
from Commom.LOG import log
from Commom.Parse_pool import parse_pool
from BearCat2.settings import REDIS_DB
from BearCat2.settings import REDIS_HOST
from BearCat2.settings import REDIS_PORT
from BearCat2.settings import THREADPOOL
from BearCat2.settings import REDIS_PARAMS
from BearCat2.settings import REDIS_MAXCONNECTIONS
from BearCat2.settings import REDIS_CONNECT_TIMEOUT
from concurrent.futures import ThreadPoolExecutor

class JisuSpider(scrapy.Spider):
    pool_redis = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS,
                                      decode_responses=True,
                                      max_connections=REDIS_MAXCONNECTIONS,
                                      socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
    r = redis.Redis(connection_pool=pool_redis)
    name = 'jisu'
    allowed_domains = ['www.superfastip.com/welcome/freeip']

    def start_requests(self):
        for num in range(1, 11):
            url = (f'http://www.superfastip.com/welcome/freeip/{num}')
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        log(f'{self.name}抓取代理成功', 'DEBUG')
        proxies_list = []
        proxy = response.xpath('//tr')[5:]
        for i in proxy:
            ip = i.xpath('./td/text()').get()
            host = i.xpath('./td/text()')[1].get()
            save = ip, host
            proxies = save[0] + ':' + save[1]
            proxies_list.append(proxies)
        proxies_list = [[self.name, i] for i in proxies_list]
        with ThreadPoolExecutor(max_workers=THREADPOOL) as t:
            for i in proxies_list:
                t.submit(parse_pool, i)
