import csv
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from os import path, makedirs, remove, getcwd
from itertools import combinations
from werkzeug.utils import secure_filename


geolocator = Nominatim(user_agent='reverse-geocoding')


def get_points(file_path):
    points = {}
    points_addresses = []

    with open(file_path, 'r') as f:
        csv_data = f.read()
        csv_reader = csv.reader(csv_data.splitlines())
        next(csv_reader)

        for point_data in csv_reader:
            name = point_data[0]

            if len(point_data) < 3:
                continue

            validated_coordinates = validate_coordinates(
                point_data[1], point_data[2]
            )

            if not validated_coordinates:
                continue

            latitude, longitude = validated_coordinates

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
    try:
        latitude, longitude = float(latitude), float(longitude)
    except ValueError:
        return False  # Invalid coordinates

    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        return False  # Invalid coordinates

    return latitude, longitude


def save_file(file, filename):
    upload_folder = path.join(getcwd(), 'uploads')
    makedirs(upload_folder, exist_ok=True)
    file_path = path.join(upload_folder, secure_filename(filename))
    file.save(file_path)
    return file_path


def remove_file(file_path):
    # Here we can add some checks before removing the file
    # or create a cron job to remove old files
    remove(file_path)


def get_address(latitude, longitude):
    location = geolocator.reverse((latitude, longitude), language='en')
    address = location.address if location else 'Unknown address'

    return address


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
