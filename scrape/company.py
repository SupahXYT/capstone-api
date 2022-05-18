from selenium.common.exceptions import InvalidArgumentException
from urllib.parse import urljoin
from selenium import webdriver
from crunchbase_service import CrunchbaseService
from shared_classes import Policy, Company
from scrape import patterns
from bs4 import BeautifulSoup
import re

MAP = {
    'identifier': 0,
    'device': 1,
    'government_record': 2,
    'protected_characteristic': 3,
    'internet_activity': 4,
    'commercial': 5,
    'geolocation': 6,
    'biometric': 7,
    'employment': 8,
    'education': 9,
    'inference': 10
}

def url_error_handling(fn):
    def check(*args): 
        try: 
            return fn(*args)
        except InvalidArgumentException:
            return None
    return check

# Selenium's html parser is really lacking and only 
# works on element references, which causes a lot of problems
# That's why BeautifulSoup is used instead

class Scraper:
    DRIVER = webdriver.Firefox()

    def __init__(self, uuid):
        self.uuid = uuid
        self.company = Company(uuid=uuid)
        self.policy = Policy(uuid=uuid)

    def find_policy(self):
        self.policy.do_not_sell = self.do_not_sell(
            self.company.url) 
        self.policy.url = self.policy_url(
            self.company.url)
        self.policy.opt_out_url = self.opt_out_url(
            self.company.url) 

        self.policy.third_party_data = self.third_party_data(
            self.policy.url)
        self.policy.categories = self.categories_collected(
            self.policy.url)
        self.policy.profiling = self.profiling(
            self.policy.url)

        self.policy.opt_out_email = self.find_email(
            self.policy.opt_out_url)

    def find_company(self):
        company_data = CrunchbaseService.get_company(self.uuid)

        self.company.name = company_data.get('name')
        self.company.desc = company_data.get('desc')
        self.company.image = company_data.get('image')
        self.company.url = company_data.get('url')
        self.company.policy = self.policy

    def get_company(self) -> Company:
        return self.company

    def get_policy(self) -> Policy:
        return self.policy

    @url_error_handling
    def categories_collected(self, url) -> list: 
        collected = []
        self.DRIVER.get(url)

        for category in patterns.CATEGORIES:
            for pattern in patterns.CATEGORIES[category]:
                if re.search(pattern, 
                                self.DRIVER.page_source, re.IGNORECASE):
                    if MAP[category] not in collected:
                        collected.append(MAP[category])
        return collected

    @url_error_handling
    def third_party_data(self, url) -> bool:
        self.DRIVER.get(url)
        if re.search(r'(?!re)sources', 
                     self.DRIVER.page_source, re.IGNORECASE):
            return True 
        return False

    @url_error_handling
    def profiling(self, url) -> bool:
        self.DRIVER.get(url)
        if re.search(
                r'personalize|profiling|interest', 
                self.DRIVER.page_source, re.IGNORECASE): 
            return True
        return False

    def make_url(self, url):
        base = self.DRIVER.current_url
        return urljoin(base, url)

    # Some privacy policies are hidden behind a wall of choices or 
    # take several steps to reach so this isn't the best solution
    # I don't think there exists a good enough solution without nlp
    @url_error_handling
    def policy_url(self, url) -> str | None:
        self.DRIVER.get(url)
        soup = BeautifulSoup(self.DRIVER.page_source, 'html.parser')

        for link in reversed(soup.find_all('a', href=True)):
            if re.search(r'privacy(?!\s(center|choices))',
                    link.get_text(), re.IGNORECASE):
                return self.make_url(link['href'])
        return None

    @url_error_handling
    def opt_out_url(self, url) -> str | None:
        self.DRIVER.get(url)
        soup = BeautifulSoup(self.DRIVER.page_source, 'html.parser')

        for link in soup.find_all('a', href=True):
            if re.search('do not sell',
                         link.get_text(), re.IGNORECASE):
                return self.make_url(link['href'])
        return None

    @url_error_handling
    def do_not_sell(self, url) -> bool:
        self.DRIVER.get(url)
        soup = BeautifulSoup(self.DRIVER.page_source, 'html.parser')

        for link in soup.find_all('a', href=True):
            if re.search('do not sell',
                         link.get_text(), re.IGNORECASE):
                return True
        return False 

    @url_error_handling
    def find_email(self, url) -> list[str]:
        self.DRIVER.get(url)
        emails = re.findall(
            r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', 
            self.DRIVER.page_source)
        if len(emails) > 3:
            return emails[:3]
        return emails

