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
            include_keys=True,
            output_delim='\n',
            *args,
            **kwargs
        ) -> None:
        super().__init__(self.name, **kwargs)
        self.start_urls=start_urls
        self.config = components
        self.type = output_type
        self._include_keys = include_keys
        self.output_delim = output_delim

    def start_requests(self):
        for url in self.start_urls:
            yield  scrapy.Request(
                    url=url,
                    callback=self.parse,
                    cb_kwargs={}
                )


    def parse(self, response: scrapy.http.Response):
        selector = scrapy.Selector(response)
        outputs = {} if self.type != 'text' else []
        for cfg in self.config:
            data = []
            count = cfg.get('count', None)
            if self.type == 'text' and self._include_keys:
                data.append(cfg['key'])
            if 'xpath' in cfg:
                path = cfg['xpath']
                if not isinstance(path, list):
                    path = [path]
                for p in path:
                    data.extend(selector.xpath(p).getall()[:count])
            else:
                path = cfg['css']
                if not isinstance(path, list):
                    path = [path]
                for p in path:
                    data.extend(selector.css(p).getall()[:count])

            for i in range(len(data)):
                if cfg.get('join_url', False):
                    if self._include_keys and i == 0:
                        continue
                    data[i] = urljoin(response.url, data[i])
                else:
                    data[i] = data[i].replace('\n', '\\n')
                    data[i] = data[i].replace('\t', '\\t')

            if self.type != 'text':
                outputs[cfg['key']] = data
            else:
                if self._include_keys:
                    outputs.append(
                        f'{data[0]}\n' +
                        f'{self.output_delim}'.join(data[1:])
                    )
                else:
                    outputs.append(
                        f'{self.output_delim}'.join(data)
                    )
        if self.type != 'text':
            yield {'text': json.dumps(outputs, ensure_ascii=False), 'url': response.url}
        else:
            yield {'text': '\n\n'.join(outputs), 'url': response.url}



