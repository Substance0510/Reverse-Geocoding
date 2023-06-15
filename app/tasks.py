from app import db
from app.models import Task


def save_task(task_id, status, data):
    task = Task(task_id=task_id, status=status, data=data)
    db.session.add(task)
    db.session.commit()


def get_task(task_id):
    return Task.query.filter_by(task_id=task_id).first()
