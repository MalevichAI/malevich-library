import hashlib
import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor

import pandas as pd
import requests
import scrapy
from fake_useragent import UserAgent
from malevich.square import APP_DIR, DF, Context, processor, scheme
from pydantic import BaseModel
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


@scheme()
class AliLink(BaseModel):
    link: str

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

ALL_CHARS_SCRIPT = """
    var click_event = new Event("click", { bubbles: true, cancelable: false });
    var all = document.evaluate("//div[@id = 'characteristics_anchor']//div[text()]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (all != null){
        all.dispatchEvent(click_event);
    }
"""  # noqa: E501

class Response:
    def __init__(self, text, url, captcha=False) -> None:
        self.text = text
        self.url = url
        self.captcha = captcha


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--user-agent={UserAgent(browsers=['chrome']).random}")  # noqa: E501
    return webdriver.Chrome(options)


def get_page_(link: str, sp_conf) -> str:
    driver = init_driver()
    driver.delete_all_cookies()
    successful = False
    captcha = False
    time_out = 5
    for _ in range(5):
        try:
            driver.get(link)

            sel = scrapy.Selector(Response(text=driver.page_source, url=link))
            not_exist = sel.xpath("//h1[contains(@class, 'PageNotFound')]")

            if len(not_exist) > 0:
                return "404", False

            WebDriverWait(driver, time_out).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//div[@id = 'content_anchor']")
                )
            )
            try:
                if sp_conf.get("browser_language", "ru") == "en":
                    driver.execute_script(TO_EN_SCRIPT)
                    WebDriverWait(driver, 15).until(
                        expected_conditions.presence_of_element_located(
                            (
                                By.XPATH,
                                "//div[@id = 'content_anchor']/h2[text() = 'Description']", # noqa: E501
                            )
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
        res_ = "CAPTCHA" if captcha else "Error"
        return res_, False

    driver.execute_script(ALL_CHARS_SCRIPT)
    filename = hashlib.sha256(link.encode()).hexdigest() + ".html"

    with open(os.path.join(APP_DIR, filename), "w") as f:
        f.write(driver.page_source)

    cards = False
    try:
        driver.find_element(By.XPATH, "//div[@data-spm = 'sku_floor']//ul")
        cards = True
    except NoSuchElementException:
        print('Page has no cards')
        ...

    return filename, cards


@processor()
def get_page_ali(df: DF[AliLink], context: Context):
    """
    Get aliexpress page and write it to the html file.

    ## Input:

    A DataFrame with column:
        - link (str): Aliexpress link.

    ## Output:

    Two DataFrames, first DataFrame with columns:
        - link (str): Aliexpress link.
        - filename (str): Filename to which page is saved.
        - cards (bool): Is there variant cards in the page.

    ---

    Second one is an error DataFrame with columns:
        - link (str): Aliexpress link.
        - error (str): Which error ocurred while trying to get page.

    -----

    Args:
        df(DF[AliLink]) A dataframe with links.

    Returns:
        Dataframes with filenames and errors.
    """
    sp_conf = context.app_cfg.get("spider_cfg", {})
    processes = []

    with ProcessPoolExecutor(multiprocessing.cpu_count()) as executor:
        errors = []
        outputs = []
        for link in df["link"].to_list():
            task = executor.submit(get_page_, link=link, sp_conf=sp_conf)
            processes.append((link, task))

        for link, task in processes:
            response, cards = task.result()
            if response == "404" or response == "CAPTCHA":
                errors.append([link, response])
            else:
                context.share(response)
                outputs.append([link, response, cards])

    return (
        pd.DataFrame(outputs, columns=["link", "filename", "cards"]),
        pd.DataFrame(errors, columns=["link", 'error'])
    )

@processor()
def get_page(df: DF, ctx: Context):
    """
    Get pages from web and write it to the html file.

    ## Input:

    A DataFrame with column:
        - link (str): page link.

    ## Output:

    Two DataFrames, first DataFrame with columns:
        - link (str): Aliexpress link.
        - filename (str): Filename to which page is saved.

    ---

    Second one is an error DataFrame with columns:
        - link (str): Aliexpress link.
        - status_code (str): Response status code.


    ## Configuration:
        - follow_redirects: bool, default False.
            Follow redirect if 3xx code is received.
    -----

    Args:
        df: A dataframe with links.

    Returns:
        Dataframes with filenames and errors.
    """
    out = []
    err = []
    for link in df['link'].to_list():
        response = requests.get(
            link, allow_redirects=ctx.app_cfg.get('follow_redirects', False)
        )
        if response.status_code < 200 or response.status_code >= 300:
            err.append([link, response.status_code])
            continue
        data = response.text
        filename = hashlib.sha256(link.encode()).hexdigest() + ".html"
        with open(
            os.path.join(
                APP_DIR,
                filename
            ), 'w'
        ) as f:
            f.write(data)
        out.append([link, filename])
        ctx.share_many([x[1] for x in out])
    return (
        pd.DataFrame(out, columns=['link', 'filename']),
        pd.DataFrame(out, columns=['link', 'status_code'])
    )
