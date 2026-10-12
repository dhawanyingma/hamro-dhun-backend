import os 

from flask import Flask
from app.extensions import db, migrate
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)
migrate.init_app(app, db)

from app.models.songs import Song
from app import routes