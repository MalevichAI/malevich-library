import json
from urllib.parse import urljoin

import scrapy
import scrapy.http


class XpathSpider(scrapy.Spider):
    name = 'xpath'

    def __init__(
            self,
            start_urls,
            components,
            output_type='json',
            include_keys=False,
            *args,
            **kwargs
        ) -> None:
        super().__init__(self.name, **kwargs)
        self.start_urls=start_urls
        self.config = components
        self.type = output_type
        self._include_keys = include_keys

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
            count = cfg.get('count', None)
            if self.type == 'text' and self._include_keys:
                data.append(cfg['key'])
            try:
                data.extend(selector.xpath(cfg['xpath']).getall()[:count])
            except KeyError:
                data.extend(selector.css(cfg['css']).getall()[:count])
            for i in range(len(data)):
                if cfg.get('join_url', False):
                    if self._include_keys and i == 0:
                        continue
                    data[i] = urljoin(response.url, data[i])
                else:
                    data[i] = data[i].replace('\n', '\\n')
                    data[i] = data[i].replace('\t', '\\t')

            if self.type == 'json':
                outputs[cfg['key']] = data
            else:
                outputs.append('\n'.join(data))
        if self.type == 'json':
            yield {'text': json.dumps(outputs, ensure_ascii=False)}
        else:
            yield {'text': '\n\n'.join(outputs)}



