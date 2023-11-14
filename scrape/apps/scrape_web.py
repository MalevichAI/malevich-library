import multiprocessing
import os
import uuid
from itertools import islice

import numpy as np
import pandas as pd
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel

from .lib.crawl import crawl
from .lib.proc import Process
from .spiders import SPIDERS


@scheme()
class ScrapeLinks(BaseModel):
    link: str

@scheme()
class ScrapeResult(BaseModel):
    result: str

@processor()
def scrape_web(
    scrape_links: DF[ScrapeLinks],
    context: Context
):
    """Scrapes web links.

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


        - spider (Spider name)

            The name of the spider to use. See [Available Spiders] for more
            information.

            Default:

                By default, the app will use the `text` spider.


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

                By default, the app will wait for 15 seconds for the spider
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


    [Available Spiders]

        Text Spider

            The text spider extracts textual content from web pages. It
            traverses all HTML elements but scripts and styles.

            To use the text spider, set the `spider` option to `text`.

            < Spider Configuration >

            The text spider accepts the following configuration options:

                - min_text_length (integer):

                    The minimum length of the text to extract. If not set,
                    the text length is not lower bounded.

                    Example:

                    - spider_cfg: { min_text_length: 10 }

                - max_text_length (integer):

                    The maximum length of the text to extract. If not set,
                    the text length is not upper bounded.

                    Example:

                    - spider_cfg: { max_text_length: 100 }


    [Suggestions]

        The general rule of thumb is to provide at least one of the following options:

            - allowed_domains
            - max_depth
            - max_results
            - timeout

        If you don't provide any of these options, the app will traverse the
        entire web which will prevent the app from finishing.

        If you want to scrape a single page, set `max_depth` to 1. This will
        prevent the app from visiting external links.

        If you are using scraper succeded by a LLM, assure that the amount
        of data returned by the scraper is not too large. Otherwise, the LLM
        will fail. For example, if you are using the text spider, set
        `max_text_length` to a reasonable value and control number of results
        using `max_results` option.


    Args:
        scrape_links (DF[ScrapeLinks]): A dataframe with a column named `link` containing web links.
        context: The configuration dictionary. See [Available Options] for more information.

    Returns:
        A dataframe with a textual column named `result`
    """  # noqa: E501

    spider_cls = SPIDERS.get(context.app_cfg.get('spider', 'text'))
    assert spider_cls, 'Spider not found.'

    timeout = context.app_cfg.get('timeout', 15)

    links_are_independent = context.app_cfg.get('links_are_independent', False)

    if links_are_independent:
        links = [[x] for x in scrape_links.link.to_list()]
    else:
        links = [scrape_links.link.to_list()]

    results = []
    procs: list[Process] = []
    ids = []
    for links_batch in links:
        _id = uuid.uuid4().hex
        proc = Process(
            target=crawl,
            kwargs={
                'settings': {
                    'CLOSESPIDER_TIMEOUT': timeout,
                    'CLOSESPIDER_ITEMCOUNT': context.app_cfg.get('max_results', 0),
                    'DEPTH_LIMIT': context.app_cfg.get('max_depth', 1),
                    'FEED_FORMAT': 'json',
                    'FEED_URI': f'output-{_id}.json'
                },
                'spider_cls': spider_cls,
                'start_urls': links_batch,
                'allowed_domains': context.app_cfg.get('allowed_domains', []),
                **context.app_cfg.get('spider_cfg', {})
            }
        )

        proc.start()
        procs.append(proc)
        ids.append(_id)


    for proc_, _id in zip(procs, ids):
        proc_.join()
        # Raise if proc failed
        if proc_.exitcode != 0:
            #print exception in proc
            proc_.terminate()
            raise Exception(f'Scraping failed. {proc_.exception}')

        assert os.path.exists(f'output-{_id}.json'), \
            "Scraper failed to save the results. Try descresing `max_results` or `timeout` options"  # noqa: E501

        with open(f'output-{_id}.json') as f:
            max_results = context.app_cfg.get('max_results', 0)
            df = pd.read_json(f).to_dict('records')
            if max_results == 0:
                max_results = len(df)

            results_ = [item['text'] for item in islice(df, max_results)]
            if context.app_cfg.get('squash_results', True) or links_are_independent:
                results.append(
                    context.app_cfg.get('squash_delimiter', '\n').join(results_)
                )
            else:
                results.extend(results_)

    return pd.DataFrame({'result': results})
