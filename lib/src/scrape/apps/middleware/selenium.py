import random
import time

import scrapy.http
from fake_useragent import UserAgent
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

class Response(scrapy.http.Response):
    def __init__(self, body, url, cards, *args, **kwargs) -> None:
        super().__init__(
            body=body,
            status=200,
            url=url,
            *args,
            **kwargs
        )
        self.cards = cards

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


class Selenium:
    def process_request(
        self,
        request: scrapy.Request,
        spider,
        *args,
        **kwargs
    ) -> scrapy.http.Response:
        agent = UserAgent(["chrome"], os=['windows'])
        random.seed(0)
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(f'--user-agent={agent.random}')
        driver = webdriver.Chrome(options)
        successful = False
        time_out = 5
        for _ in range(5):
            try:
                driver.get(request.url)
                WebDriverWait(driver, time_out).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "//div[@id = 'content_anchor']")
                        )
                    )
                try:
                    if spider.browser_language == 'en':
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
                time_out += 5
                capcha_sel = scrapy.Selector(
                    Response(driver.page_source, request.url)
                )
                capcha_sel = capcha_sel.xpath(
                    "//div[@class = 'scratch-captcha-title']"
                ).getall()
                if len(capcha_sel) > 0:
                    driver.execute_script("localStorage = {}")
                    driver.delete_all_cookies()
                    driver.execute_cdp_cmd(
                        'Network.setUserAgentOverride',
                        {
                            "userAgent":agent.random,
                            "platform":"Windows"
                        }
                    )
                time.sleep(2 + random.random() * 8)
                continue

        if not successful:
            driver.delete_all_cookies()
            raise Exception(
                "After several attempts, the page did not load correctly. Check "
                f"that the link is valid: {request.url}"
            )
        driver.execute_script('localStorage = {}')
        driver.delete_all_cookies()

        return Response(
            url=request.url,
            body=driver.page_source.encode(),
            cards = get_cards(driver)
        )

