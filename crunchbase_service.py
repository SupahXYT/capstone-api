from urllib.parse import urljoin
import requests, json

IMAGEHOST = 'https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco,dpr_1/'

class CrunchbaseService:
    HEADERS = {
        "X-RapidAPI-Host": "crunchbase-crunchbase-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "d899ed6582msh662b17611a43bedp1c8dc6jsn9ae5e92f948b"
    }
    BASE_URL = 'https://crunchbase-crunchbase-v1.p.rapidapi.com/'

    @classmethod
    def _autocomplete(cls, query: str):
        response = requests.get(
            urljoin(cls.BASE_URL, "/autocompletes"),
            headers=cls.HEADERS,
            params={
                'query': query,
                'limit': 8
                }).text
        return json.loads(response)

    @classmethod
    def autocomplete(cls, query):
        response = []
        cb_data = cls._autocomplete(query)

        for company in cb_data['entities']:
            name = company['identifier'].get('value')
            desc = company.get('short_description')
            uuid = company['identifier'].get('uuid')
            image = company['identifier'].get('image_id')

            response.append({
                         'name': name, 
                         'desc': desc,
                         'uuid': uuid, 
                         'image': image
                         })
        return response

    @classmethod
    def entity(cls, uuid: str):
        host = urljoin(cls.BASE_URL, "/entities/organizations/")
        response = requests.get(
            f'{host}{uuid}',
            headers=cls.HEADERS,
            params={'field_ids': 'website_url'}).text
        return json.loads(response)['properties']

    @classmethod
    def get_company(cls, uuid: str):
        company_data = cls.entity(uuid)

        return {
            'name': company_data['identifier'].get('value'),
            'desc': company_data.get('short_description'),
            'image': company_data['identifier'].get('image_id'),
            'url': company_data.get('website_url')
        }

