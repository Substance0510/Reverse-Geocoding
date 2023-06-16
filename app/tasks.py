from app import app, db
from app.models import Task
from app.utils import get_points, get_point_distances, remove_file


def create_task(status=False, result=False):
    if not status:
        status = 'running'
    if not result:
        result = {}

    task = Task(status=status, result=result)
    db.session.add(task)
    db.session.commit()
    return task.id, task.status


def update_task(task_id, status, result):
    task = Task.query.filter_by(id=task_id).first()
    task.status = status
    task.result = result
    db.session.commit()


def get_task(task_id):
    return Task.query.filter_by(id=task_id).first()


def proceed_task(task_id, file_path):
    task = get_task(task_id)
    data = {}

    if not task:
        raise ValueError('Task not found')

    points, points_addresses = get_points(file_path)
    data['points'] = points_addresses

    update_task(task_id, 'running', data)

    point_distances = get_point_distances(points)
    data['links'] = point_distances

    update_task(task_id, 'done', data)

    # Remove the file after the task is done
    remove_file(file_path)

    return task.id, task.status
