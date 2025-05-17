from db import db

class PlayerModel(db.Model):
    __tablename__ = "penant_players"  # 他アプリと衝突しないようにする

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    trajectory = db.Column(db.Integer, nullable=False, default=2)
    contact = db.Column(db.Integer, nullable=False)
    power = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    arm = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    catch = db.Column(db.Integer, nullable=False)
