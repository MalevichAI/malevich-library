import multiprocessing
from concurrent.futures import ProcessPoolExecutor

import pandas as pd
import scrapy
from fake_useragent import UserAgent
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

TO_EN_SCRIPT = """
        var ru_xp = "//div[text() = 'RU']"
        var eng_xp = "//li/div/span/span[text() = 'English']"
        var click_event = new Event("click", { bubbles: true, cancelable: false });

        var ru = document.evaluate(ru_xp, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
        console.log(ru)
        if (ru == null){
            ru_xp = "//div[text() = 'EN']"
            ru = document.evaluate(ru_xp, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
            console.log(ru)
        }
        var resp = ru.dispatchEvent(click_event)
        ru = document.evaluate(eng_xp, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
        console.log(ru)
        resp = ru.dispatchEvent(click_event)
        """  # noqa: E501

class Response:
    def __init__(self, text, url, cards={}, captcha=False) -> None:
        self.text = text
        self.url = url
        self.cards = cards
        self.captcha = captcha

@scheme()
class ScrapeLinks(BaseModel):
    link: str


@scheme()
class ScrapeResult(BaseModel):
    result: str

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

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(f"--user-agent={UserAgent(browsers=['chrome']).random}") # noqa: E501
    return webdriver.Chrome(options)

def get_page(link, sp_conf):
    driver = init_driver()
    driver.delete_all_cookies()
    successful = False
    captcha = False
    time_out = 5
    for _ in range(5):
        try:
            driver.get(link)

            sel = scrapy.Selector(Response(text=driver.page_source, url=link))
            not_exist = sel.xpath(
                "//h1[contains(@class, 'PageNotFound')]"
            )

            if len(not_exist) > 0:
                return Response(driver.page_source, link, {})

            WebDriverWait(driver, time_out).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//div[@id = 'content_anchor']")
                    )
                )
            try:
                if sp_conf.get('browser_language', 'ru') == 'en':
                    driver.execute_script(
                        TO_EN_SCRIPT
                    )
                    WebDriverWait(driver, 15).until(
                        expected_conditions.presence_of_element_located(
                            (By.XPATH,
                            "//div[@id = 'content_anchor']/h2[text() = 'Description']") # noqa: E501
                        )
                    )
            except (TimeoutException, WebDriverException):
                continue
            WebDriverWait(driver, time_out).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//div[@id = 'characteristics_anchor']")
                )
            )
            successful = True
            break
        except (TimeoutException, WebDriverException):
            capcha_sel = scrapy.Selector(Response(driver.page_source, link))
            capcha_sel = capcha_sel.xpath(
                "//div[@class = 'scratch-captcha-title']"
            ).getall()
            captcha = False
            if len(capcha_sel) > 0:
                driver.execute_script("localStorage = {}")
                driver.delete_all_cookies()
                captcha = True
            time_out += 5
            continue

    if not successful:
        driver.delete_all_cookies()
        return Response(driver.page_source, link, captcha=captcha)
    return Response(driver.page_source, link, get_cards(driver))

@processor()
def scrape_aliexpress( scrape_links: DF[ScrapeLinks], context: Context):
    """Scrapes aliexpress.

    [Input Format]

        A dataframe with a column named `link` containing web links
        to be scraped

    [Output Format]

        A dataframe with a column named `result` containing the results.
        There is not distinction between results from different links. The
        number of rows in the output dataframe is equal to the number of
        results or is exactly one if `squash_results` option is set.

    [Available Options]
        - allowed_domains (a list of strings)

            A list of allowed domains to scrape. If not provided, all domains
            are allowed, so the app will traverse the entire web. Otherwise,
            the scraper won't visit external links.

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


        - max_depth (integer):

            The maximum depth to traverse the web. If not provided, the app
            will traverse the entire web.

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

        - spider_cfg (dict):

            A dictionary of configuration options for the spider. If not
            provided, the app will use the default configuration for each
            spider. See [Available Spiders] for more information.


        - max_results (integer):

            The maximum number of results to return. If not provided, the app
            will return all results.

            Example:

                1. max_results: 100
                2. max_results: 0 (equivalent to not providing the option)
                3. max_results: 2

                In case (1), the app will return exactly 100 results.

                In case (2), the app will return all results. The number
                is then unbounded.


        - timeout (int):

            The maximum number of seconds to wait for collecting responses
            from the spiders.

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


        - squash_results (bool):

            If set, the app will squash the results into a single string separated
            by the `squash_delimiter` option.

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


        - delimiter (str):

            The delimiter to use when squashing the results or when using independent crawl.
            See `squash_results` and `links_are_independent` option for more information.

            Default:

                By default, the app will use the newline character as the
                delimiter.

        - links_are_independent (bool):

            If set, the app will crawl each link independently. Otherwise, the app
            will assume all links comprise a single corpus and will crawl them
            together.

    [Spider Options]

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
    Args:
        scrape_links (DF[ScrapeLinks]): A dataframe with a column named `link` containing web links.
        context: The configuration dictionary. See [Available Options] for more information.

    Returns:
        A dataframe with a textual column named `result`
    """ # noqa: E501
    sp_conf = context.app_cfg.get('spider_cfg', {})
    max_results = context.app_cfg.get('max_results', None)

    processes = []
    with ProcessPoolExecutor(multiprocessing.cpu_count()) as executor:
        for link in scrape_links['link'].to_list():
            task = executor.submit(get_page, link=link, sp_conf=sp_conf)
            processes.append((link, task))

        text_df = []
        image_df = []
        errors_df = []
        card_df = []
        props_df = []
        for link, task in processes:
            response = task.result()
            cards = response.cards
            sel = scrapy.Selector(response)

            not_found = sel.xpath("//h1[contains(@class, 'PageNotFound')]").getall()
            if len(not_found) > 0:
                errors_df.append([link, "404"])
                continue
            elif response.captcha:
                errors_df.append([link, "captcha"])
                continue

            title = ' '.join(sel.xpath('//h1/text()').getall())
            description = "" + ' '.join(sel.xpath(
                "//div[@id = 'content_anchor']//*[not(self::img) and not(self::script) \
                and not(self::div)]/text()"
            ).getall())

            keys = sel.xpath(
                "//div[@id = 'characteristics_anchor']//span[contains(@class, 'title')]/text()"  # noqa: E501
            ).getall()
            values = sel.xpath(
                "//div[@id = 'characteristics_anchor']//span[contains(@class, 'value')]/text()" # noqa: E501
            ).getall()

            properties = {}
            for key, val in zip(keys, values):
                if key not in properties.keys():
                    properties[key] = val

            images = sel.xpath("//div[@class = 'gallery_Gallery__picList']//picture//img/@src").getall()   # noqa: E501
            images.extend(sel.xpath("//div[@id = 'content_anchor']//img/@src").getall())

            text_df.append([
                link,
                f'Title:\n{title}\n\n' +
                f'Description:\n{description}\n\n' +
                f'Properties:\n{properties}\n\n' +
                'Images:\n' + '\n'.join(images[:max_results])
            ])

            for image in images[:max_results]:
                image_df.append([link, image])

            for key in cards.keys():
                for val in cards[key]:
                    card_df.append([link, key, val])

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

    return_df.append(pd.DataFrame(errors_df, columns=["link", "error"]))

    return return_df
