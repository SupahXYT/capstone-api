from app import api
from flask import abort, request
from app.classes.data import NoUserTask, TaskStatus
from shared_classes import Company
from crunchbase_service import CrunchbaseService

def validate_uuid(uuid: str):
    return bool(CrunchbaseService.entity(uuid))

def add_task(uuid: str):
    NoUserTask(uuid=uuid).save()
    return "OK"

def delete_task(uuid: str):
    task = NoUserTask.objects(uuid=uuid).first()
    if not task:
        abort(404)
    task.delete()
    return "OK"

def update_task(uuid: str, body):
    """Updates the status of a task. Currently this is the 
    only reason you'd ever want to update a task."""
    task = NoUserTask.objects(uuid=uuid).first()
    if not task:
        abort(404)
    task.status = body.get('status')
    task.save()
    return 'OK'

def get_task(uuid: str):
    task = NoUserTask.objects(uuid=uuid).first()
    if not task:
        abort(404)
    return "OK"

@api.route('/task/<uuid>', methods=['GET', 'PUT', 'POST', 'DELETE'])
def task(uuid: str):
    if request.method == 'GET':
        return get_task(uuid)
    elif request.method == 'PUT':
        return update_task(uuid, body=request.get_json())
    elif request.method == 'POST':
        return add_task(uuid)
    else:
        return delete_task(uuid)

def _select_tasks(page: int,
                  size: int, *args):
    return NoUserTask.objects.skip(
        page*size).limit(size)

def add_tasks(tasks: list[str]):
    for task in tasks:
        pass

def update_tasks(tasks: list[str]):
    for task in tasks:
        pass

def get_tasks(page: int,
              size: int):
    """Contructs json response containging all tasks and 
    associated company."""
    response = {'tasks': []}

    for task in _select_tasks(page, size):
        task_dict = task.to_mongo().to_dict()
        task_dict.pop('_id')
        response['tasks'].append(task_dict)
    return response

@api.route('/tasks', methods=['GET', 'PUT', 'POST', 'DELETE'])
def tasks():
    if request.method == 'GET':
        page = request.args.get('page')
        size = request.args.get('size')
        if page and size:
            return get_tasks(int(page), int(size))
        else: 
            abort(400)
    return "OK"
