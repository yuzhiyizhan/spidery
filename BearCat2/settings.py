# -*- coding: utf-8 -*-

# Scrapy settings for BearCat2 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from faker import Faker

BOT_NAME = 'BearCat2'

SPIDER_MODULES = ['BearCat2.spiders']
NEWSPIDER_MODULE = 'BearCat2.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'BearCat2 (+http://www.yourdomain.com)'
# 包括第一次下载，最多的重试次数
RETRY_TIMES = 1
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# 是否启用logging
LOG_ENABLED = False
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 100
#下载器超时时间
DOWNLOAD_TIMEOUT = 3
# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 100
# CONCURRENT_REQUESTS_PER_IP = 100

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False
# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': Faker().user_agent(),
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'BearCat2.middlewares.HttpRequeseSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'BearCat2.middlewares.UserAgentDownloadMiddleware': 543,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     # 'BearCat2.pipelines.HttpsProxiesPipeline': 300,
#     'BearCat2.pipelines.ProxiesPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# 爬取目标网站
VERIFICATION_URL = 'https://www.mzitu.com/'
# 爬取目标使用的请求头
VERIFICATION_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': Faker().user_agent(),
    'referer': 'https://www.mzitu.com/japan/',
}
# 代理类型（填HTTP或HTTPS）
PROXIES_MOD = 'HTTPS'
# redis服务配置
# redis主机名
REDIS_HOST = '127.0.0.1'
# redis端口
REDIS_PORT = '6379'
# redis密码
REDIS_PARAMS = ''
# redis db
REDIS_DB = 1
# redis最大连接数
REDIS_MAXCONNECTIONS = 100
# redis超时时间
REDIS_CONNECT_TIMEOUT = 30
# 多爬虫启动配置
COMMANDS_MODULE = 'BearCat2.commands'
# 验证模块等待多长时间验证全部代理活性
VERIFY_TIME = 600
# 验证代理线程数(越大越快,资源占用也越多)
THREADPOOL = 10
