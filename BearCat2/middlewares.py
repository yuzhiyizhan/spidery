# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import re
from time import strftime, localtime
from scrapy import signals
from faker import Faker
import redis
from BearCat2.settings import REDIS_HOST
from BearCat2.settings import REDIS_PORT
from BearCat2.settings import REDIS_PARAMS
from BearCat2.settings import REDIS_DB
from BearCat2.settings import REDIS_MAXCONNECTIONS
from BearCat2.settings import REDIS_CONNECT_TIMEOUT

pool_redis = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS,
                                  decode_responses=True,
                                  max_connections=REDIS_MAXCONNECTIONS,
                                  socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
r = redis.Redis(connection_pool=pool_redis)


class Bearcat2SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Bearcat2DownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HttpRequeseSpiderMiddleware(object):
    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        print(exception)


class UserAgentDownloadMiddleware(object):
    def process_request(self, request, spider):
        user_agent = Faker().user_agent()
        request.headers['User-Agent'] = user_agent
        # if 'https' in request.url:
        #     if r.scard('https') > 0:
        #         request.meta['proxy'] = 'https://' + r.srandmember('https')
        # else:
        #     if r.scard('http') > 0:
        #         request.meta['proxy'] = 'http://' + r.srandmember('https')

    def process_response(self, request, response, spider):

        if response.status != 200:
            print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'请求失败网址:{response.url}响应码:{request.status}')
        if response.status == 200:
            print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'请求成功网址为:{response.url}')
            return response

    def process_exception(self, request, exception, spider):
        try:
            p = re.split('//', request.meta['proxy'])[1]
            r.srem(f'{spider.name}', p)
        except:
            pass
        print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'请求失败错误信息为:{exception}')
        print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'请求失败网址为:{request.url}')
        if r.scard(f'{spider.name}') > 0:
            proxies = r.srandmember(f'{spider.name}')
            if spider.name == 'xici' or 'kuai' or 'jiangxianli':
                request.meta['proxy'] = 'https://' + proxies
                print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'\033[1;31;40m准备重试:{request.url}\033[0m')
                return request
            else:
                request.meta['proxy'] = 'http://' + proxies
                print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'\033[1;31;40m准备重试:{request.url}\033[0m')
                return request
        # if 'https' in request.url:
        #     if r.scard('https') > 0:
        #         proxies = requests.get(url='http://127.0.0.1:5555/https').text
        #         request.meta['proxy'] = 'https://' + proxies
        #         print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'\033[1;31;40m准备重试:{request.url}\033[0m')
        #         return request
        # else:
        #     if r.scard('http') > 0:
        #         proxies = requests.get(url='http://127.0.0.1:5555/http').text
        #         request.meta['proxy'] = 'http://' + proxies
        #         print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'\033[1;31;40m准备重试:{request.url}\033[0m')
        #         return request
