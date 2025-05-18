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

    is_pitcher = db.Column(db.Boolean, default=False)
    pitch_speed = db.Column(db.Integer)
    control = db.Column(db.Integer)
    stamina = db.Column(db.Integer)
    breaking_ball = db.Column(db.Integer)

class SeasonStatModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(
        db.Integer,
        db.ForeignKey('penant_players.id', ondelete="CASCADE"),  # ★重要
        nullable=False
    )
    season = db.Column(db.Integer, default=2025)

    at_bats = db.Column(db.Integer, default=0)
    hits = db.Column(db.Integer, default=0)
    home_runs = db.Column(db.Integer, default=0)
    walks = db.Column(db.Integer, default=0)
    strikeouts = db.Column(db.Integer, default=0)

    player = db.relationship('PlayerModel', backref=db.backref('season_stats', cascade='all, delete-orphan'))

