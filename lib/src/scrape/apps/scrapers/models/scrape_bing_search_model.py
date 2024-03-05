# generated by datamodel-codegen:
#   filename:  scrape_bing_search_model.json
#   timestamp: 2024-03-05T17:40:29+00:00

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ScrapeBingSearch(BaseModel):
    allowed_domains: Optional[List[str]] = Field(
        None, description='A list of allowed domains to scrape'
    )
    max_depth: Optional[int] = Field(
        0, description='The maximum depth to traverse the web'
    )
    spider_cfg: Optional[Dict[str, Any]] = Field(
        {}, description='A dictionary of configuration options for the spider'
    )
    max_results: Optional[int] = Field(
        None, description='The maximum number of results to return'
    )
    timeout: Optional[int] = Field(
        0,
        description='The maximum number of seconds to wait for collecting responses from the spiders',
    )
    squash_results: Optional[bool] = Field(
        False,
        description='If set, the app will squash the results into a single string separated by the `squash_delimiter` option',
    )
    delimiter: Optional[str] = Field(
        "'\n'",
        description='The delimiter to use when squashing the results or when using independent crawl',
    )
    links_are_independent: Optional[bool] = Field(
        False, description='If set, the app will crawl each link independently'
    )
