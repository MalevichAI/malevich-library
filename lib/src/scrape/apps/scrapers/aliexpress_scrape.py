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

        A dataframe with a column:
        - `link` (str): containing web links to be scraped

    ## Output:
        Depends on the configuration, processor returns from 2 to 5 DataFrames.

        By default, it returns 3 DataFrames: text, images, properties.

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

    text_df = []
    image_df = []
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

    if sp_conf.get('only_images', False):
        return_df.append(pd.DataFrame(image_df, columns=["link", "image"]))

    elif sp_conf.get('only_properties', False):
        return_df.append(pd.DataFrame(props_df, columns=["link", "key", "val"]))

    else:
        return_df.extend([
            pd.DataFrame(text_df, columns=["link", "text"]),
            pd.DataFrame(image_df, columns=["link", "image"]),
            pd.DataFrame(props_df, columns=["link", "name", "value"])
        ])

    return return_df
