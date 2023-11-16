import json
import logging
from typing import Any
from urllib.parse import urlencode

import scrapy
import scrapy.http


def get_scrappable_url(url: str, api_key: str) -> str:
    payload = {
        'api_key': api_key,
        'url': url,
        'autoparse': 'true',
        'country_code': 'us'
    }
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


def build_google_link(query: str):
    google_dict = {'q': query }
    return 'http://www.google.com/search?' + urlencode(google_dict)


def get_domain(url: str) -> str:
    # https://stackoverflow.com/a/9626540/9263761 -> www.stackoverflow.com

    # remove http:// and https://
    url = url.replace('https://', '').replace('http://', '')

    # remove www.
    url = url.replace('www.', '')

    # remove everything after the first /
    url = url.split('/')[0]

    return 'www.' + url



class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['api.scraperapi.com']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'LOG_LEVEL': 'INFO',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 5,
        'RETRY_TIMES': 5
    }

    def __init__(
        self,
        scrape_api_key = None,
        allow_same_domain = False,
        cut_to_domain = False,
        start_urls = None,
        *args: Any,
        **kwargs: Any
    ) -> None:  # noqa: ANN401, E501
        super().__init__(self.name, **kwargs)

        if not scrape_api_key:
            raise ValueError("scrape_api_key is required")

        self._api_key = scrape_api_key
        self.start_urls = [
            get_scrappable_url(build_google_link(x), self._api_key)
            for x in start_urls
        ]
        self._allow_same_domain = allow_same_domain
        self._cut_to_domain = cut_to_domain
        self._domain_set = set()


    def parse(self, response: scrapy.http.Response):
        di = json.loads(response.text)
        for result in di['organic_results']:
            domain = get_domain(result['link'])
            if not self._allow_same_domain and domain in self._domain_set:
                continue
            self._domain_set.add(domain)
            link = result['link'] if not self._cut_to_domain else domain
            yield {'text': link}

        try:
            next_page = di['pagination']['load_more_url']
            if next_page:
                yield scrapy.Request(
                    get_scrappable_url(next_page, self._api_key),
                    callback=self.parse
                )
        except Exception:
            logging.info("No more pages. Exiting...")
            return

