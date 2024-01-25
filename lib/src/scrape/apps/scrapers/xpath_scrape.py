from apps.scrape_web import ScrapeLinks, run_spider
from malevich.square import DF, Context, processor


@processor()
def scrape_by_selectors(
    scrape_links: DF[ScrapeLinks],
    context: Context
    ):
    """
    The xPath spider extracts links from web pages using xPath (or CSS) selectors.

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

            The delimiter to use when squashing the results or when using
            independent crawl. See `squash_results` and `links_are_independent`
            option for more information.

            Default:

                By default, the app will use the newline character as the
                delimiter.

        - links_are_independent (bool):

            If set, the app will crawl each link independently. Otherwise, the app
            will assume all links comprise a single corpus and will crawl them
            together.

    [Spider Options]

        - components (list[dict]): a list of rules in the following format:
        [
            {
                "key": <string>,
                "xpath": <string>,
                "css": <string>,
            }
        ]

        where `key` is the name of entity to extract, `xpath` is the xPath selector,
        and `css` is the CSS selector. Either `xpath` or `css` must be provided.

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

    Args:
        scrape_links (DF[ScrapeLinks]): A dataframe with a column named `link` containing web links.
        context: The configuration dictionary. See [Available Options] for more information.

    Returns:
        A dataframe with a textual column named `result`
    """ # noqa: E501
    context.app_cfg['spider'] = 'xpath'
    return run_spider(scrape_links, context)
