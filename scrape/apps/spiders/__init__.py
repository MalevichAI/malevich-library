from .text import TextSpider
from .linked_in_profiles import LinkedInPeopleSpider
from .linked_in_org import LinkedInCompanySpider

SPIDERS = {
    'text': TextSpider,
    'linkedin_people_profile': LinkedInPeopleSpider,
    'linkedin_company_profile': LinkedInCompanySpider
}