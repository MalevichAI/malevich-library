import json

import pandas as pd
import requests
import scrapy
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel

from .models import ScrapeYamarket, ScrapeYamarketApi


@scheme()
class YaMarket(BaseModel):
    offer_id: str


@processor()
def scrape_yamarket_api(df: DF[YaMarket], context: Context[ScrapeYamarketApi]):
    """Scrape Yandex Market using API
    ## Input:
        A dataframe with a single column:
        - offer_id (str): Product SKU vendor code.

    ## Output:
        A dataframe with columns:
        - offer_id (str): Product SKU vendor code.
        - name (str): Product name.
        - description (str): Product description.
        - image (str): Product image links

    ## Configuration:
        - business_id: str.
            Yandex Market business_id.
        - api_token: str.
            Yandex Market API token.
        - max_image_links: int, default None.
            Max amount of images per product.
    -----
    """
    business_id = context.app_cfg.get('business_id', None)
    assert business_id, "Must provide Business_ID"

    api_token = context.app_cfg.get("api_token", None)
    assert api_token, "Must provide API Token"

    max_results = context.app_cfg.get("max_image_links", None)

    response = json.loads(
        requests.post(
            f'https://api.partner.market.yandex.ru/businesses/{business_id}/offer-mappings',
            headers={
                "Authorization": f"Bearer {api_token}"
            },
            json={
                'offerIds': df['offer_id'].to_list()
            }
        ).text
    )
    outputs = []
    for item in response['result']['offerMappings']:
        item_offer = item["offer"]
        outputs.append(
            [
                item_offer['offerId'],
                item_offer['name'],
                item_offer['description'],
                '\n'.join(item_offer['pictures'][:max_results])
            ]
        )
    return pd.DataFrame(outputs, columns = ['offer_id', 'name', 'description', 'image'])


@processor()
def scrape_yamarket(df: DF, ctx: Context[ScrapeYamarket]):
    """
    Scarpe Yandex Market Product Card

    ## Input:
    A single DataFrame with two columns:
        - link (str): Link to the product
        - filename (str): Filename to which the product was written.

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
    max_results = ctx.app_cfg.get('max_results', 3)
    text_df = []
    image_df = []
    props_df = []

    for _, row in df.iterrows():
        link = row['link']
        page = open(ctx.get_share_path(row['filename'])).read()
        sel = scrapy.Selector(text=page)
        text = ""

        title = sel.xpath("//h1[@data-additional-zone='title']/text()").get()
        if title:
            text += f"Title:\n{title}\n\n"
        desc = sel.xpath(
            'normalize-space(//div[contains(@data-zone-name, "ProductDescription")]'
            '//div[text()]/text())'
        ).get()
        if desc:
            text += f"Description:\n{desc}"

        text_df.append([link, text])

        alls = json.loads(
            sel.xpath(
                '//div[contains(@data-apiary-widget-name, "SpecsList")]'
                '//noframes[@class="apiary-patch"]/text()'
            ).get()
        )

        try:
            alls = alls['collections']['fullSpecs']
            for k, v in alls.items():
                if 'specItems' in v:
                    for item in v['specItems']:
                        props_df.append([link, item['name'], item['value']])
        except KeyError:
            pass

        images = sel.xpath(
                '//div[@data-apiary-widget-name="@card/MediaViewerGallery"]'
                '//img[contains(@src, "https://")]/@src'
            ).getall()
        images.extend(
            sel.xpath('//ul[@role="tablist"]//img[contains(@src, "https://")]/@src').getall()
        )
        for i in range(min(max_results, len(images))):
            image_df.append([link, images[i]])

    return (
        pd.DataFrame(text_df, columns=['link', 'text']),
        pd.DataFrame(image_df, columns=['link', 'image']),
        pd.DataFrame(props_df, columns=['link', 'key', 'value'])
    )
