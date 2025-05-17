import os
from flask import Flask
from db import db
from models import PlayerModel

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.drop_all()      # 🔥 既存テーブル（中のデータも）削除
    db.create_all()    # 🆕 現在のmodels.pyに基づき再作成
    print("テーブル再作成完了")