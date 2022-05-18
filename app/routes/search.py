from app import api
from shared_classes import Policy
from flask import abort, request
from crunchbase_service import CrunchbaseService, IMAGEHOST

@api.route('/company/search')
def search_company():
    query = request.args.get('q')

    if query:
        response = {'companies': []}
        cb_data = CrunchbaseService.autocomplete(query)

        for company in cb_data:
            policy = Policy.objects(
                uuid=company['uuid']).first()
            if policy:
                company['policy'] = policy.to_mongo().to_dict()
                company['policy'].pop('_id')
            if company.get('image'):
                company['image'] = f'{IMAGEHOST}{company["image"]}'
            response['companies'].append(company)

        return response
    abort(400)

# I don't know if I should include a data broker search 
# @api.route('/broker/search')
# def search_data_broker():

