import os
import uuid
from itertools import islice

import apps.lib.crawl
import apps.lib.proc
import apps.middleware.selenium
import apps.spiders.aliexpress
import apps.spiders.bing
import apps.spiders.google
import apps.spiders.text
import apps.spiders.xpath
import pandas as pd
from malevich.square import DF, Context, scheme
from pydantic import BaseModel

SPIDERS = {
    'text': 'apps.spiders.text.TextSpider',
    'google': 'apps.spiders.google.GoogleSpider',
    'bing': 'apps.spiders.bing.BingSpider',
    'linkedin_people_profile': 'apps.spiders.linked_in_profiles.LinkedInPeopleSpider',
    'linkedin_company_profile': 'apps.spiders.linked_in_org.LinkedInCompanySpider',
    'aliexpress': 'apps.spiders.aliexpress.AliexpSpider',
    'xpath': 'apps.spiders.xpath.XpathSpider',
}

@scheme()
class ScrapeLinks(BaseModel):
    link: str


@scheme()
class ScrapeResult(BaseModel):
    result: str


def run_spider(
        scrape_links: DF[ScrapeLinks],
        context: Context
    ):
    spider_cls = SPIDERS.get(context.app_cfg.get('spider', 'text'))
    assert spider_cls, 'Spider not found.'

    timeout = context.app_cfg.get('timeout', 15)

    links_are_independent = context.app_cfg.get('links_are_independent', False)

    if links_are_independent:
        links = [[x] for x in scrape_links.link.to_list()]
    else:
        links = [scrape_links.link.to_list()]

    results = []
    procs: list[apps.lib.proc.XtProcess] = []
    ids = []

    for links_batch in links:
        _id = uuid.uuid4().hex
        settings = {
                    'CLOSESPIDER_TIMEOUT': timeout,
                    'CLOSESPIDER_ITEMCOUNT': context.app_cfg.get('max_results', 0),
                    'DEPTH_LIMIT': context.app_cfg.get('max_depth', 1),
                    'FEED_FORMAT': 'json',
                    "FEED_EXPORT_ENCODING": "utf-8",
                    'FEED_URI': f'output-{_id}.json'
        }
        if context.app_cfg.get('spider', 'text') == 'aliexpress':
            settings['DOWNLOADER_MIDDLEWARES'] = {
                apps.middleware.selenium.Selenium : 543
            }

        proc = apps.lib.proc.XtProcess(
            target=apps.lib.crawl.crawl,
            kwargs={
                'settings': settings,
                'spider_cls': eval(spider_cls),
                'start_urls': links_batch,
                'allowed_domains': context.app_cfg.get('allowed_domains', []),
                **context.app_cfg.get('spider_cfg', {})
            }
        )

        proc.start()
        procs.append(proc)
        ids.append(_id)

    for proc_, _id in zip(procs, ids):
        proc_.join(timeout * len(procs) if timeout > 0 else None)
        # Raise if proc failed
        if proc_.exitcode != 0:
            # print exception in proc
            proc_.terminate()
            raise Exception(f'Scraping failed. {proc_.exception}')

        assert os.path.exists(f'output-{_id}.json'), \
            "Scraper failed to save the results. Try descresing `max_results` or `timeout` options"  # noqa: E501

        with open(f'output-{_id}.json') as f:
            max_results = context.app_cfg.get('max_results', 0)
            df = pd.read_json(f).to_dict('records')
            if max_results == 0:
                max_results = len(df)

            results_ = [item['text'] for item in islice(df, max_results)]
            if context.app_cfg.get('squash_results', False) or links_are_independent:
                results.append(
                    context.app_cfg.get('squash_delimiter',
                                        '\n').join(results_)
                )
            else:
                results.extend(results_)
    return pd.DataFrame({'result': results})
