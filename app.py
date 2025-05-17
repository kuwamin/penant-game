from flask import Flask, render_template, request
from game import Game
from team import Team
from player import Player
import random

app = Flask(__name__)

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

@app.route('/simulate', methods=['POST'])
def simulate():
    # ユーザー入力からチーム作成
    teamA = Team("あなたのチーム")
    batters = []
    for i in range(1, 10):
        name = request.form.get(f'player{i}')
        stats = generate_random_stats()
        player = Player(name=name, position="野手", is_pitcher=False, stats=stats, position_role="不明")
        teamA.add_player(player)
        batters.append(player)

    dh_index = int(request.form.get("dh_index")) - 1
    dh_player = batters[dh_index]
    teamA.set_lineup_and_defense(batters, dh_player=dh_player)

    # 自動生成チーム（相手）
    teamB = Team("COMチーム")
    pitcherB = Player("エースCOM", "投手", is_pitcher=True, stats={
        "pitch_speed": 150, "control": 75, "stamina": 80, "breaking_ball": 65
    })
    teamB.add_player(pitcherB)
    auto_batters = []
    for i in range(9):
        stats = generate_random_stats()
        p = Player(name=f"COM選手{i+1}", position="野手", is_pitcher=False, stats=stats, position_role="不明")
        teamB.add_player(p)
        auto_batters.append(p)
    teamB.set_lineup_and_defense(auto_batters, dh_player=auto_batters[8])

    # 試合実行
    game = Game(team_home=teamA, team_away=teamB)
    game.play_game()

    result = {
        "teamA": teamA.name,
        "teamB": teamB.name,
        "scoreA": game.score_home,
        "scoreB": game.score_away
    }

    return render_template("result.html", result=result)
