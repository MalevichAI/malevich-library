import json

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
            output_type='json',
            only_images=False,
            only_properties=False,
            browser_language='ru',
            *args,
            **kwargs
        ) -> None:
        super().__init__(self.name, **kwargs)
        self.start_urls=start_urls
        self.type = output_type
        self.img_only = only_images
        self.prop_only = only_properties
        self.browser_language = browser_language

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response:scrapy.http.Response):
        sel = scrapy.Selector(Response(response.body.decode(), response.url))
        if not self.img_only and not self.prop_only:
            data = {} if self.type == 'json' else ''
            title = ' '.join(sel.xpath('//h1/text()').getall())

            description = ' '.join(
                sel.xpath(
                    "//*[contains(@id, 'tl_')]/text()"
                ).getall()
            )
            keys = sel.xpath(
                "//div[@id = 'characteristics_anchor']//span[contains(@class, 'title')]/text()"  # noqa: E501
            ).getall()
            values = sel.xpath(
                "//div[@id = 'characteristics_anchor']//span[contains(@class, 'value')]/text()" # noqa: E501
            ).getall()
            properties = []
            for key, val in zip(keys, values):
                properties.append(f'{key}: {val}')

            properties = ', '.join(properties)

            images = sel.xpath("//div[@class = 'gallery_Gallery__picList__1gsooe']//picture//img/@src").getall()   # noqa: E501
            images.extend(sel.xpath("//div[@id = 'content_anchor']//img/@src").getall())
            if self.type == 'json':
                data['title'] = title
                data['description'] = description
                data['properties'] = properties
                data['images'] = images
                yield {'text': json.dumps(data, ensure_ascii=False)}
            else:
                data += f'Title:\n{title}\n\n' +\
                    f'Description:\n{description}\n\n' +\
                    f'Properties:{properties}\n\n' +\
                    'Images:\n'.join(images)
                yield {'text': data }
        elif self.prop_only:
            keys = sel.xpath(
                "//div[@id = 'characteristics_anchor']//span[contains(@class, 'title')]/text()"  # noqa: E501
            ).getall()
            values = sel.xpath(
                "//div[@id = 'characteristics_anchor']//span[contains(@class, 'value')]/text()" # noqa: E501
            ).getall()
            properties = []
            for key, val in zip(keys, values):
                properties.append(f'{key}: {val}')

            properties = ', '.join(properties)
            yield {'text': properties}
        else:
            images = sel.xpath(
                "//div[@class = 'gallery_Gallery__picList__1gsooe']//picture//img/@src"
            ).getall()
            for img in images:
                yield {'text': img}
