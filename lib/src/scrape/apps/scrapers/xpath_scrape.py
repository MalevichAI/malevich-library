import json
import os
from itertools import islice

import pandas as pd
from apps.scrape_web import run_spider
from malevich.square import DF, Context, processor, scheme
from pydantic import BaseModel

from .models import ScrapeBySelectors


@scheme()
class ScrapeLinksXpath(BaseModel):
    link: str


@processor()
def scrape_by_selectors(
    scrape_links: DF[ScrapeLinksXpath],
    context: Context[ScrapeBySelectors]
    ):
    """
    The xPath spider extracts links from web pages using xPath (or CSS) selectors.

    ## Input:

        A dataframe with a column:
        - `link` (str): containing web links to be scraped

    ## Output:

        A dataframe with a column:
        - `result` (str): containing the results.

        There is not distinction between results from different links. The
        number of rows in the output dataframe is equal to the number of
        results or is exactly one if `squash_results` option is set.

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

        - `components`: list[dict], default [].
            A list of components with keys and Xpaths need to be found.

        - `output_type`: str, default 'single_table'.
            Output type of scraping results.
                In case of 'disjoint' will return a DataFrame for every key.
                For 'single_table' will return a DataFrame in format [link, key, value].
                In case of 'json' or 'text' will return a DataFrame in format [link, result].

        - `output_delimeter`: str, default '\\n'.
            If output_type is text, will use this delimeter to combine values.

        - `include_keys`: bool, default False.
            If output_type is text and set to True, will include keys into the text.

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

    ## Spider Options

        - components (list[dict]): a list of rules in the following format:
        [
            {
                "key": <string>,
                "xpath": <string>,
                "css": <string>,
                "join_url": <boolean>,
                "count": <int>
            }
        ]

        where `key` is the name of entity to extract, `xpath` is the xPath selector,
        and `css` is the CSS selector. Either `xpath` or `css` must be provided. If
        `join_url` is True, the scraper will join relative links with the site domain.
        `count` is used to control the number of objects to retrieve.

        - output_format (string): the output format. Valid values are "json" or "text.
            Default: "json".
            If "json", the output will be a JSON object with the following structure:
            {
                <key1>: [<value1>, ..., <valueN>],
                <key2>: [<value1>, ..., <valueN>],
            }

            where `key` is the name of the entity and `value` is the values matched by
            the selector.

            If "text", the output will be a raw text in the following format:

            <key1>:
                <value1>
                ...
                <valueN>
            <key2>:
                <value1>
                ...

            where `key` is the name of the entity and `value` is the values matched by
            the selector. If there are multiple values, they will be separated by a
            newline character. If include_keys is False, the output will be a raw text
            in the following format:

            <value1>
            <value2>
            ...
            <valueN>

        - include_keys (boolean): Include keys into text output. Default is False

    -----

    Args:
        scrape_links (DF[ScrapeLinksXpath]): A dataframe with a column named `link` containing web links.
        context: The configuration dictionary. See [Available Options] for more information.

    Returns:
        A dataframe with a textual column named `result`
    """ # noqa: E501
    context.app_cfg['spider'] = 'xpath'

    if context.app_cfg.get('spider_cfg', None) is None :
            context.app_cfg['spider_cfg'] = {}

    if context.app_cfg.get('components', None) is not None:
        components = context.app_cfg.pop('components')
        if 'components' not in context.app_cfg['spider_cfg']:
            context.app_cfg['spider_cfg']['components'] = components
    else:
        components = context.app_cfg['spider_cfg'].get('components', [])

    if context.app_cfg.get('output_type', None) is not None:
        output_type = context.app_cfg.pop('output_type')
        if 'output_type' not in context.app_cfg['spider_cfg']:
            context.app_cfg['spider_cfg']['output_type'] = output_type
    else:
        output_type = context.app_cfg['spider_cfg'].get('output_type', 'single_table')

    if context.app_cfg.get('include_keys', None) is not None:
        include = context.app_cfg.pop('include_keys')
        context.app_cfg['spider_cfg']['include_keys'] = include

    context.app_cfg['spider_cfg']['output_delim'] = context.app_cfg.get(
        'output_delimeter',
        '\n'
    )

    procs, ids = run_spider(scrape_links, context)
    results = []
    timeout = context.app_cfg.get('timeout', 15)

    if output_type == 'disjoint':
        disjoint = {}
        for component in components:
            disjoint[component['key']] = []

    for proc_, _id in zip(procs, ids):
        proc_.join(timeout * len(procs) if timeout > 0 else None)
        # Raise if proc failed
        if proc_.exitcode != 0:
            proc_.terminate()
            raise Exception(f'Scraping failed. {proc_.exception}')

        assert os.path.exists(f'output-{_id}.json'), \
            "Scraper failed to save the results. Try descresing `max_results` or `timeout` options"  # noqa: E501

        with open(f'output-{_id}.json') as f:
            max_results = context.app_cfg.get('max_results', 0)
            df = pd.read_json(f).to_dict('records')
            if max_results == 0:
                max_results = len(df)

            if output_type == 'disjoint':
                for item in islice(df, max_results):
                    data = json.loads(item['text'])
                    link = item['url']
                    for key, val in data.items():
                        for v in val:
                            disjoint[key].append(
                                [
                                    link,
                                    v
                                ]
                            )

            elif output_type == 'single_table':
                for item in islice(df, max_results):
                    data = json.loads(item['text'])
                    link = item['url']
                    for i, (key, val) in enumerate(data.items()):
                        for v in val:
                            results.append([i, link, key, v])

            else:
                for item in islice(df, max_results):
                    results.append([item['url'], item['text']])

    if output_type == 'disjoint':
        ret = [
            pd.DataFrame(
                val,
                columns=['link', key]
            ) for key, val in disjoint.items()
        ]
        return ret

    return pd.DataFrame(
        results,
        columns=['idx', 'link', 'key', 'value']
        if output_type == 'single_table' else ['link', 'result']
    )
