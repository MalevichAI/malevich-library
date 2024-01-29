import uuid

import apps.lib.crawl
import apps.lib.proc
import apps.middleware.selenium
import apps.spiders.aliexpress
import apps.spiders.bing
import apps.spiders.google
import apps.spiders.text
import apps.spiders.xpath
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

    return (procs, ids)

