from app import api
from shared_classes import Policy, Company
from app.classes.data import QueueRequest
# load balancer or something should go here, persistant storange 
# should be in the form of an sqlite database or something 
@api.route('/queue/<uuid>')
def add_to_queue(uuid):
    if (not Policy.objects(uuid=uuid) 
    and not QueueRequest.objects(uuid=uuid)):
        QueueRequest(uuid=uuid).save()
    return "OK"

