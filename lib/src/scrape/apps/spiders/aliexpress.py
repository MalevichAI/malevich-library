import json
import re

import scrapy
import scrapy.http


class AliexpSpider(scrapy.Spider):
    name = 'aliexpress'

    def __init__(
            self,
            start_urls,
            browser_language='ru',
            *args,
            **kwargs
        ) -> None:
        super().__init__(self.name, **kwargs)
        self.start_urls=start_urls
        self.browser_language = browser_language

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        sel = scrapy.Selector(response)

        not_found = sel.xpath("//h1/text()").getall()
        if "Такой страницы нет" in not_found:
            return {
                'text': "",
                'json': json.dumps({}, ensure_ascii=False),
                'status': 404
            }

        title = ' '.join(sel.xpath('//h1/text()').getall())
        description = "" + ' '.join(sel.xpath(
            "//div[@id = 'content_anchor']//*[not(self::img) and not(self::script) \
            and not(self::div)]/text()"
        ).getall())
        description = re.sub("[\n ]*$", "", description)
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

        images = sel.xpath("//div[ contains( @class, 'gallery_Gallery__picList')]//picture//img/@src").getall()   # noqa: E501
        images.extend(sel.xpath("//div[@id = 'content_anchor']//img/@src").getall())
        json_data = {}
        json_data['title'] = title
        json_data['description'] = description
        json_data['properties'] = properties
        json_data['images'] = images
        json_data['multicards'] = response.cards
        data = ''
        data += (
            f'Title:\n{title}\n\n'
            f'Description:\n{description}\n\n'
            f'Properties:\n{properties}\n\n'
        )
        yield {
                'text': data,
                'json': json.dumps(json_data, ensure_ascii=False),
                'status': 200
            }
