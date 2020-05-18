# -*- coding: utf-8 -*-
import redis
import requests
from BearCat2.LOG import log
from BearCat2.settings import REDIS_DB
from BearCat2.settings import REDIS_HOST
from BearCat2.settings import REDIS_PORT
from BearCat2.settings import PROXIES_MOD
from BearCat2.settings import REDIS_PARAMS
from BearCat2.settings import REDIS_TIMEOUT
from BearCat2.settings import VERIFICATION_URL
from BearCat2.settings import DOWNLOAD_TIMEOUT
from BearCat2.settings import VERIFICATION_HEADERS
from BearCat2.settings import REDIS_MAXCONNECTIONS
from BearCat2.settings import REDIS_CONNECT_TIMEOUT

pool_redis = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS,
                                  decode_responses=True,
                                  max_connections=REDIS_MAXCONNECTIONS,
                                  socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
r = redis.Redis(connection_pool=pool_redis)


def parse_pool(proxy):
    if PROXIES_MOD == 'HTTPS':
        proxies = {'https': 'https://' + proxy[1]}
        error = 0
        while True:
            try:
                response = requests.get(url=VERIFICATION_URL, headers=VERIFICATION_HEADERS, proxies=proxies,
                                        timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    log(f"可用ip:{proxy[1]}重试过{error}次,代理来自{proxy[0]}")
                    r.sadd('https', proxy[1])
                    if type(REDIS_TIMEOUT) == int:
                        r.exists('https', REDIS_TIMEOUT)
                    break
            except:
                error = error + 1
                if error > 3:
                    log(f'无效ip:{proxy[1]}', False)
                    break
                else:
                    log(f'重试ip{error}次:{proxy[1]}', "INFO")
                    continue
    if PROXIES_MOD == 'HTTP':
        proxies = {'http': 'http://' + proxy[1]}
        error = 0
        while True:
            try:
                response = requests.get(url=VERIFICATION_URL, headers=VERIFICATION_HEADERS, proxies=proxies,
                                        timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    log(f"可用ip:{proxy[1]}重试过{error}次,代理来自{proxy[0]}")
                    r.sadd('http', proxy[1])
                    if type(REDIS_TIMEOUT) == int:
                        r.exists('http', REDIS_TIMEOUT)
                    break
            except:
                error = error + 1
            if error > 3:
                log(f'无效ip:{proxy[1]}', False)
                break
            else:
                log(f'重试ip{error}次:{proxy[1]}', "INFO")
                continue
