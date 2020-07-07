import time
import redis
import requests
import threadpool
from Commom.LOG import log
from BearCat2.settings import REDIS_DB
from BearCat2.settings import REDIS_HOST
from BearCat2.settings import REDIS_PORT
from BearCat2.settings import THREADPOOL
from BearCat2.settings import PROXIES_MOD
from BearCat2.settings import VERIFY_TIME
from BearCat2.settings import REDIS_PARAMS
from BearCat2.settings import VERIFICATION_URL
from BearCat2.settings import VERIFICATION_HEADERS
from BearCat2.settings import REDIS_MAXCONNECTIONS
from BearCat2.settings import REDIS_CONNECT_TIMEOUT

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS, decode_responses=True,
                            max_connections=REDIS_MAXCONNECTIONS, socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
r = redis.Redis(connection_pool=pool)
pool = threadpool.ThreadPool(THREADPOOL)


def parse_pool(proxy):
    if PROXIES_MOD == 'HTTPS':
        proxies = {'https': 'https://' + proxy}
        error = 0
        while True:
            try:
                response = requests.get(url=VERIFICATION_URL, headers=VERIFICATION_HEADERS, proxies=proxies,
                                        timeout=2)
                if response.status_code == 200:
                    log(f'可用ip:{proxy}重试过{error}次')
                    r.sadd('https', proxy)
                    break
            except:
                error = error + 1
                if error > 3:
                    log(f'删除ip:{proxy}', False)
                    requests.get(url=f'http://127.0.0.1:5555/deletes?delete={proxy}')
                    break
                else:
                    log(f'重试ip{error}次:{proxy}', "DEBUG")
                    continue
    if PROXIES_MOD == 'HTTP':
        proxies = {'http': 'http://' + proxy}
        error = 0
        while True:
            try:
                response = requests.get(url=VERIFICATION_URL, headers=VERIFICATION_HEADERS, proxies=proxies,
                                        timeout=2)
                if response.status_code == 200:
                    log(f'可用ip:{proxy}重试过{error}次')
                    r.sadd('http', proxy)
                    break
            except:
                error = error + 1
            if error > 3:
                log(f'删除ip:{proxy}', False)
                requests.get(url=f'http://127.0.0.1:5555/delete?delete={proxy}')
                break
            else:
                log(f'重试ip{error}次:{proxy}', "DEBUG")
                continue


def verify():
    while True:
        if PROXIES_MOD == 'HTTPS':
            if r.scard('https') == 0:
                continue
            proxy_list = r.srandmember('https', r.scard('https'))
            theading = threadpool.makeRequests(parse_pool, proxy_list)
            for i in theading:
                pool.putRequest(i)
            pool.wait()
            time.sleep(VERIFY_TIME)

        if PROXIES_MOD == 'HTTP':
            if r.scard('http') == 0:
                continue
            proxy_list = r.srandmember('http', r.scard('http'))
            theading = threadpool.makeRequests(parse_pool, proxy_list)
            for i in theading:
                pool.putRequest(i)
            pool.wait()
            time.sleep(VERIFY_TIME)



