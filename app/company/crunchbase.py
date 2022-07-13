from urllib.parse import urljoin
import requests


def get_company_data(company: dict):
    if company.get('error'):
        return {}
    if company.get('properties'):
        company = company['properties']

    return {
        'uuid': company['identifier'].get('uuid'),
        'name': company['identifier'].get('value'),
        'image_url': company['identifier'].get('image_id'),
        'description': company.get('short_description')
    }


class Crunchbase:
    host = "https://crunchbase-crunchbase-v1.p.rapidapi.com/"
    headers = {"X-RapidAPI-Host": "crunchbase-crunchbase-v1.p.rapidapi.com",
               "X-RapidAPI-Key": "d899ed6582msh662b17611a43bedp1c8dc6jsn9ae5e92f948b"}

    @classmethod
    def request_autocomplete(cls, query: str):
        url = urljoin(cls.host, "/autocompletes")
        response = requests.get(url, headers=cls.headers,
                                params={'query': query, 'limit': 8})
        return response.json()

    @classmethod
    def search(cls, query):
        cb = cls.request_autocomplete(query)
        try:
            return [get_company_data(company) for company in cb['entities']]
        except KeyError:
            return {}

    @classmethod
    def request_entity(cls, uuid: str):
        url = urljoin(cls.host, f"/entities/organizations/{uuid}")
        response = requests.get(url, headers=cls.headers,
                                params={'field_ids': 'website_url,short_description'})
        return response.json()

    @classmethod
    def get_company(cls, uuid):
        company = cls.request_entity(uuid)
        return get_company_data(company)


if __name__ == '__main__':
    print(Crunchbase.search('apple'))
    print(Crunchbase.get_company('7063d087-96b8-2cc1-ee88-c221288acc2a'))
