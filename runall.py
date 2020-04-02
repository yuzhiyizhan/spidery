# from scrapy import cmdline
# cmdline.execute(['scrapy', 'crawlall'])
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


def main():
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    didntWorkSpider = ['sample']

    for spider_name in process.spiders.list():
        if spider_name in didntWorkSpider:
            continue
        print("Running spider %s" % (spider_name))
        process.crawl(spider_name)
    process.start()
main()