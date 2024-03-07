from urllib.parse import urlencode

import pandas as pd
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel
from scrapy import Selector
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


@scheme()
class LinkedInProfile(BaseModel):
    link: str

class Response:
    def __init__(self, text, url) -> None:
        self.url = url
        self.text = text

@processor()
def get_people(df: DF[LinkedInProfile], context: Context):
    """
    Get people profiles from link or keyword

    ## Input:

        A dataframe with a single column:

        - `link`(str): Link to search page or keyword for searching.

    ## Output:

        A dataframe with a column:

        - `link`(str): Link with profile.

    ## Configuration:

        - `cookie`: str.
            LinkedIn Session Cookie.

        - `max_pages`: int.
            How many pages to visit.

        - `max_profiles`: int.
            How many profiles to retrieve.
    -----

    Args:
        df(DF[LinkedInProfile]): A dataframe with a single column named 'link'.
    Returns:
        A dataframe with profile links
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:122.0) "
                         "Gecko/20100101 Firefox/122.0")
    driver = webdriver.Chrome(options)
    driver.get('https://www.linkedin.com/')
    driver.add_cookie({
            "name": "li_at",
            "value": context.app_cfg.get('cookie', ''),
            "domain": "linkedin.com"
            })
    profiles = context.app_cfg.get('max_profiles', 10)
    pages = context.app_cfg.get('max_pages', 1)
    people = []
    for link in df['link'].to_list():
        if not link.startswith('http'):
            link = (
                "https://www.linkedin.com/search/results/people/"
                f"?{urlencode({'keywords': link})}"
            )
        driver.get('https://www.linkedin.com/search/results/people/')
        source = driver.page_source
        selector = Selector(Response(source, 'abc'))
        people.extend(
            selector.xpath(
                "//ul[contains(@class, 'result-list')]//"
                "div[@class = 'mb1']//"
                "a[contains(@href, 'miniProfileUrn') and "
                "contains(@class, 'app-aware-link')]/@href"
            ).getall()
        )
        for i in range(2, pages+1):
            driver.get(f'{link}&page={i}')
            try:
                WebDriverWait(driver, 3).until(
                expected_conditions.presence_of_element_located(
                        (
                            By.XPATH,
                            "//ul[contains(@class, 'result-list')]//"
                            "div[@class = 'mb1']//"
                            "a[contains(@href, 'miniProfileUrn') and "
                            "contains(@class, 'app-aware-link')]"
                        )
                    )
                )
            except (TimeoutException, WebDriverException):
                selector = Selector(Response(driver.page_source, 'abc'))
                no_found = selector.xpath("//h2[text() = 'No results found']").getall()
                if len(no_found):
                    print("The last page")
                    break

            selector = Selector(Response(driver.page_source, 'abc'))
            people.extend(
                selector.xpath("//ul[contains(@class, 'result-list')]//"
                    "div[@class = 'mb1']//"
                    "a[contains(@href, 'miniProfileUrn') and "
                    "contains(@class, 'app-aware-link')]/@href"
                ).getall()
            )

    return pd.DataFrame(list(set(people))[:profiles], columns=['link'])


@processor()
def get_linkedin_profile(df: DF[LinkedInProfile], context: Context):
    """
    Get people profiles from link or keyword

    ## Input:

        A dataframe with a single column:

        - `link`(str): Link to LinkedIn profile.

    ## Output:

        A dataframe with a column:

        - `link`(str): Link with profile.

    ## Configuration:

        - `cookie`: str.
            LinkedIn Session Cookie.

    -----

    Args:
        df(DF[LinkedInProfile]): A dataframe with a single column named 'link'.
    Returns:
        A dataframe with profile links
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:122.0) "
                         "Gecko/20100101 Firefox/122.0")
    driver = webdriver.Chrome(options)
    driver.get('https://www.linkedin.com/')
    driver.add_cookie({
        "name": "li_at",
        "value": context.app_cfg.get('cookie', ''),
        "domain": "linkedin.com"
        })
    outputs_users = []
    outputs_exp = []
    for id, link in enumerate(df['link'].to_list()):
        driver.get(link)
        try:
            WebDriverWait(driver, 3).until(
                expected_conditions.presence_of_element_located(
                    (
                        By.XPATH,
                        "//section[div[@id = 'experience']]"
                        )
                )
            )
        except TimeoutException:
            selector = Selector(Response(driver.page_source, 'url'))
            no_found = selector.xpath("//h2[text() = 'No results found']").getall()
            if len(no_found):
                outputs_users.append({
                    'id': id,
                    'name': 'Not found',
                    'position': 'Not found',
                    'about': 'Not_found'
                })
                continue
        print(f"Getting {link}")
        if len(driver.page_source) > 100:
            print("Non-empty")
        else:
            print(driver.page_source)
        selector = Selector(Response(driver.page_source, 'url'))
        data = {}
        data['name'] = str(selector.xpath("//a/h1/text()").get())
        pos = selector.xpath(
        "//div[span/a/h1]/following-sibling::div/text()"
        ).get()
        data['position'] = pos.strip(" \n") if pos is not None else 'Unknown'

        if selector.xpath("//section[div[@id = 'about']]").get() is not None:
            data['about'] = selector.xpath("//section[div[@id = 'about']]/"
                                        "div//span[@aria-hidden = 'true']/text()").get()
        else:
            data['about'] = ''
        data['experience'] = []
        if selector.xpath("//section[div[@id = 'experience']]").get() is not None:
            for exp_num in range(
                1,
                len(selector.xpath("//section[div[@id = 'experience']]/div/ul/li")) + 1
            ):
                exp_ = selector.xpath(
                    "(//section[div[@id = 'experience']]"
                    f"/div/ul/li)[{exp_num}]//span[@aria-hidden = 'true']/text()"
                ).getall()
                data["experience"].append(
                    {
                        'position' : exp_[0] if len(exp_) > 0 else '',
                        'name' : exp_[1] if len(exp_) > 1 else 'Unknown',
                        'duration': exp_[2] if len(exp_) > 2 else 'Unknown',
                        'location': exp_[3] if len(exp_) > 3 else 'Unknown',
                        'summary': ' '.join(exp_[4:]) if len(exp_) > 4 else ''
                    }
                )
        data['education'] = []
        if selector.xpath("//section[div[@id = 'education']]").get() is not None:
            for exp_num in range(
                1,
                len(selector.xpath("//section[div[@id = 'education']]/div/ul/li"))+1
            ):
                exp_ = selector.xpath(
                    "(//section[div[@id = 'education']]"
                    f"/div/ul/li)[{exp_num}]//span[@aria-hidden = 'true']/text()"
                ).getall()
                data["education"].append(
                    {
                        'name' : exp_[0] if len(exp_) > 0 else 'Unknown',
                        'position' : exp_[1] if len(exp_) > 1 else 'Unknown',
                        'duration': exp_[2] if len(exp_) > 2 else 'Unknown',
                        'summary': ' '.join(exp_[3:]) if len(exp_) > 3 else ''
                    }
                )
        outputs_users.append(
            [
                id,
                data['name'],
                data['position'],
                data['about'],
            ]
        )
        for exp_ in data['experience']:
            outputs_exp.append(
                [
                    id,
                    'experience',
                    exp_['name'],
                    exp_['position'],
                    exp_['duration'],
                    exp_['summary']
                ]
            )
        for exp_ in data['education']:
            outputs_exp.append(
                [
                    id,
                    'education',
                    exp_['name'],
                    exp_['position'],
                    exp_['duration'],
                    exp_['summary']
                ]
            )
    return [
            pd.DataFrame(
                outputs_users,
                columns=['id', 'name', "position", 'about']
            ),
            pd.DataFrame(
                outputs_exp,
                columns=['id', 'type', 'name', 'position', 'duration', 'summary']
            )
    ]
