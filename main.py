from player import Player
from team import Team
from game import Game

def create_pitcher(name, stats):
    return Player(name=name, position="投手", is_pitcher=True, stats=stats)

def create_batter(name, position_role, stats):
    return Player(name=name, position="野手", is_pitcher=False, position_role=position_role, stats=stats)

def build_team(name, pitcher_info, batter_infos, dh_index=0):
    team = Team(name)

    # 投手登録
    pitcher = create_pitcher(**pitcher_info)
    team.add_player(pitcher)

    # 野手登録
    batters = []
    for info in batter_infos:
        batter = create_batter(**info)
        team.add_player(batter)
        batters.append(batter)

    # DHを1人選ぶ
    dh_player = batters[dh_index]

    # スタメン設定（投手を除いた9人）
    starters = batters  # 9人想定（DH含む）
    team.set_lineup_and_defense(starters=starters, dh_player=dh_player)

    return team

def main():
    # チームAの選手情報
    teamA_pitcher = {
        "name": "佐藤 太郎",
        "stats": {"pitch_speed": 145, "control": 70, "stamina": 80, "breaking_ball": 60}
    }

    teamA_batters = [
        {"name": "山田 一郎", "position_role": "捕手",   "stats": {"contact": 70, "power": 60, "speed": 65, "arm": 70, "defense": 75, "catch": 80}},
        {"name": "田中 次郎", "position_role": "一塁手", "stats": {"contact": 60, "power": 80, "speed": 50, "arm": 60, "defense": 60, "catch": 65}},
        {"name": "鈴木 三郎", "position_role": "二塁手", "stats": {"contact": 75, "power": 50, "speed": 80, "arm": 65, "defense": 70, "catch": 70}},
        {"name": "高橋 四郎", "position_role": "三塁手", "stats": {"contact": 68, "power": 72, "speed": 55, "arm": 68, "defense": 65, "catch": 60}},
        {"name": "伊藤 五郎", "position_role": "遊撃手", "stats": {"contact": 74, "power": 55, "speed": 78, "arm": 75, "defense": 80, "catch": 70}},
        {"name": "中村 六郎", "position_role": "左翼手", "stats": {"contact": 65, "power": 60, "speed": 70, "arm": 62, "defense": 60, "catch": 65}},
        {"name": "小林 七郎", "position_role": "中堅手", "stats": {"contact": 80, "power": 50, "speed": 85, "arm": 68, "defense": 85, "catch": 80}},
        {"name": "加藤 八郎", "position_role": "右翼手", "stats": {"contact": 62, "power": 75, "speed": 60, "arm": 70, "defense": 65, "catch": 60}},
        {"name": "松本 九郎", "position_role": "代打",   "stats": {"contact": 90, "power": 90, "speed": 40, "arm": 50, "defense": 40, "catch": 40}},
    ]

    # チームBの選手情報（適当にコピーして一部変更）
    teamB_pitcher = {
        "name": "村田 一成",
        "stats": {"pitch_speed": 150, "control": 75, "stamina": 85, "breaking_ball": 70}
    }

    teamB_batters = [
        {"name": "野口 一郎", "position_role": "捕手",   "stats": {"contact": 65, "power": 58, "speed": 60, "arm": 66, "defense": 68, "catch": 70}},
        {"name": "佐々木 二郎", "position_role": "一塁手", "stats": {"contact": 60, "power": 85, "speed": 55, "arm": 58, "defense": 55, "catch": 58}},
        {"name": "今井 三郎", "position_role": "二塁手", "stats": {"contact": 72, "power": 60, "speed": 75, "arm": 64, "defense": 72, "catch": 65}},
        {"name": "大野 四郎", "position_role": "三塁手", "stats": {"contact": 70, "power": 68, "speed": 65, "arm": 67, "defense": 70, "catch": 67}},
        {"name": "金子 五郎", "position_role": "遊撃手", "stats": {"contact": 76, "power": 53, "speed": 77, "arm": 73, "defense": 78, "catch": 75}},
        {"name": "岡田 六郎", "position_role": "左翼手", "stats": {"contact": 68, "power": 63, "speed": 72, "arm": 66, "defense": 64, "catch": 67}},
        {"name": "和田 七郎", "position_role": "中堅手", "stats": {"contact": 75, "power": 55, "speed": 83, "arm": 70, "defense": 80, "catch": 78}},
        {"name": "藤井 八郎", "position_role": "右翼手", "stats": {"contact": 60, "power": 70, "speed": 58, "arm": 65, "defense": 60, "catch": 60}},
        {"name": "石井 九郎", "position_role": "代打",   "stats": {"contact": 88, "power": 88, "speed": 45, "arm": 52, "defense": 45, "catch": 45}},
    ]

    # チーム作成
    teamA = build_team("東京サンダーズ", teamA_pitcher, teamA_batters, dh_index=8)
    teamB = build_team("大阪ブレイカーズ", teamB_pitcher, teamB_batters, dh_index=8)

    # 試合
    game = Game(team_home=teamA, team_away=teamB)
    winner = game.play_game()

    if winner:
        print(f"\n勝者：{winner.name}")
    else:
        print("\n引き分けです。")

if __name__ == "__main__":
    main()
