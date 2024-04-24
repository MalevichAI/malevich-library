import re
import string

import pandas as pd
import scrapy
from fake_useragent import UserAgent
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By

from .models import ScrapeAliexpress


def get_cards(driver: webdriver.Chrome):
    chars_data = {}

    chars = driver.find_elements(
        By.XPATH,
        "//div[contains(@exp_attribute, 'sku_attr')]/div[contains(@class, 'skuProp')]"
    )

    for i in range(len(chars)):
        prop_name = driver.find_element(
            By.XPATH,
            "//div[contains(@exp_attribute, 'sku_attr')]/"
            f"div[contains(@class, 'skuProp')][{i+1}]/div/span"
        ).text.strip(':')

        if prop_name not in chars_data.keys():
            chars_data[prop_name] = []

        variants = driver.find_elements(
            By.XPATH,
            "//div[contains(@exp_attribute, 'sku_attr')]"
            f"/div[contains(@class, 'skuProp')][{i+1}]//ul/li/button"
        )
        for j in range(len(variants)):
            driver.execute_script(
                f"""
                var click_event = new Event(
                    "click",
                    {{ bubbles: true, cancelable: false }}
                )
                var button = document.evaluate(
                    "(//div[contains(@class, 'skuProp')])[{i+1}]//ul/li/button[@id = 'SkuPropertyValue-{j}']",
                    document.body,
                    null,
                    XPathResult.FIRST_ORDERED_NODE_TYPE,
                    null
                ).singleNodeValue
                button.dispatchEvent(click_event)
                """  # noqa: E501
            )
            prop = driver.find_elements(
                By.XPATH,
                "(//div[contains(@exp_attribute, 'sku_attr')]"
                f"/div[contains(@class, 'skuProp')])[{i+1}]/div/span"
            )
            chars_data[prop_name].append(prop[1].text)
    return chars_data

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

