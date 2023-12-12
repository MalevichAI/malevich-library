from .text import TextSpider
from .google import GoogleSpider
from .linked_in_profiles import LinkedInPeopleSpider
from .linked_in_org import LinkedInCompanySpider
from .bing import BingSpider
from .xpath import XpathSpider

SPIDERS = {
    'text': TextSpider,
    'google': GoogleSpider,
    'bing': BingSpider,
    'linkedin_people_profile': LinkedInPeopleSpider,
    'linkedin_company_profile': LinkedInCompanySpider,
    'xpath': XpathSpider
}
