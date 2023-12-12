import json
from urllib.parse import urlencode

import scrapy
import scrapy.http


class Response:
    def __init__(self, text, url) -> None:
        self.text = text
        self.url = url

class AliexpSpider(scrapy.Spider):
    name = 'aliexpress'

    def __init__(
            self,
            start_urls,
            scrape_api_key,
            output_type='json',
            *args,
            **kwargs
        ) -> None:
        super().__init__(self.name, **kwargs)
        self.start_urls=start_urls
        self.type = output_type
        self.api_key=scrape_api_key

    def form_request(self, url):
        payload = {
            'asp': 'true',
            'render_js': 'true',
            'auto_scroll': 'true',
            'url': url,
            'key': self.api_key
        }
        return 'https://api.scrapfly.io/scrape?' + urlencode(payload)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(self.form_request(url), callback=self.parse) \

    def parse(self, response: scrapy.http.Response):
        with open('file1.html', 'w') as f:
            f.write(response.text)
        outputs = json.loads(response.text)
        sel = scrapy.Selector(Response(outputs['result']['content'], response.url))
        data = {} if self.type == 'json' else ''
        title = ' '.join(sel.xpath('//h1/text()').getall())
        description = ' '.join(
            sel.xpath(
                "//span[contains(@id, 'tl_')]/text()"
            ).getall()
        )
        characteristics = description + ' ' + ' '.join(sel.xpath(
            "//span[contains(@class, 'titleContent') or \
                contains(@class, 'value')]/text()"
        ).getall())
        if self.type == 'json':
            data['title'] = title
            data['description'] = characteristics
            yield {'text': json.dumps(data, ensure_ascii=False)}
        else:
            data += f'Title:\n{title}\n\nDescription:\n{characteristics}'
            yield {'text': data }
