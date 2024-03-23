import json

import pandas as pd
import requests
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel

from .models import ScrapeYamarketApi


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
