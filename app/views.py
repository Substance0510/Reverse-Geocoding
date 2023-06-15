from flask import request
from flask_restful import Resource
from app import api, db
from app.models import Task
from app.utils import create_point_pairs
from app.tasks import save_task, get_task


class CalculateDistancesAPI(Resource):
    def post(self):
        # Get the uploaded file from the request
        uploaded_file = request.files['file']

        # Check if a file was uploaded
        if not uploaded_file:
            return {"error": "No file provided"}, 400

        # Read the CSV data from the file
        csv_data = uploaded_file.read().decode('utf-8')

        # Create point pairs
        point_pairs = create_point_pairs(csv_data)

        # Save task and return task_id
        task_id = "<XXXX>"
        status = "running"
        save_task(task_id, status, data=None)

        return {"task_id": task_id, "status": status}, 200


class GetResultAPI(Resource):
    def get(self):
        task_id = request.args.get('task_id')

        # Get task by task_id
        task = get_task(task_id)

        if task:
            return {"task_id": task.task_id, "status": task.status, "data": task.data}, 200
        else:
            return {"error": "Task not found"}, 404


api.add_resource(CalculateDistancesAPI, '/api/calculateDistances')
api.add_resource(GetResultAPI, '/api/getResult')
