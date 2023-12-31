import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
api = Api()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/db.sqlite3'
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'

    db.init_app(app)
    api.init_app(app)

    with app.app_context():
        # Create the db folder if it doesn't exist
        db_folder = os.path.join(app.root_path, '..', 'db')
        os.makedirs(db_folder, exist_ok=True)

        # Create the db.sqlite3 file if it doesn't exist
        db_file = os.path.join(db_folder, 'db.sqlite3')
        if not os.path.isfile(db_file):
            open(db_file, 'a').close()

        db.create_all()
        db.session.commit()

    return app