@processor()
def scrape_aliexpress(
        scrape_links: DF[ScrapeLinksAli],
        context: Context[ScrapeAliexpress]
    ):
    """Scrapes aliexpress.

    ## Input:

        A dataframe with a column:
        - `link` (str): containing web links to be scraped

    ## Output:
        Depends on the configuration, processor returns from 2 to 5 DataFrames.

        By default, it returns 5 DataFrames: text, images, properties, cards and errors.

        Each DataFrame has a `link` column. And depend on the DataFrame, it has its own columns.
        For example: Image DataFrame has two columns: `link` and `image`.

        ---

        If `properties_only` is True, processor will return 2 DataFrames: properties and errors.
        Same situation when `images_only` will be set to True.


    ## Configuration:
         - `allowed_domains`: list[str], default None.
            A list of allowed domains to scrape.
            If not provided, all domains are allowed, so the app will traverse the entire web. Otherwise, the scraper won't visit external links.

            Example:

                1. allowed_domains: ["example.com"]
                2. allowed_domains: ["example.com", "malevich.ai"]
                3. allowed_domains: []

                In the case (1), the app will only visit links from
                https://www.example.com and its subdomains.

                In the case (2), the app will only visit links from
                https://www.example.com and may jump to https://www.malevich.ai or its
                subdomains or vice versa.

                In the case (3), the app will traverse the entire web as it
                is equivalent to not providing the option. In this case the app
                halts when either `max_depth` or `max_results` is reached. Be sure
                to provide at least one of these options.

            Default:

                By default, `allowed_domains` is set to an empty list, so the
                app will traverse the entire web.


        - `max_depth`: int, default 0.
            The maximum depth to traverse the web.
            If not provided, the app will traverse the entire web.

            Example:

                1. max_depth: 1
                2. max_depth: 0 (equivalent to not providing the option)
                3. max_depth: 2

                In case (1), the app will only visit links from the provided
                links

                In case (2), the app will traverse the entire web as it
                is equivalent to not providing the option. In this case the app
                halts when either all links if `allowed_domains` are exhausted
                or `max_results` is reached. Be sure to provide at least one of
                these options.

                In case (3), the app will visit links from the provided links
                and links found in the given ones.

        - `spider_cfg`: dict, default {}.
            A dictionary of configuration options for the spider.
            If not provided, the app will use the default configuration for each
            spider. See [Available Spiders] for more information.


        - `max_results`: int, default None.
            The maximum number of results to return.
            If not provided, the app will return all results.

            Example:

                1. max_results: 100
                2. max_results: 0 (equivalent to not providing the option)
                3. max_results: 2

                In case (1), the app will return exactly 100 results.

                In case (2), the app will return all results. The number
                is then unbounded.


        - `timeout`: int, default 0.
            The maximum number of seconds to wait for collecting responses from the spiders.

            Example:

                1. timeout: 10
                2. timeout: 0 (equivalent to not providing the option)

                In case (1), the app will wait for 10 seconds for the spider
                to finish.

                In case (2), the app will wait indefinitely for the spider
                to finish. In this case the app halts when either all links if
                `allowed_domains` are exhausted or `max_results` is reached.
                Be sure to provide at least one of these options.

            Default:

                By default, the app will wait for 120 seconds for the spider
                to finish.


        - `squash_results`: bool, default False.
            If set, the app will squash the results into a single string separated by the `squash_delimiter` option.

            Example:

                Assuming the app obtained the following results:

                | result |
                |--------|
                |   a    |
                |   b    |
                |   c    |

                1. squash_results: true, squash_delimiter: ','
                2. squash_results: true, squash_delimiter: '\\n'
                3. squash_results: false

                In case (1), the app will return a dataframe with a single row
                with the following result:

                | result |
                |--------|
                | a,b,c  |

                In case (2), the app will return a dataframe with a single row
                with the following result:

                | result |
                |--------|
                | a\\nb\\nc|

                In case (3), the app will return a dataframe with three rows
                with the following results:

                | result |
                |--------|
                |   a    |
                |   b    |
                |   c    |


        - `delimiter`: str, default "'\\n'".
            The delimiter to use when squashing the results or when using independent crawl.
            See `squash_results` and `links_are_independent` option for more information.

            Default:

                By default, the app will use the newline character as the
                delimiter.

        - `links_are_independent`: bool, default False.
            If set, the app will crawl each link independently.
            Otherwise, the app will assume all links comprise a single corpus and will crawl them together.

    ## Spider Options:

        - output_type (str):
            The output can be in 2 types:
                JSON ('json'):

                    {
                        "title" : "Product_Title",
                        "description": "Product description",
                        "properties": "<key1>: <value1>, <key2>: <value2>, ..."
                        "images": ["image_link1", "image_link2", ...]
                    }

                Text ('text'):

                    title:
                    Product_Title

                    description:
                    Product description

                    properties:
                    <key1>: <value1>, <key2>: <value2>, ... <keyN>: <valueN>

                    images:
                    "image_link1", "image_link2", ...
                    "

            Default value is 'json'

            Example:
                spider_cfg = {output_type: 'text'}

        - only_images (bool):
            Get only product image links

            Default value is False

        - only_properties (bool):
            Get only product properties

            Default value is False

        - browser_language (str):
            Set language of the product page

            There are 2 options:
                'en' for English
                'ru' for Russian

            Default value is 'ru'

    -----

    Args:
        scrape_links (DF[ScrapeLinksAli]): A dataframe with a column named `link` containing web links.
        context: The configuration dictionary. See [Available Options] for more information.

    Returns:
        A dataframe with a textual column named `result`
    """ # noqa: E501
    sp_conf = context.app_cfg.get('spider_cfg', {})
    max_results = context.app_cfg.get('max_results', None)
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--user-agent={UserAgent(browsers=['chrome']).random}")  # noqa: E501
    driver = webdriver.Chrome(options)

    text_df = []
    image_df = []
    card_df = []
    props_df = []
    for _, row in scrape_links.iterrows():
        link = row['link']
        file = open(context.get_share_path(row['filename'])).read()

        sel = scrapy.Selector(Response(file, link))

        title = ' '.join(sel.xpath('//h1/text()').getall())
        description = "" + sel.xpath(
            "normalize-space(string(//div[@id = 'content_anchor']))"
        ).get()

        description = re.sub(r'window.adminAccountId=.*;', '', description)

        keys = sel.xpath(
            "//div[@id = 'characteristics_anchor']//span[contains(@class, 'name')]/text()"  # noqa: E501
        ).getall()
        values = sel.xpath(
            "//div[@id = 'characteristics_anchor']//span[contains(@class, 'value')]/text()" # noqa: E501
        ).getall()

        properties = {}
        for key, val in zip(keys, values):
            if key not in properties.keys():
                properties[key] = val

        images = sel.xpath("//div[contains(@class, 'gallery_Gallery__picList')]//picture//img/@src").getall()   # noqa: E501
        images.extend(sel.xpath("//div[@id = 'content_anchor']//img/@src").getall())

        text = (
            f'Title:\n{title}\n\n'
            f'Description:\n{description}\n\n'
            f'Properties:\n{properties}\n\n'
        )



        for image in images[:max_results]:
            image_df.append([link, image])

        if sel.xpath("//div[@data-spm = 'sku_floor']//ul").get() is not None:
            try:
                driver.get(f"file://{context.get_share_path(row['filename'])}")
                cards = get_cards(driver)
                cards_str = 'Variants:\n'
                for key in cards.keys():
                    cards_str += key + '\n'
                    for val in cards[key]:
                        cards_str += val + '\n'
                        card_df.append([link, key, val])
                text += cards_str
            except Exception:
                ...
        text_df.append([
            link,
            text
        ])

        for key in properties.keys():
            props_df.append([link, key, properties[key]])

    return_df = []

    if sp_conf.get('only_images', False):
        return_df.append(pd.DataFrame(image_df, columns=["link", "image"]))

    elif sp_conf.get('only_properties', False):
        return_df.append(pd.DataFrame(props_df, columns=["link", "key", "val"]))

    else:
        return_df.extend([
            pd.DataFrame(text_df, columns=["link", "text"]),
            pd.DataFrame(image_df, columns=["link", "image"]),
            pd.DataFrame(props_df, columns=["link", "name", "value"]),
            pd.DataFrame(card_df, columns=["link", "name", "value"])
        ])

    return return_df

