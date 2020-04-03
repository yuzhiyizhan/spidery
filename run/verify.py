import time
from time import strftime, localtime
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import requests
import redis
import threadpool
from BearCat2.settings import VERIFICATION_URL
from BearCat2.settings import VERIFICATION_HEADERS
from BearCat2.settings import PROXIES_MOD
from BearCat2.settings import REDIS_HOST
from BearCat2.settings import REDIS_PORT
from BearCat2.settings import REDIS_PARAMS
from BearCat2.settings import REDIS_DB
from BearCat2.settings import REDIS_MAXCONNECTIONS
from BearCat2.settings import REDIS_CONNECT_TIMEOUT
from BearCat2.settings import VERIFY_TIME
from BearCat2.settings import THREADPOOL

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
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'\033[1;32;40m可用ip:{proxy}重试过{error}次\033[0m')
                    r.sadd('https', proxy)
                    break
            except:
                error = error + 1
                if error > 3:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'\033[1;31;40m删除ip:{proxy}\033[0m')
                    requests.get(url=f'http://127.0.0.1:5555/deletes?delete={proxy}')
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
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'\033[1;32;40m可用ip:{proxy}重试过{error}次\033[0m')
                    r.sadd('http', proxy)
                    break
            except:
                error = error + 1
            if error > 3:
                print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'\033[1;31;40m删除ip:{proxy}\033[0m')
                requests.get(url=f'http://127.0.0.1:5555/delete?delete={proxy}')
                break
            else:
                print(strftime("%Y-%m-%d %H:%M:%S", localtime()), f'重试ip{error}次:{proxy}')
                continue


def main():
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


if __name__ == '__main__':
    main()
