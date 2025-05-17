from flask import Flask, render_template, request, redirect, url_for, flash
from flask import request, redirect, url_for, render_template
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
        name = request.form.get('name')
        contact = int(request.form.get('contact'))
        power = int(request.form.get('power'))
        speed = int(request.form.get('speed'))
        arm = int(request.form.get('arm'))
        defense = int(request.form.get('defense'))
        catch = int(request.form.get('catch'))

        existing = PlayerModel.query.filter_by(name=name).first()
        if existing:
            return render_template("register.html", message=f"{name} はすでに登録されています。")

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
        db.session.commit()
        return render_template("register.html", message=f"{name} を登録しました！")

    return render_template("register.html")

@app.route('/players')
def show_players():
    all_players = PlayerModel.query.all()
    return render_template("players.html", players=all_players)

@app.route('/delete_player/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    player = PlayerModel.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    return redirect(url_for('show_players'))  # ※show_playersに変更済みならそれ

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
    # あなたのチームの仮想投手（今はCOM固定と同様）
    pitcherA = Player("マイチームエース", "投手", is_pitcher=True, stats={
        "pitch_speed": 145, "control": 70, "stamina": 75, "breaking_ball": 60
    })
    teamA.add_player(pitcherA)
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
    teamA.set_lineup_and_defense(teamA.players[1:], dh_player=dh_player)

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
        "scoreB": game.score_away,
        "log": game.log,
        "inning_scores_home": game.inning_scores_home,
        "inning_scores_away": game.inning_scores_away,
        "hits_home": game.hits_home,
        "hits_away": game.hits_away,
        "errors_home": 0,
        "errors_away": 0
    }

    return render_template("result.html", result=result)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

