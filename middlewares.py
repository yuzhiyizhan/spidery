import time
import aiohttp
from loguru import logger


# url http://127.0.0.1:5555/https | http://127.0.0.1:5555/http


class IPProxyDownloadMiddleware(object):
    async def process_request(self, request, spider):
        async with aiohttp.ClientSession() as client:
            while True:
                responses = await client.get(url='http://127.0.0.1:5555/https')
                proxies = await responses.text()
                if proxies == '43.255.228.150:3128':
                    time.sleep(30)
                    continue
                request.meta['proxy'] = 'https://' + proxies
                logger.debug(f'使用代理{proxies}')
                break

# settings.py
# TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
