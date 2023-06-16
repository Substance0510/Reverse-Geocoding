import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/db.sqlite3'
app.config['GEOCODING_API_URL'] = 'https://nominatim.openstreetmap.org/reverse'
db = SQLAlchemy(app)
api = Api(app)

from .models import Task  # Import the Task model

# Create the tables if they don't exist
with app.app_context():
    # db.drop_all()  # Drop existing tables
    db.create_all()
    db.session.commit()

from . import views  # Import views after creating tables to avoid circular imports
