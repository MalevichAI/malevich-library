from .text import TextSpider
from .google import GoogleSpider
from .linked_in_profiles import LinkedInPeopleSpider
from .linked_in_org import LinkedInCompanySpider

SPIDERS = {
    'text': TextSpider,
    'google': GoogleSpider,
    'linkedin_people_profile': LinkedInPeopleSpider,
    'linkedin_company_profile': LinkedInCompanySpider,
}
