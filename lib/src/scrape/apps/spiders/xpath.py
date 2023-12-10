import scrapy


class XpathSpider(scrapy.Spider):
    name = 'xpath'

    def __init__(self, start_urls, ) -> None:
        self.start_urls=start_urls

    def start_requests(self):
        requests = []
        for url in self.start_urls:
            requests.append(
                scrapy.Request(
                    url=url,
                    callback=self.parse,
                    cb_kwargs={}
                )
            )
        return requests

    def parse(self, response, ):
        sel = scrapy.Selector(response)
        sel.xpath()
