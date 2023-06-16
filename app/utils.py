import csv
import requests
from os import path, makedirs, remove
from itertools import combinations
from werkzeug.utils import secure_filename
from geopy.distance import geodesic

from app import app


def get_points(file_path):
    points = {}
    points_addresses = []

    with open(file_path, 'r') as f:
        csv_data = f.read()
        csv_reader = csv.reader(csv_data.splitlines())
        next(csv_reader)

        for point_data in csv_reader:
            name = point_data[0]

            latitude, longitude = validate_coordinates(
                point_data[1], point_data[2]
            )

            points[name] = (latitude, longitude)

            adress = get_address(latitude, longitude)
            points_addresses.append({
                'name': name,
                'address': adress,
                'latitude': latitude,
                'longitude': longitude,
            })

    return points, points_addresses


def validate_coordinates(latitude, longitude):
    latitude = float(latitude)
    longitude = float(longitude)

    if not (-90 <= latitude <= 90):
        raise ValueError("Invalid latitude value")
    if not (-180 <= longitude <= 180):
        raise ValueError("Invalid longitude value")

    return latitude, longitude


def save_file(file, filename):
    upload_folder = app.config['UPLOAD_FOLDER']
    makedirs(upload_folder, exist_ok=True)
    file_path = path.join(upload_folder, secure_filename(filename))
    file.save(file_path)
    return file_path


def remove_file(file_path):
    # Here we can add some checks before removing the file
    # or create a cron job to remove old files
    remove(file_path)


def get_address(latitude, longitude):
    api_url = app.config['GEOCODING_API_URL']
    accept_language = 'en-us,en;q=0.5'
    url = f"{api_url}?lat={latitude}&lon={longitude}&format=json&accept-language={accept_language}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        return str(data['display_name'])

    return 'Unknown address'


def get_point_distances(points):
    point_pairs = []

    # Generate pairs of points using itertools.combinations
    for pair in combinations(points, 2):
        point1 = pair[0]
        point2 = pair[1]
        distance = calculate_distance(points[point1], points[point2])
        point_pairs.append({
            'name': f"{point1}{point2}",
            'distance': distance,
        })

    return point_pairs


def calculate_distance(coord1, coord2):
    return round(geodesic(coord1, coord2).meters, 2)
