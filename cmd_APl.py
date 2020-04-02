'''接口模块'''
import re
import sys
import os
import redis
from flask import Flask, request
from BearCat2.settings import REDIS_HOST
from BearCat2.settings import REDIS_PORT
from BearCat2.settings import REDIS_PARAMS
from BearCat2.settings import REDIS_DB
from BearCat2.settings import REDIS_MAXCONNECTIONS
from BearCat2.settings import REDIS_CONNECT_TIMEOUT

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

app = Flask(__name__)
pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS, decode_responses=True,
                            max_connections=REDIS_MAXCONNECTIONS, socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
r = redis.Redis(connection_pool=pool)


@app.route('/api', methods=['GET'])
def helli_work():
    return 'hello'


@app.route('/', methods=['GET'])
def hello():
    return 'hello'


@app.route('/https')
def https():
    if r.scard('https') > 0:
        ip = r.srandmember('https')
    else:
        ip = '43.255.228.150:3128'
    # r.sadd('可用https',ip)
    return ip


@app.route('/http')
def http():
    if r.scard('http') > 0:
        ip = r.srandmember('http')
    else:
        ip = '43.255.228.150:3128'
    return ip


@app.route('/delete')
def dele():
    p = request.args.get('delete')
    if p == None:
        return '请指定要删除的代理'
    k = re.split('=', request.full_path)[1]
    r.srem('http', k)
    return f'已删除{k}'


@app.route('/deletes')
def deles():
    p = request.args.get('delete')
    if p == None:
        return '请指定要删除的代理'
    k = re.split('=', request.full_path)[1]
    r.srem('https', k)
    return f'已删除{k}'


@app.route('/count/https')
def counts():
    num = r.srandmember('https', r.scard('https'))
    return f'可用https数量{len(num)}'


@app.route('/count/http')
def countss():
    num = r.srandmember('http', r.scard('http'))
    return f'可用http数量{len(num)}'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5555, debug=True)
