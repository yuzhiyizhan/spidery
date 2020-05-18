# -*- coding: utf-8 -*-
import re
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


class XsdailiSpider(scrapy.Spider):
    pool_redis = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS,
                                      decode_responses=True,
                                      max_connections=REDIS_MAXCONNECTIONS,
                                      socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
    r = redis.Redis(connection_pool=pool_redis)
    pool = threadpool.ThreadPool(THREADPOOL)
    name = 'xsdaili'
    allowed_domains = ['www.xsdaili.com']
    start_urls = ['http://www.xsdaili.com/']

    def parse(self, response):
        urls = response.xpath('//div[@class="title"]/a/@href').getall()
        for i in urls:
            url = response.urljoin(i)
            if url:
                yield scrapy.Request(url=url, callback=self.parse_next, dont_filter=True)
            else:
                yield scrapy.Request(url='http://www.xsdaili.com/', callback=self.parse_next, dont_filter=True)

    def parse_next(self, response):
        log(f'{self.name}抓取代理成功')
        proxies_list = re.findall(r'(?:(?:[0,1]?\d?\d|2[0-4]\d|25[0-5])\.){3}(?:[0,1]?\d?\d|2[0-4]\d|25[0-5])',
                                  response.text)
        proxies_lists = [[self.name, i] for i in proxies_list]
        theading = threadpool.makeRequests(parse_pool, proxies_lists)
        for i in theading:
            self.pool.putRequest(i)
        self.pool.wait()
