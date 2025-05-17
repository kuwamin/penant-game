import os
from flask import Flask
from db import db
from models import PlayerModel
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    # データを消さず、列だけ追加
    db.session.execute(text("ALTER TABLE penant_players ADD COLUMN IF NOT EXISTS is_pitcher BOOLEAN DEFAULT FALSE;"))
    db.session.commit()
    print("is_pitcher カラム追加完了")
