import json

import scrapy
import scrapy.http


class XpathSpider(scrapy.Spider):
    name = 'xpath'

    def __init__(self, start_urls, components, output_type='json') -> None:
        self.start_urls=start_urls
        self.config = components
        self.type = output_type

    def start_requests(self):
        for url in self.start_urls:
            yield  scrapy.Request(
                    url=url,
                    callback=self.parse,
                    cb_kwargs={}
                )


    def parse(self, response: scrapy.http.Response):
        selector = scrapy.Selector(response)
        outputs = {} if self.type == 'json' else []
        for cfg in self.config:
            data = []
            if self.type == 'text':
                data.append(cfg['key'])
            try:
                data = selector.xpath(cfg['xpath']).getall()
            except KeyError:
                data = selector.css(cfg['css']).getall()

            if self.type == 'json':
                outputs[cfg['key']] = data
            else:
                outputs.append('\n'.join(data))

        if self.type == 'json':
            yield json.dumps(outputs)
        else:
            yield '\n\n'.join(outputs)



