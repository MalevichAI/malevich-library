import json
import os

import pandas as pd
from apps.scrape_web import ScrapeLinks, run_spider
from malevich.square import DF, Context, processor


@processor()
def scrape_aliexpress(
    scrape_links: DF[ScrapeLinks],
    context: Context
    ):
    """Scrapes aliexpress.

    [Input Format]

        A dataframe with a column named `link` containing web links
        to be scraped

    [Output Format]
    
        A dataframe with three columns:
            text: json string or text string depending on output_type option
            properties: product properties
            images: product image links
            
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
        A dataframe with three columns:
            text: json string or text depending on output_type option
            properties: product properties
            images: product image links
    """ # noqa: E501
    context.app_cfg['spider'] = 'aliexpress'

    if 'timeout' not in context.app_cfg.keys():
        context.app_cfg['timeout'] = 120

    context.app_cfg['links_are_independent'] = True
    procs, ids = run_spider(scrape_links, context)
    results = []
    timeout = context.app_cfg.get('timeout', 15)
    for proc_, _id in zip(procs, ids):
        proc_.join(timeout * len(procs) if timeout > 0 else None)
        # Raise if proc failed
        if proc_.exitcode != 0:
            # print exception in proc
            proc_.terminate()
            raise Exception(f'''
                            Scraping failed. Exception: {proc_.exception}
                            1. Make sure, that links are valid
                            2. Most likely we faced CAPTCHA. Try again after 1-3 minutes
                            ''')

        assert os.path.exists(f'output-{_id}.json'), \
            "Scraper failed to save the results. Try descresing `max_results` or `timeout` options"  # noqa: E501

        with open(f'output-{_id}.json') as f:
            max_results = context.app_cfg.get('max_results', None)
            # df = pd.read_json(f).to_dict('records')
            data = json.loads(f.read())
            # if max_results == 0:
            #     max_results = len(df)

            # results_ = [item['text'] for item in islice(df, max_results)]
            spider_cfg = context.app_cfg.get('spider_cfg', {})
            for d in data:
                result_ = []
                result_.append(
                    d['text'] if \
                    spider_cfg.get('output_type', 'json') == 'text'\
                    else d['json']
                )
                json_data = json.loads(d['json'])
                result_.append(json_data['properties'])
                result_.append('\n'.join(json_data['images'][:max_results]))
                results.append(
                    pd.DataFrame([result_], columns=['text', 'properties', 'images'])
                )
    results = pd.concat(results, ignore_index=True)
    return results
