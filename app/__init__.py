from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/database.db'
db = SQLAlchemy(app)
api = Api(app)

# Create the tables if they don't exist
with app.app_context():
    db.create_all()
    db.session.commit()
    db.session.connection().execute(
        db.text('CREATE UNIQUE INDEX idx_unique_point ON point (latitude, longitude)')
    )

from app import views
