from flask import Flask, render_template, request, redirect, url_for
from models import PlayerModel
from db import db
from game import Game
from team import Team
from player import Player
import random
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def generate_random_stats():
    return {
        "contact": random.randint(50, 90),
        "power": random.randint(50, 90),
        "speed": random.randint(50, 90),
        "arm": random.randint(50, 90),
        "defense": random.randint(50, 90),
        "catch": random.randint(50, 90),
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        messages = []
        for i in range(1, 10):
            name = request.form.get(f'player{i}_name')
            contact = int(request.form.get(f'player{i}_contact'))
            power = int(request.form.get(f'player{i}_power'))
            speed = int(request.form.get(f'player{i}_speed'))
            arm = int(request.form.get(f'player{i}_arm'))
            defense = int(request.form.get(f'player{i}_defense'))
            catch = int(request.form.get(f'player{i}_catch'))

            # 重複チェック
            existing = PlayerModel.query.filter_by(name=name).first()
            if existing:
                messages.append(f"{name} はすでに登録されています。")
                continue

            player = PlayerModel(
                name=name,
                contact=contact,
                power=power,
                speed=speed,
                arm=arm,
                defense=defense,
                catch=catch
            )
            db.session.add(player)
        
        if messages:
            return render_template("register.html", message="\\n".join(messages))
        
        db.session.commit()
        return render_template("register.html", message="登録完了しました。")

    return render_template("register.html")

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

