import os
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from urllib.parse import quote

import pandas as pd
import requests
from malevich.square import APP_DIR, DF, Context, processor, scheme
from pydantic import BaseModel
from scrapy import Selector

from .models import GetPageCrawlbaseAli


@scheme()
class CrawlBase(BaseModel):
    link: str

class Response:
    def __init__(self, text, url) -> None:
        self.text = text
        self.url = url

def get_page(link, token):
    link = (
        f"https://api.crawlbase.com/?token={token}"
        f"&url={quote(link, safe='')}&page_wait=3000"
    )
    return requests.get(
        link
    ).text

@processor()
def get_page_crawlbase_ali(df: DF[CrawlBase], context: Context[GetPageCrawlbaseAli]):
    """Get aliexpress product page using CrawlBase API
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
            CrawlBase API token (https://crawlbase.com/).

    -----
    Args:
        df(DF[CrawlBase]): DataFrame with aliexpress links.
    Returns:
        DataFrames with results and errors.
    """
    out = []
    captcha = []
    results = []
    with ThreadPoolExecutor(15) as executor:
        for pr in df['link'].to_list():
            task = executor.submit(
                get_page,
                link=pr,
                token=context.app_cfg.get('crawlbase_token')
            )
            results.append((pr, task))
        for link, thrd in results:
            data = thrd.result()
            sel = Selector(Response(data, link))

            if sel.xpath("//div[@class = 'scratch-captcha-title']").get() is not None:
                captcha.append([link, 'Captcha'])
            elif sel.xpath("//h1[contains(@class, 'PageNotFound')]").get() is not None:
                captcha.append([pr, 'NotFound'])
            else:
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
