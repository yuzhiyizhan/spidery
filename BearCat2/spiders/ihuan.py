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

class IhuanSpider(scrapy.Spider):
    pool_redis = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS,
                                      decode_responses=True,
                                      max_connections=REDIS_MAXCONNECTIONS,
                                      socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
    r = redis.Redis(connection_pool=pool_redis)
    name = 'ihuan'
    allowed_domains = ['ip.ihuan.me/']
    start_urls = ['http://ip.ihuan.me/']

    def parse(self, response):
        log(f'{self.name}抓取代理成功', 'DEBUG')
        proxies_list = []
        proxy = response.xpath('//tr')[1:]
        urls = response.xpath('//ul[@class="pagination"]/li/a/@href').getall()[-1]
        url = response.urljoin(urls)
        for i in proxy:
            http = i.xpath('./td/a/text()').getall()[-1]
            if '高匿' in http:
                ip = i.xpath('./td/a/text()').get()
                host = i.xpath('./td/text()').get()
                save = ip, host
                proxies = save[0] + ':' + save[1]
                proxies_list.append(proxies)
        proxies_list = [[self.name, i] for i in proxies_list]
        with ThreadPoolExecutor(max_workers=THREADPOOL) as t:
            for i in proxies_list:
                t.submit(parse_pool, i)
        if urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
        else:
            yield scrapy.Request(url='http://ip.ihuan.me/', callback=self.parse, dont_filter=True)
