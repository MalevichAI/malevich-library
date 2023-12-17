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
                data.extend(selector.xpath(cfg['xpath']).getall())
            except KeyError:
                data.extend(selector.css(cfg['css']).getall())
            for i in range(len(data)):
                data[i] = data[i].replace('\n', '\\n')
                data[i] = data[i].replace('\t', '\\t')

            if self.type == 'json':
                outputs[cfg['key']] = data
            else:
                outputs.append('\n'.join(data))
        if self.type == 'json':
            yield outputs
        else:
            yield {'items': '\n\n'.join(outputs)}


