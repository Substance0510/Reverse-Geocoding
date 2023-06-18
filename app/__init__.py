import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
api = Api()


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/db.sqlite3'
    app.config['GEOCODING_API_URL'] = 'https://nominatim.openstreetmap.org/reverse'
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'

    db.init_app(app)
    api.init_app(app)

    # Create the tables if they don't exist
    with app.app_context():
        # db.drop_all()  # Drop existing tables
        db.create_all()
        db.session.commit()

    from app import views

    return app
