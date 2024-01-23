import scrapy.http
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

TO_RU_SCRIPT = """
        var icon_xp = "//div[text() = 'EN']"
        var lang_xp = "//li/div/span/span[text() = 'Русский язык']"
        var click_event = new Event("click", { bubbles: true, cancelable: false });

        var icon = document.evaluate(icon_xp, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
        if (icon == null){
            icon_xp = "//div[text() = 'RU']"
            icon = document.evaluate(icon_xp, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
        }
        var resp = icon.dispatchEvent(click_event)
        icon = document.evaluate(lang_xp, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
        resp = icon.dispatchEvent(click_event)
        """  # noqa: E501

class Selenium:
    def process_request(
        self,
        request: scrapy.Request,
        spider,
        *args,
        **kwargs
    ) -> scrapy.http.Response:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36') # noqa: E501
        driver = webdriver.Chrome(options)
        successful = False
        wait = WebDriverWait(driver, 20)
        for _ in range(5):
            try:
                driver.get(request.url)
                wait.until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "//div[@id = 'content_anchor']")
                        )
                    )
                try:
                    if spider.browser_language == 'en':
                        driver.execute_script(
                            TO_EN_SCRIPT # noqa:E501
                        )
                        wait.until(
                            expected_conditions.presence_of_element_located(
                                (By.XPATH,
                                "//div[@id = 'content_anchor']/h2[text() = 'Description']")  # noqa: E501
                            )
                        )
                except (TimeoutException, WebDriverException):
                    continue
                wait.until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "//div[@id = 'characteristics_anchor']")
                    )
                )
                successful = True
                break
            except (TimeoutException, WebDriverException):
                continue

        if not successful:
            driver.delete_all_cookies()
            raise Exception(
                "After several attempts, the page did not load correctly. Check "
                f"that the link is valid: {request.url}"
            )
        driver.delete_all_cookies()
        return scrapy.http.Response(url=request.url, body=driver.page_source.encode())
