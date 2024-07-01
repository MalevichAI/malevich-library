import json
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

        By default, it returns 3 DataFrames: text, images, properties.

        Each DataFrame has a `link` column. And depend on the DataFrame, it has its own columns.
        For example: Image DataFrame has two columns: `link` and `image`.

        ---

        If `properties_only` is True, processor will return 2 DataFrames: properties and errors.
        Same situation when `images_only` will be set to True.


    ## Configuration:

        - max_results: str, default None.
            Max images to retrieve.
        - only_images: bool, default False.
            Get only images DataFrame.
        - only_properties: bool, default False.
            Get only properties DataFrame.
        - output_type: str, default 'text'.
            Format of text data. Either 'text' or 'json'.

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
    output_type = context.app_cfg.get('output_type', 'text')

    text_df = []
    image_df = []
    props_df = []
    for _, row in scrape_links.iterrows():
        link = row['link']
        file = open(context.get_share_path(row['filename'])).read()
        sel = scrapy.Selector(Response(file, link))

        title = ' '.join(sel.xpath('//h1/text()').get())
        description = "" + sel.xpath(
            "normalize-space(string(//div[@id = 'content_anchor']))"
        ).get()

        description = re.sub(r'window.adminAccountId=.*;', '', description)

        keys = sel.xpath(
            "//div[@id = 'characteristics_anchor']//span[contains(@class, 'title') or contains(@class, 'name')]/text()"  # noqa: E501
        ).getall()
        values = sel.xpath(
            "//div[@id = 'characteristics_anchor']//span[contains(@class, 'value')]/text()" # noqa: E501
        ).getall()

        properties = {}
        for key, val in zip(keys, values):
            if key not in properties.keys():
                properties[key] = val

        images = sel.xpath("//div[contains(@class, 'Grid')]//div[contains(@class, 'gallery_Gallery__picList')]//picture//img/@src").getall()   # noqa: E501
        images.extend(sel.xpath("//div[@id = 'content_anchor']//img/@src").getall())

        if output_type == 'json':
            text = json.dumps(
                {
                    'title': title,
                    'description': description,
                    'properties': properties
                }
            )
        else:
            text = (
                f'Title:\n{title}\n\n'
                f'Description:\n{description}\n\n'
                f'Properties:\n{properties}\n\n'
            )



        for image in images[:max_results]:
            image_df.append([link, image])

        text_df.append([
            link,
            text
        ])

        for key in properties.keys():
            props_df.append([link, key, properties[key]])

    return_df = []

    if imgs_only:
        return_df.append(pd.DataFrame(image_df, columns=["link", "image"]))

    elif props_only:
        return_df.append(pd.DataFrame(props_df, columns=["link", "key", "val"]))

    else:
        return_df.extend([
            pd.DataFrame(text_df, columns=["link", "text"]),
            pd.DataFrame(image_df, columns=["link", "image"]),
            pd.DataFrame(props_df, columns=["link", "name", "value"])
        ])

    return return_df
