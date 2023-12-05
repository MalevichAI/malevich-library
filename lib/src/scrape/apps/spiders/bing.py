import json
import logging
from typing import Any
from urllib.parse import urlencode

import scrapy
import scrapy.http


def get_scrappable_url(query, offset, count=50) -> str:
    payload = {
        "q": query,
        "count": count,
        "offset": offset,
        "cc": "us"
    }
    proxy_url = 'https://api.bing.microsoft.com/v7.0/search?' + \
        urlencode(payload)
    return proxy_url


def get_domain(url: str) -> str:
    # https://stackoverflow.com/a/9626540/9263761 -> www.stackoverflow.com

    # remove http:// and https://
    url = url.replace('https://', '').replace('http://', '')

    # remove www.
    url = url.replace('www.', '')

    # remove everything after the first /
    url = url.split('/')[0]

    return 'www.' + url


class BingSpider(scrapy.Spider):
    name = 'bing'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'LOG_LEVEL': 'INFO',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 5,
        'RETRY_TIMES': 5
    }

    def __init__(
        self,
        bing_api_key=None,
        allow_same_domain=False,
        cut_to_domain=False,
        start_urls=None,
        *args: Any,  # noqa: ANN401
        **kwargs: Any  # noqa: ANN401
    ) -> None:

        super().__init__(self.name, **kwargs)
        if not bing_api_key:
            raise ValueError("bing_api_key is required")

        self._api_key = bing_api_key
        self.start_urls = start_urls
        self._allow_same_domain = allow_same_domain
        self._cut_to_domain = cut_to_domain
        self._domain_set = set()

    def start_requests(self):
        requests = []
        for query in self.start_urls:
            requests.append(
                scrapy.Request(
                    url=get_scrappable_url(query, 1),
                    headers={"Ocp-Apim-Subscription-Key": self._api_key},
                    callback=self.parse,
                    cb_kwargs={
                        'offset': 1
                    }
                )
            )
        return requests

    def parse(self, response: scrapy.http.Response, offset=1, count=50, max=None):
        di = json.loads(response.text)
        if max is None:
            max = min(di['webPages']['totalEstimatedMatches'], 65535)
        self.logger.info(f"RESULTS {len(di['webPages']['value'])}")
        for result in di['webPages']['value']:
            domain = get_domain(result['url'])
            if not self._allow_same_domain and domain in self._domain_set:
                self.logger.info(f"SKIPPING {domain}")
                continue
            self._domain_set.add(domain)
            link = result['url'] if not self._cut_to_domain else domain
            self.logger.info(f"LINK {link}")
            yield {'text': link}
        self.logger.info(f"Offset {offset}, Count: {count}, Max: {max}")
        offset += count
        if offset < max:
            yield scrapy.Request(
                url=get_scrappable_url(
                    di['queryContext']['originalQuery'],
                    offset,
                    count
                ),
                callback=self.parse,
                headers={
                    "Ocp-Apim-Subscription-Key": self._api_key
                },
                cb_kwargs={
                    'offset': offset,
                    'count': count,
                    'max': max
                }
            )
        else:
            logging.info("No more pages. Exiting...")
            return
