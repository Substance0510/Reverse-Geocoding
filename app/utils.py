import csv
from itertools import combinations
from geopy.distance import geodesic
from app.models import Point, Task
from app import db


def create_point_pairs(csv_data, task_id):
    point_pairs = []
    csv_reader = csv.reader(csv_data.splitlines())
    next(csv_reader)  # Skip the header row
    points = list(csv_reader)  # Read all the points from the CSV file

    # Store points and addresses in the database
    for point_data in points:
        name = point_data[0]
        latitude = point_data[1]
        longitude = point_data[2]
        address = get_address(latitude, longitude)  # Call your geocoding function to get the address

        # Create Point object and add it to the database
        point = Point(name=name, latitude=latitude, longitude=longitude, address=address, task_id=task_id)
        db.session.add(point)

    db.session.commit()

    # Generate pairs of points using itertools.combinations
    for pair in combinations(points, 2):
        point1 = pair[0]
        point2 = pair[1]
        point_pairs.append((point1, point2))

    return point_pairs


def calculate_distance(coord1, coord2):
    point1 = tuple(map(float, coord1.split(",")))
    point2 = tuple(map(float, coord2.split(",")))
    return geodesic(point1, point2).miles

