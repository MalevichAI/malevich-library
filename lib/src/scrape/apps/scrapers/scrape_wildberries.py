import re

import pandas as pd
import scrapy
from malevich.square import DF, Context, processor

from .models import ScrapeWildberries


class Response:
    def __init__(self, text, url) -> None:
        self.text = text
        self.url = url
        self.encoding = 'utf-8'

@processor()
def scrape_wildberries(
        df: DF,
        context: Context[ScrapeWildberries]
    ):
    """
    Scarpe Wildberries Product Card

    ## Input:
        A single DataFrame with two columns:
        - `link` (str): Link to the product.
        - `filename` (str): Filename to which the product was written.

    ## Output:
        Three DataFrames with text, images and properties. First one contains two columns:
        - link (str): Link to the product
        - text (str): Product title and description

    ---

        Second DataFrame contains two columns:
        - link (str): Link to the product
        - image (str): Link to the image

    ---

        Last DataFrame contains three columns:
        - link (str): Link to the product
        - key (str): Property key
        - value (str): Property value

    ## Configuration:
        - max_results: int, default 3.
            The amount of images to retrieve.
    -----
    """  # noqa: E501
    max_results = context.app_cfg.get('max_results', 3)
    text_df = []
    image_df = []
    props_df = []

    for _, row in df.iterrows():
        link = row['link']
        page = open(context.get_share_path(row['filename'])).read()
        sel = scrapy.Selector(text=page)
        prop_row = sel.xpath('//tbody').getall()
        for pr in prop_row:
            props = scrapy.Selector(text=pr).xpath('string(//tbody)').get()
            if props is not None:
                kvs = re.sub(r" {4,}", "<sep>", props.strip())
                kvs = kvs.split('<sep>')
                for i in range(0,len(kvs), 2):
                    props_df.append(
                        [link, kvs[i].strip('\n '), kvs[i+1].strip('\n ')]
                    )

        text = ""
        title = sel.xpath("//h1[contains(@class, 'title')]/text()").get()
        if title:
            text += f"Title:\n{title}\n\n"
        desc= sel.xpath(
            '//section[contains(@class, "description")]/*[@class="option__text"]/text()'
        ).get()
        if desc:
            text += f"Description:\n{desc}"
        text_df.append([link, text])

        images = sel.xpath('//ul[contains(@class, "swiper")]//img[contains(@src, "https://")]/@src').getall()
        for i in range(0, min(max_results, len(images))):
            image_df.append([link, images[i]])

    return (
        pd.DataFrame(text_df, columns=['link', 'text']),
        pd.DataFrame(image_df, columns=['link', 'image']),
        pd.DataFrame(props_df, columns=['link', 'key', 'value'])
    )
