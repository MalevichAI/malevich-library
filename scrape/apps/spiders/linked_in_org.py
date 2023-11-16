import scrapy
import scrapy.http


class LinkedInCompanySpider(scrapy.Spider):
    name = "linkedin_company_profile"

    def parse_response(self, response):
        company_item = {}

        company_item['name'] = \
            response.css('.top-card-layout__entity-info h1::text')\
            .get(default='not-found').strip()
        company_item['summary'] = \
            response.css('.top-card-layout__entity-info h4 span::text')\
            .get(default='not-found').strip()

        try:
            # all company details
            company_details = response.css(
                '.core-section-container__content .mb-2')

            # industry line
            company_industry_line = company_details[1].css(
                '.text-md::text').getall()
            company_item['industry'] = company_industry_line[1].strip()

            # company size line
            company_size_line = company_details[2].css(
                '.text-md::text').getall()
            company_item['size'] = company_size_line[1].strip()

            # company founded
            company_size_line = company_details[5].css(
                '.text-md::text').getall()
            company_item['founded'] = company_size_line[1].strip()
        except IndexError:
            print("Error: Skipped Company - Some details missing")

        yield company_item
