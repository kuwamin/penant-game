import os
from flask import Flask
from db import db
from models import PlayerModel

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    print("テーブル作成完了")