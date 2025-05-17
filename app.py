from flask import Flask, render_template, request, redirect, url_for
from game import Game
from team import Team
from player import Player

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    # チームと選手をハードコード（後にフォーム入力に変更）
    teamA = Team("Team A")
    teamB = Team("Team B")

    # 投手と野手をそれぞれ登録（仮データ）
    pitcherA = Player("投手A", "投手", is_pitcher=True, stats={"pitch_speed": 150, "control": 80, "stamina": 85, "breaking_ball": 70})
    pitcherB = Player("投手B", "投手", is_pitcher=True, stats={"pitch_speed": 148, "control": 75, "stamina": 80, "breaking_ball": 65})
    teamA.add_player(pitcherA)
    teamB.add_player(pitcherB)

    batter_stats = {"contact": 80, "power": 70, "speed": 70, "arm": 70, "defense": 70, "catch": 70}
    battersA = [Player(f"A野手{i}", "野手", stats=batter_stats, position_role="遊撃手") for i in range(9)]
    battersB = [Player(f"B野手{i}", "野手", stats=batter_stats, position_role="遊撃手") for i in range(9)]
    for b in battersA:
        teamA.add_player(b)
    for b in battersB:
        teamB.add_player(b)

    teamA.set_lineup_and_defense(battersA, dh_player=battersA[8])
    teamB.set_lineup_and_defense(battersB, dh_player=battersB[8])

    game = Game(team_home=teamA, team_away=teamB)
    game.play_game()

    result = {
        "teamA": teamA.name,
        "teamB": teamB.name,
        "scoreA": game.score_home,
        "scoreB": game.score_away
    }
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
