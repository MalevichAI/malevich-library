import re

import pandas as pd
import scrapy
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel

from .models import ScrapeAliexpress


@scheme()
class ScrapeLinksAli(BaseModel):
    link: str
    filename: str


@scheme()
class ScrapeResult(BaseModel):
    result: str


class Response:
    def __init__(self, text, url) -> None:
        self.text = text
        self.url = url
        self.encoding = 'utf-8'

@processor()
def scrape_aliexpress(
        scrape_links: DF[ScrapeLinksAli],
        context: Context[ScrapeAliexpress]
    ):
    """Scrapes aliexpress.

    ## Input:

        A dataframe with two columns:
        - `link` (str): containing web links to be scraped
        - `filename` (str): filename with page content

    ## Output:
        Depends on the configuration, processor returns from 2 to 5 DataFrames.

        By default, it returns 2 DataFrames: images, key-value fields.

        Each DataFrame has a `link` column. And depend on the DataFrame, it has its own columns.
        For example: Image DataFrame has two columns: `link` and `image`.

        ---

        If `properties_only` is True, processor will return 2 DataFrames: properties and errors.
        Same situation when `images_only` will be set to True.


    ## Configuration:

        - max_results: int, default None.
            Max images to retrieve.
        - only_images: bool, default False.
            Get only images DataFrame.
        - only_properties: bool, default False.
            Get only properties DataFrame.

    -----

    Args:
        scrape_links (DF[ScrapeLinksAli]): A dataframe with a column named `link` containing web links.
        context: The configuration dictionary. See [Available Options] for more information.

    Returns:
        A dataframe with a textual column named `result`
    """ # noqa: E501
    max_results = context.app_cfg.get('max_results', None)
    imgs_only = context.app_cfg.get('only_images', False)
    props_only = context.app_cfg.get('only_properties', False)

    image_df = []
    props_df = []
    for _, row in scrape_links.iterrows():
        link = row['link']
        file = open(context.get_share_path(row['filename'])).read()
        sel = scrapy.Selector(Response(file, link))

        properties = {}

        description = "" + sel.xpath(
            "normalize-space(string(//div[@id = 'content_anchor']))"
        ).get()

        description = re.sub(r'window.adminAccountId=.*;', '', description)

        properties['title'] = sel.xpath('//h1/text()').get()
        properties['description'] = description
        properties['price'] = sel.xpath(
            "//div[contains(@class, 'Price')]/text()"
        ).get()
        properties['brand'] = sel.xpath(
            "//div[@id = 'characteristics_anchor']//span[2]/text()"
        ).get()
        try:
            properties['internal_pim_id'] = re.search(
                r'item\/(?P<PIM>\d+)\.html',
                link
            ).group("PIM")
        except Exception:
            properties['internal_pim_id'] = None

        keys = sel.xpath(
            "//div[@id = 'characteristics_anchor']//span[contains(@class, 'title') or contains(@class, 'name')]/text()"  # noqa: E501
        ).getall()
        values = sel.xpath(
            "//div[@id = 'characteristics_anchor']//span[contains(@class, 'value')]/text()" # noqa: E501
        ).getall()

        for key, val in zip(keys, values):
            if key not in properties.keys():
                properties[key] = val

        images = sel.xpath("//div[contains(@class, 'Grid')]//div[contains(@class, 'gallery_Gallery__picList')]//picture//img/@src").getall()   # noqa: E501
        images.extend(sel.xpath("//div[@id = 'content_anchor']//img/@src").getall())

        for image in images[:max_results]:
            image_df.append([link, image])

        for key in properties.keys():
            props_df.append([link, key, properties[key]])

    return_df = []

    if imgs_only:
        return_df.append(pd.DataFrame(image_df, columns=["link", "image"]))

    elif props_only:
        return_df.append(pd.DataFrame(props_df, columns=["link", "key", "val"]))

    else:
        return_df.extend([
            pd.DataFrame(image_df, columns=["link", "image"]),
            pd.DataFrame(props_df, columns=["link", "name", "value"])
        ])

    return return_df
