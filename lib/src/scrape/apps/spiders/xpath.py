import json

import scrapy
import scrapy.http


class XpathSpider(scrapy.Spider):
    name = 'xpath'

    def __init__(self, start_urls, config) -> None:
        self.start_urls=start_urls
        self.config = config

    def start_requests(self):
        for url in self.start_urls:
            yield  scrapy.Request(
                    url=url,
                    callback=self.parse,
                    cb_kwargs={}
                )


    def parse(self, response: scrapy.http.Response):
        selector = scrapy.Selector(response)
        for cfg in self.config:
            data = []
            try:
                data = selector.xpath(cfg['xpath']).getall()
            except KeyError:
                data = selector.css(cfg['css']).getall()
            yield json.dumps({cfg['key']: data})
        return



