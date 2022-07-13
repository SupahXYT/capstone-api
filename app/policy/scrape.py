import re

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from dataclasses import dataclass, field, asdict


def serialize_policy(policy):
    policy.driver = None
    policy.parser = None
    policy_dict = asdict(policy)
    policy_dict.pop('driver')
    policy_dict.pop('parser')
    return policy_dict


@dataclass
class Policy:
    website_url: str
    policy_url: str = field(init=False)
    driver: webdriver.Firefox = field(repr=False)
    parser: BeautifulSoup = field(repr=False, init=False)
    do_not_sell: bool = field(init=False)
    third_party_data: bool = field(init=False)
    profiling: bool = field(init=False)
    categories: list[str] = field(default_factory=list)
    opt_out_email: list[str] = field(default_factory=list)
    opt_out_url: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.driver.get(self.website_url)
        self.parser = BeautifulSoup(self.driver.page_source, 'html.parser')
        self.do_not_sell = self._do_not_sell()
        self.policy_url = self._policy_url()

        self.driver.get(self.policy_url)
        self.parser = BeautifulSoup(self.driver.page_source, 'html.parser')
        self.third_party_data = self._third_party_data()
        self.profiling = self._profiling()

    def _policy_url(self):
        for tag in reversed(self.parser.findAll('a', href=True)):
            if re.search(r'privacy(?!\s(center|choices))',
                         tag.text, re.IGNORECASE):
                return urljoin(self.website_url, tag['href'])

    def _do_not_sell(self):
        for tag in self.parser.findAll('a', href=True):
            if re.search('do not sell', tag.text, re.IGNORECASE):
                return True
        return False

    def _opt_out_url(self):
        for tag in self.parser.find_all('a', href=True):
            if re.search('do not sell',
                         tag.text, re.IGNORECASE):
                return self.make_url(tag['href'])

    def _third_party_data(self):
        if re.search(r'(?!re)sources',
                     str(self.parser), re.IGNORECASE):
            return True
        return False

    def _profiling(self) -> bool:
        if re.search(
                r'personalize|profiling|interest',
                str(self.parser), re.IGNORECASE):
            return True
        return False


class PolicyWrapper:
    # driver = webdriver.Firefox()
    print('psst')

    def __init__(self):
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=firefox_options)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def get_policy(self, website_url):
        return serialize_policy(Policy(website_url, self.driver))

