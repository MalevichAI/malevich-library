import os
import re
from hashlib import sha256

import pandas as pd
import scrapy
from fake_useragent import UserAgent
from malevich.square import APP_DIR, DF, Context, processor
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from .models import ScrapeWildberries

SCRIPT = """
var expr = "//button[contains(@class, 'detail')]"
var click_event = new Event("click", { bubbles: true, cancelable: false });
var all_chars = document.evaluate(expr, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
var resp = all_chars.dispatchEvent(click_event)
"""  # noqa: E501

class Response:
    def __init__(self, text, url) -> None:
        self.text = text
        self.url = url
        self.encoding = 'utf-8'

@processor()
def get_page_wb(df: DF, ctx: Context):
    """
    Get Wildberries product page.

    ## Input:

    A single DataFrame with one column:
        - `link` (str): Link to the WB product.

    ## Output:

    A single DataFrame with two columns:
        - `link` (str): Link to the WB product.
        - `filename` (str): HTML File with product content.
    -----
    Args:
        df(DF): DF with products.
    Returns:
        DF with files.
    """
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--user-agent={UserAgent(browsers=['chrome']).random}")  # noqa: E501
    driver = Chrome(options)
    driver.execute_cdp_cmd(cmd="Network.clearBrowserCache", cmd_args={})
    wait = WebDriverWait(driver, 2)

    outs = []

    for link in df['link'].to_list():
        driver.get(link)
        try:
            wait.until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, '//button[contains(@class, "detail")]')
                )
            )
            driver.execute_script(
                SCRIPT
            )
            wait.until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, '//p[@class = "option__text"]')  # noqa: E501
                )
            )
        except TimeoutException:
            ...
        path = sha256(link.encode()).hexdigest() + '.html'
        with open(os.path.join(APP_DIR, path), 'w') as f:
            f.write(driver.page_source)
        ctx.share(path)
        outs.append([link, path])
    return pd.DataFrame(
        outs,
        columns=['link', 'filename']
    )

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
        - output_type: str, default 'text'.
            Format of text data. Either 'text' or 'json'.
    -----
    """  # noqa: E501
    max_results = context.app_cfg.get('max_results', 3)
    image_df = []
    props_df = []

    for _, row in df.iterrows():
        link = row['link']
        page = open(context.get_share_path(row['filename'])).read()
        sel = scrapy.Selector(text=page)
        props_df.append(
            [
                link,
                'title',
                sel.xpath("//h1[contains(@class, 'title')]/text()").get()
            ]
        )
        props_df.append(
            [
                link,
                'description',
                sel.xpath(
                    '//p[@class = "option__text"]/text()'
                ).get()
            ]
        )
        props_df.append(
            [
                link,
                'internal_pim_id',
                sel.xpath(
                    '//div[@class="product-page"]//table//td[1]/span/text()'
                ).get()
            ]
        )
        props_df.append(
            [
                link,
                'brand',
                sel.xpath(
                    "//div[@class='product-page__header']/a/text()"
                ).get()
            ]
        )
        props_df.append(
            [
                link,
                'price',
                sel.xpath(
                    "//div[contains(@class, 'aside')]"
                    "//span[contains(@class, 'price')]/ins/text()"
                ).get().strip()
            ]
        )
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

        images = sel.xpath('//ul[contains(@class, "swiper")]//img[contains(@src, "https://")]/@src').getall()
        for i in range(0, min(max_results, len(images))):
            image_df.append([link, images[i]])

    return [
        pd.DataFrame(image_df, columns=['link', 'image']),
        pd.DataFrame(props_df, columns=['link', 'key', 'value'])
    ]
