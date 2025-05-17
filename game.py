from player import Player
from team import Team
import random

class Game:
    def __init__(self, team_home, team_away):
        self.team_home = team_home
        self.team_away = team_away
        self.score_home = 0
        self.score_away = 0
        self.log = []  # ここで試合ログを記録
        self.inning_scores_home = []  # 各回の得点（ホーム）
        self.inning_scores_away = []  # 各回の得点（アウェイ）
        self.hits_home = 0            # ヒット数（仮）
        self.hits_away = 0
        self.batter_index_home = 0
        self.batter_index_away = 0



    def play_game(self):
        for inning in range(1, 10):  # 1回〜9回まで
            self.log.append(f"【{inning}回表：{self.team_home.name} の攻撃】")
            score_home_inning = self.simulate_half_inning_with_log(self.team_home, self.team_away)
            self.score_home += score_home_inning
            self.inning_scores_home.append(score_home_inning)

            self.log.append(f"【{inning}回裏：{self.team_away.name} の攻撃】")
            score_away_inning = self.simulate_half_inning_with_log(self.team_away, self.team_home)
            self.score_away += score_away_inning
            self.inning_scores_away.append(score_away_inning)

        self.log.append(f"{self.team_home.name}: {self.score_home}点")
        self.log.append(f"{self.team_away.name}: {self.score_away}点")


    def simulate_half_inning(self, offense_team: Team, defense_team: Team):
        score = 0
        outs = 0
        batter_index = 0

        pitcher = next((p for p in defense_team.players if p.is_pitcher), None)
        if not pitcher:
            raise ValueError(f"{defense_team.name} に投手がいません")

        batters = offense_team.starters  # DHを含む9人
        while outs < 3:
            batter = batters[batter_index % len(batters)]
            if batter.is_pitcher:
                batter_index += 1
                continue  # 投手は打席に立たない

            result = self.at_bat_result(batter, pitcher, defense_team)
            print(f"{batter.name} の結果: {result}")

            if result in ["ヒット", "長打", "ホームラン"]:
                score += 1  # 今は単純化した得点処理
            elif result == "アウト":
                outs += 1

            batter_index += 1

        return score
    
    def simulate_half_inning_with_log(self, offense_team: Team, defense_team: Team):
        score = 0
        outs = 0

        # 打順の基準となるバッターインデックスをチームごとに選ぶ
        if offense_team == self.team_home:
            batter_index = self.batter_index_home
        else:
            batter_index = self.batter_index_away

        pitcher = next((p for p in defense_team.players if p.is_pitcher), None)
        batters = offense_team.starters

        while outs < 3:
            batter = batters[batter_index % len(batters)]
            if batter.is_pitcher:
                batter_index += 1
                continue

            result = self.at_bat_result(batter, pitcher, defense_team)
            self.log.append(f"{batter.name} の打席結果：{result}")

            if result in ["ヒット", "長打", "ホームラン"]:
                score += 1
            elif result == "アウト":
                outs += 1

            batter_index += 1

        # 次のイニングのために現在のバッター位置を保存
        if offense_team == self.team_home:
            self.batter_index_home = batter_index % len(batters)
        else:
            self.batter_index_away = batter_index % len(batters)

        self.log.append(f"{offense_team.name} の得点：{score}点")
        return score



    def at_bat_result(self, batter: Player, pitcher: Player, defense_team: Team):
        hit_chance = batter.contact - pitcher.control + random.randint(-10, 10)
        power = batter.power

        defenders = list(defense_team.defense_positions.values())
        if defenders:
            defense_score = sum(p.defense for p in defenders) / len(defenders)
            hit_chance -= int(defense_score * 0.1)

        if hit_chance > 60:
            return "ホームラン" if power > 90 else "長打"
        elif hit_chance > 40:
            return "ヒット"
        else:
            return "アウト"

    def get_winner(self):
        if self.score_home > self.score_away:
            self.team_home.wins += 1
            self.team_away.losses += 1
            return self.team_home
        elif self.score_home < self.score_away:
            self.team_away.wins += 1
            self.team_home.losses += 1
            return self.team_away
        else:
            self.team_home.draws += 1
            self.team_away.draws += 1
            return None

    def print_result(self):
        print("\n試合結果：")
        print(f"{self.team_home.name}: {self.score_home}点")
        print(f"{self.team_away.name}: {self.score_away}点")
