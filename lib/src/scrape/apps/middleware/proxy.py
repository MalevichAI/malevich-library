import os
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256

import pandas as pd
import requests
from malevich.square import APP_DIR, DF, Context, processor, scheme
from pydantic import BaseModel
from scrapy import Selector

from .models import GetPageCrawlbaseAli, GetPageWithProxy

CRAWLBASE_CFG = {
    'page_wait': 3000,
    'ajax_wait': 2000
}
SCRAPE_CFG = {
    'render': 'true'
}

@scheme()
class CrawlBase(BaseModel):
    link: str

class Response:
    def __init__(self, text, url) -> None:
        self.text = text
        self.url = url
        self.encoding = 'utf-8'

def get_page(config: dict):
    return requests.get(
        "https://api.crawlbase.com/",
        params=config
    )

def get_page_scrape(config: dict):
    return requests.get(
        'https://api.scraperapi.com/',
        params=config
    )


@processor()
def get_page_with_proxy(df: DF, context: Context[GetPageWithProxy]):
    """Get web page using proxy API (Scrape API or Crawlbase)
    ## Input:
        A DataFrame with columns:
            - link (str): Link to a page.

    ## Output:
        Two DataFrames. First one is Result DataFrame with columns:
            - link (str): Link to a page.
            - filename (str): Filename to which the page was written.
    ---
        Second DataFrame contains errors occured. Columns:
            - link (str): Link to the page.
            - error (str): Which error occured. Either status_code or error name.

    ## Configuration:
        - token: str.
            API token (CrawlBase or ScrapeAPI).
        - api: str, default "crawlbase".
            Which API to use: CrawlBase or ScrapeAPI.
        - proxy_config: dict, default {}.
            Config with request parameters. Reffer to [Crawlbase Docs](https://crawlbase.com/docs/crawling-api/parameters) or [Scrape Docs](https://docs.scraperapi.com/making-requests/customizing-requests).
    -----
    Args:
        df(DF[CrawlBase]): DataFrame with aliexpress links.
    Returns:
        DataFrames with results and errors.
    """  # noqa: E501
    out = []
    captcha = []
    results = []
    token = context.app_cfg.get('token', None)
    assert context.app_cfg.get('token', None), "Proxy token must be provided"
    api = context.app_cfg.get('api', 'crawlbase')

    cfg = context.app_cfg.get('proxy_config', {})
    if api == 'crawlbase':
        cfg["token"] = token
    else:
        cfg["api_key"] = token
    if context.app_cfg.get('api', 'crawlbase') == 'crawlbase':
        for k, v in CRAWLBASE_CFG.items():
            if k not in cfg:
                cfg[k] = v
    else:
        for k, v in SCRAPE_CFG.items():
            if k not in cfg:
                cfg[k] = v

    with ThreadPoolExecutor(15) as executor:
        for pr in df['link'].to_list():
            cfg['url'] = pr
            task = executor.submit(
                (
                    get_page if api == 'crawlbase'
                    else get_page_scrape
                ),
                config = cfg
            )
            results.append((pr, task))
        for link, thrd in results:
            response = thrd.result()
            if api == 'crawlbase':
                if str(response.headers['pc_status']) != '200':
                    captcha.append(
                        [
                            link,
                            'Captcha' if response.headers['pc_status'] == 503
                            else response.headers['pc_status']
                        ]
                    )
                    continue
            else:
                if response.status_code >= 400:
                    captcha.append([link, response.status_code])
                    continue

            data = response.text

            filename = sha256(link.encode()).hexdigest() + '.html'
            with open(os.path.join(APP_DIR, filename), 'w') as f:
                f.write(
                    data
                )
            context.share(filename)
            out.append(
                [
                    link,
                    filename
                ]
            )
    return (
        pd.DataFrame(out, columns=['link', 'filename']),
        pd.DataFrame(captcha, columns=['link', 'error'])
    )


@processor()
def get_page_crawlbase_ali(df: DF[CrawlBase], context: Context[GetPageCrawlbaseAli]):
    """Get aliexpress product page using API
    ## Input:
        A DataFrame with columns:
            - link (str): Link to a page.

    ## Output:
        Two DataFrames. First one is Result DataFrame with columns:
            - link (str): Link to a page.
            - filename (str): Filename where the page was written.
    ---
        Second DataFrame contains errors occured. Columns:
            - link (str): Link to the page.
            - error (str): Which error occured.

    ## Configuration:
        - token: str.
            API token (CrawlBase or ScrapeAPI).
        - api: str, default "crawlbase".
            Which API to use: CrawlBase or ScrapeAPI.
    -----
    Args:
        df(DF[CrawlBase]): DataFrame with aliexpress links.
    Returns:
        DataFrames with results and errors.
    """
    cfg = context.app_cfg.get('proxy_config', {})
    if 'selector' not in cfg:
        cfg['selector']='div#characteristics_anchor'

    context.app_cfg['proxy_config'] = cfg

    files_df, errors_df = get_page_with_proxy(df, context)
    captcha = []
    files = []
    for _, row in errors_df.iterrows():
        captcha.append([row['link'], row['error']])
    for _, row in files_df.iterrows():
        link = row['link']
        data = open(context.get_share_path(row['filename'])).read()
        sel = Selector(Response(data, link))
        if sel.xpath("//div[@class = 'scratch-captcha-title']").get() is not None:
            captcha.append([link, 'Captcha'])
            continue
        elif sel.xpath("//h1[contains(@class, 'PageNotFound')]").get() is not None:
            captcha.append([link, 'NotFound'])
            continue
        else:
            files.append([link, row['filename']])
    return (
        pd.DataFrame(files, columns=['link', 'filename']),
        pd.DataFrame(captcha, columns=['link', 'error'])
    )