@processor()
def get_matches(
    text: DF,
    keys: DF,
    vals: DF,
    kvals: DF,
    context: Context
):
    """
    Match key-value in text

    ## Input:
    Four dataframes. First one is Text DataFrame with columns:
        - link (str): Aliexpress Link.
        - text (str): Aliexpress product info.
    ---

    Second one is Keys DataFrame with columns:
        - idx (int): Key ID.
        - key (str): Key name.

    ---

    Third one is Values DataFrame with columns:
        - idx (int): Value ID.
        - value (str): Value name.

    ---

    The last is match DataFrame which contains key -> value mapping.
        - key (int): Key ID.
        - value (int): Value ID.

    ## Output:
    Three DataFrames with results. First DataFrame contains matches.
        - link (str): Aliexpress link.
        - key (int): Key ID.
        - value (int): Value ID.
    ---
    Second one contains not matched keys.
        - link (str): Aliexpress link.
        - key (int): Key ID which wasn't found in the text.
    ---
    Third DF contains not matched values.
        - link (str): Aliexpress link.
        - key (int): Key ID which was found in the text.
        - value (int): Value ID which was not found.
    -----
    Args:
        text(DF): Text DataFrame.
        keys(DF): Keys DataFrame.
        values(DF): Values DataFrame.
        kvals(DF): Key-Values Mapping.
    Returns:
        Match results.
    """
    keys_dict = {}
    vals_dict = {}
    props = {}
    for _, row in keys.iterrows():
        keys_dict[row['idx']] = row['key']

    for _, row in vals.iterrows():
        vals_dict[row['idx']] = row['value']

    for kid in kvals['key'].unique():
        props[kid] = kvals[kvals['key'] == kid]['value'].to_list()

    matches = []
    not_matched_keys = []
    not_matched_value = []

    for _, row in text.iterrows():
        text_:str = row['text'].lower()
        for char in string.punctuation:
            if char in text_:
                text_ = text_.replace(char, ' ')

        for key in props.keys():
            if keys_dict[key].lower() not in text_:
                not_matched_keys.append([row['link'], key])
            else:
                for val in props[key]:
                    if vals_dict[val].lower() in text_:
                        matches.append([row['link'], key, val])
                    else:
                        not_matched_value.append(row['link'], key, val)
    return (
        pd.DataFrame(matches, columns=['link', 'key', 'value']),
        pd.DataFrame(not_matched_keys, columns=['link', 'key']),
        pd.DataFrame(not_matched_value, columns=['link', 'key', 'value'])
    )
