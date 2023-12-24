import scrapy.http
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class Selenium:
    def process_request(self, request, spider):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        driver = webdriver.Chrome(options)
        for _ in range(5):
            try:
                driver.get(request.url)
                WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located(
                                (By.XPATH, "//div[@id = 'content_anchor']")
                ))
                break
            except TimeoutException:
                print('Timeout')
            except WebDriverException:
                print('WebDriverException')
        return scrapy.http.Response(url = request.url, body=driver.page_source.encode())
