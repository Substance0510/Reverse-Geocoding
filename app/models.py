from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default="running")
    pairs = db.relationship("Pair", backref="task", lazy=True)

    def __repr__(self):
        return f"<Task {self.id}>"


class Point(db.Model):
    __tablename__ = 'point'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)

    def validate_latitude(self, latitude):
        latitude = float(latitude)
        if not (-90 <= latitude <= 90):
            raise ValueError("Invalid latitude value")
        return latitude

    def validate_longitude(self, longitude):
        longitude = float(longitude)
        if not (-180 <= longitude <= 180):
            raise ValueError("Invalid longitude value")
        return longitude

    def __repr__(self):
        return f"<Point {self.name}>"


class Pair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    distance = db.Column(db.Float)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)

    def __repr__(self):
        return f"<Pair {self.name}>"
