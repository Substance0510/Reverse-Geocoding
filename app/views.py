from flask import request
from flask_restful import Resource
from app import api
from app.utils import save_file
from app.tasks import create_task, get_task, proceed_task


class CalculateDistancesAPI(Resource):
    def post(self):
        print("Received a POST request to /api/calculateDistances")
        print(request.files)

        # Get the uploaded file from the request
        uploaded_file = request.files['file']

        # Check if a file was uploaded
        if not uploaded_file:
            return {"error": "No file provided"}, 400

        task_id, task_status = create_task()
        file_name = f"points_{task_id}.csv"
        file_path = save_file(uploaded_file, file_name)

        # Create a delayed task
        proceed_task.delay(task_id, file_path)

        return {"task_id": task_id, "status": task_status}, 200


class GetResultAPI(Resource):
    def get(self):
        task_id = request.args.get('task_id')

        # Get task by task_id
        task = get_task(task_id)

        if task:
            return {"task_id": task.id, "status": task.status, "data": task.result}, 200
        else:
            return {"error": "Task not found"}, 404


def initialize_routes(api):
    api.add_resource(CalculateDistancesAPI, '/api/calculateDistances')
    api.add_resource(GetResultAPI, '/api/getResult')


initialize_routes(api)
