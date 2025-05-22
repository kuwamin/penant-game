from db import db
from flask import Flask
from models import PlayerModel, SeasonStatModel

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Kouchan2012@penant-db-kuwamin.cvmemimsu60d.ap-southeast-2.rds.amazonaws.com:5432/penant-db-kuwamin"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    print("✅ DBテーブル作成完了")
