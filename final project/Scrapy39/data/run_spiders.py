from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from data.spiders import a39net


def run_spiders():
    process = CrawlerProcess(get_project_settings())
    process.crawl(a39net.A39netSpider)

    process.start()


if __name__ == "__main__":
    run_spiders()
