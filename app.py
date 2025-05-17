from flask import Flask, render_template, request, redirect, url_for, flash
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

@app.route('/players')
def players():
    all_players = PlayerModel.query.all()
    return render_template("players.html", players=all_players)

@app.route('/select_starters', methods=['GET'])
def select_starters():
    players = PlayerModel.query.all()
    return render_template("select_starters.html", players=players)

@app.route('/simulate', methods=['POST'])
def simulate():
    ids = request.form.getlist("starter_ids")
    if len(ids) != 9:
        players = PlayerModel.query.all()
        return render_template("select_starters.html", players=players, error="9人ちょうど選んでください。")

    # 順序を維持して取得
    selected_players_dict = {str(p.id): p for p in PlayerModel.query.filter(PlayerModel.id.in_(ids)).all()}
    ordered_players = [selected_players_dict[pid] for pid in ids]

    teamA = Team("あなたのチーム")
    for p in ordered_players:
        player = Player(name=p.name, position="野手", is_pitcher=False, stats={
            "contact": p.contact,
            "power": p.power,
            "speed": p.speed,
            "arm": p.arm,
            "defense": p.defense,
            "catch": p.catch
        }, position_role="不明")
        teamA.add_player(player)

    dh_player = teamA.players[-1]
    teamA.set_lineup_and_defense(teamA.players, dh_player=dh_player)

    # 相手COMチーム生成（今まで通り）
    teamB = Team("COMチーム")
    pitcherB = Player("エースCOM", "投手", is_pitcher=True, stats={
        "pitch_speed": 150, "control": 75, "stamina": 80, "breaking_ball": 65
    })
    teamB.add_player(pitcherB)
    auto_batters = []
    for i in range(9):
        stats = generate_random_stats()
        p = Player(name=f"COM選手{i+1}", position="野手", is_pitcher=False, stats=stats)
        teamB.add_player(p)
        auto_batters.append(p)
    teamB.set_lineup_and_defense(auto_batters, dh_player=auto_batters[8])

    # 試合開始
    game = Game(team_home=teamA, team_away=teamB)
    game.play_game()

    result = {
        "teamA": teamA.name,
        "teamB": teamB.name,
        "scoreA": game.score_home,
        "scoreB": game.score_away
    }

    return render_template("result.html", result=result)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

