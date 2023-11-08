from itertools import islice

import pandas as pd
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel
from scrapy.crawler import CrawlerProcess

from .spiders import SPIDERS


@scheme()
class ScrapeLinks(BaseModel):
    link: str

@scheme()
class ScrapeResult(BaseModel):
    result: str

@processor()
def scrape_with(
    scrape_links: DF[ScrapeLinks],
    context: Context
):
    """Scrapes web links.

    Input:
        A dataframe with a column named `link` containing web links.

    Output:
        A dataframe with a column named `text` containing the text
        scraped from the web links.

    Configuration:
        - allowed_domains (list[str]):
            A list of allowed domains to scrape. If not provided, all domains
            are allowed, so the app will traverse the entire web.
        - max_depth (int):
            The maximum depth to traverse the web. If not provided, the app will
            traverse as deep as possible.
        - spiders (list[str]):
            A list of spiders to use for scraping. If not provided, the app will
            use the default spider.
        - max_results (int):
            The maximum number of results to return. If not provided, the app
            will return all results. Defaults to 1000.
        - spider_cfg (dict):
            A dictionary of configuration options for the spiders. If not
            provided, the app will use the default configuration for each
            spider.
        - timeout (int):
            The maximum number of seconds to wait for collecting responses
            from the spiders. If not provided, the app will wait indefinitely.
            Defaults to 15 seconds.
        - squash_results (bool):
            If true, the app will squash the results into a single string.
            Defaults to false.
        - squash_delimiter (str):
            The delimiter to use when squashing results. Defaults to a new line.

            See available spiders in Details.

            Also, each of the spiders may have its own configuration options.
            See the documentation for each spider for more information.

    Details:
        Either `allowed_domains` or `max_depth` must be provided. If both are
        provided, the app will traverse the web until either condition is met.

        Available spiders:
            - text: Extracts text from web pages.

    Args:
        scrape_links (DF[ScrapeLinks]):
            A dataframe with a column named `link` containing web links.
        context (Context):
            The context information.

    Returns:
        DF[ScrapeResult]:
            A dataframe with a column named `text` containing the text
            scraped from the web links.
    """
    assert context.app_cfg.get('allowed_domains') or context.app_cfg.get('max_depth'), \
        'Either allowed_domains or max_depth must be provided.'

    spider_cls = SPIDERS.get(context.app_cfg.get('spider', 'text'))
    assert spider_cls, 'Spider not found.'

    timeout = context.app_cfg.get('timeout', 15)

    process = CrawlerProcess(settings={
        'CLOSESPIDER_TIMEOUT': timeout,
        'CLOSESPIDER_ITEMCOUNT': context.app_cfg.get('max_results', 1000),
        'DEPTH_LIMIT': context.app_cfg.get('max_depth', None) or 0,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json'
    })

    process.crawl(
        spider_cls,
        start_urls=scrape_links.link.to_list(),
        allowed_domains=context.app_cfg.get('allowed_domains', []),
        **context.app_cfg.get('spider_cfg', {})
    )
    process.start(stop_after_crawl=True)

    with open('output.json') as f:
        results = [
            item['text']
            for item in islice(
                pd.read_json(f).to_dict('records'),
                context.app_cfg.get('max_results', 1000)
            )
        ]

    process.stop()

    if context.app_cfg.get('squash_results', False):
        return pd.DataFrame({
            'result': [
                context.app_cfg.get('squash_delimiter', '\n').join(results)
            ]
        })
    else:
        return pd.DataFrame({
            'result': list(set(results))
        })
