# Reverse Geocoding API

This is a simple RESTful API built with Python Flask framework and Flask-RESTful. It provides reverse geocoding functionality to calculate distances between multiple locations using human-readable addresses.

## Project Structure

The project has the following structure:

project/  
├── app/  
│ ├── init.py  
│ ├── models.py  
│ ├── tasks.py  
│ └── views.py  
├── db/  
│ └── database.db  
├── requirements.txt  
└── run.py  


- The `app/` directory contains the application code, including models, tasks, and views.
- The `db/` directory holds the SQLite database file for task persistence.
- `requirements.txt` lists the project dependencies.
- `run.py` is the entry point to run the API.

## Installation

1. Clone the repository:

$ git clone https://github.com/Substance0510/Reverse-Geocoding.git  
$ cd Reverse-Geocoding

2. Set up a virtual environment (optional but recommended):  
$ python -m venv venv  
$ source venv/bin/activate  

3. Install the dependencies:  
$ pip install -r requirements.txt


## Usage

1. Run the API:

$ python run.py


2. The API will be accessible at `http://localhost:5000`.

## API Endpoints

- **POST `/api/calculateDistances`**: Upload a CSV file with point locations to calculate distances. The CSV file should have the structure: `Point, Latitude, Longitude`. The API will generate readable addresses for each point and all distinct links between points, including distance in meters. It returns a response with the generated task details, including a unique `task_id` and `status`.

- **GET `/api/getResult`**: Retrieve a stored task result object identified by `task_id`. The response includes the task ID, status, and the task result data containing points with their addresses and links with distances.

## Persistence

The task results are persisted in a SQLite database located at `db/database.db`. The `Task` model in `app/models.py` defines the schema for the tasks.

## Database Configuration

By default, the API is configured to use a SQLite database. However, you can modify the database configuration in `app/__init__.py` to use a different database (e.g., PostgreSQL, MySQL) by changing the `SQLALCHEMY_DATABASE_URI` parameter.

## Testing
curl -X POST -F "file=@<path>/test_points.csv" http://localhost:5000/api/calculateDistances  
curl http://localhost:5000/api/getResult?task_id=1

## Dependencies

The project uses the following dependencies:

- Flask: A micro web framework for building the API.
- Flask-RESTful: An extension to Flask for quickly building RESTful APIs.
- Flask-SQLAlchemy: An ORM extension for Flask to work with databases.

For a complete list of dependencies and their versions, refer to the `requirements.txt` file.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
