import pandas as pd
from fake_useragent import UserAgent
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel
from scrapy import Selector
from selenium import webdriver


@scheme()
class YaMarket(BaseModel):
    link: str


class Response:
    def __init__(self, text, url) -> None:
        self.text = text
        self.url = url


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--user-agent={UserAgent(browsers=['chrome']).random}")  # noqa: E501
    return webdriver.Chrome(options)


@processor()
def scrape_yamarket(df: DF[YaMarket], context: Context):
    """
    ## Input:

    ## Output:

    ## Configuration:

    -----
    Args:

    Returns:
    """
    driver = init_driver()
    text = []
    props = []
    images = []
    errors = []
    for link in df["link"].to_list():
        driver.get(link)
        print(driver.page_source)
        sel = Selector(Response(driver.page_source, link))
        if sel.xpath("//header[text() = 'Тут ничего нет']").get() is not None:
            errors.append([link, "404"])
            continue

        title = sel.xpath("//h1[@data-additional-zone = 'title']/text()").get()
        description = sel.xpath(
            "//div[@aria-label = 'product-description']//span/text()"
        ).get()
        char_num = len(sel.xpath("//div[@aria-label = 'Характеристики']/div").getall())
        chars = {}
        for i in range(char_num):
            char_ = sel.xpath(
                "(//div[@data-zone-name = 'ProductSpecsList']//"
                f"div[@aria-label = 'Характеристики']/div)[{i}]//span/text()"
            ).getall()
            if len(char_) == 2:
                if char_[0] not in chars.keys():
                    chars[char_[0]] = char_[1]

        imgs = sel.xpath(
            "//ul[@aria-roledescription = 'carousel']/li//img/@src"
        ).getall()
        text.append([link, f"{title}\n\n{description}"])
        for key, val in chars.items():
            props.append([link, key, val])
        for img in imgs[: context.app_cfg.get("max_results", None)]:
            images.append([link, img])

    return_dfs = []

    if context.app_cfg.get("only_images", False):
        return_dfs.append(pd.DataFrame(images, columns=["link", "image"]))
    elif context.app_cfg.get("only_properties", False):
        return_dfs.append(
            pd.DataFrame(props, columns=["link", "prop_name", "prop_value"])
        )
    else:
        return_dfs.extend(
            [
                pd.DataFrame(text, columns=["link", 'text']),
                pd.DataFrame(images, columns=["link", "image"]),
                pd.DataFrame(props, columns=["link", "prop_name", "prop_value"])
            ]
        )
    return_dfs.append(pd.DataFrame(errors, columns=['link', 'error']))
    return return_dfs
