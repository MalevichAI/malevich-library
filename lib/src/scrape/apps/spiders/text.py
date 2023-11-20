import scrapy
import scrapy.http


class TextSpider(scrapy.Spider):
    name = 'text'

    def __init__(
        self,
        start_urls=None,
        allowed_domains=None,
        min_text_length=0,
        max_text_length=65536,
        *args,
        **kwargs
    ) -> None:
        super().__init__(self.name)
        self.start_urls = start_urls or []
        self.allowed_domains = allowed_domains
        self.min_text_length = min_text_length
        self.max_text_length = max_text_length

    def parse(self, response: scrapy.http.Response):
        # Extract text using CSS selectors
        for text in response.css('body *:not(script):not(style)::text').getall():
            if text.strip():  # Check if the text is not just whitespace
                l = len(text.strip())
                if l < self.min_text_length:
                    continue
                if l > self.max_text_length:
                    continue
                yield {'text': text.strip()}

        # Follow links to the next page
        next_pages = response.css('a::attr(href)').getall()
        for next_page in next_pages:
            if next_page is not None:
                yield response.follow(next_page, self.parse)
