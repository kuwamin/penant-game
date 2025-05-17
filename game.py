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
        bases = [False, False, False]  # 1塁、2塁、3塁

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

            result, hit_prob = self.at_bat_result(batter, pitcher, defense_team)
            log_line = f"{batter.name} の打席結果：{result}（hit_prob: {hit_prob}）"

            # 塁・得点処理
            if result == "アウト":
                outs += 1

            elif result == "ヒット":
                # 3塁ランナー生還
                if bases[2]:
                    score += 1
                    log_line += " → 3塁ランナー生還"
                # 2→3, 1→2
                bases[2] = bases[1]
                bases[1] = bases[0]
                bases[0] = True  # 打者が1塁へ

            elif result == "長打":
                # 3塁, 2塁ランナー生還
                if bases[2]:
                    score += 1
                    log_line += " → 3塁ランナー生還"
                if bases[1]:
                    score += 1
                    log_line += " → 2塁ランナー生還"
                # 1塁ランナー→3塁へ（進塁）
                bases[2] = bases[0]
                bases[1] = False
                bases[0] = False
                # 打者は2塁へ（ただし記録はしない）

            elif result == "ホームラン":
                runs = 1 + sum(bases)
                score += runs
                bases = [False, False, False]
                log_line += f" → ホームランで {runs} 点"

            self.log.append(log_line)
            batter_index += 1

        # 打順継続のために保存
        if offense_team == self.team_home:
            self.batter_index_home = batter_index % len(batters)
        else:
            self.batter_index_away = batter_index % len(batters)

        self.log.append(f"{offense_team.name} の得点：{score}点")
        return score

    def at_bat_result(self, batter: Player, pitcher: Player, defense_team: Team):
        # 守備スコア
        defenders = list(defense_team.defense_positions.values())
        defense_score = sum(p.defense for p in defenders) / len(defenders) if defenders else 50

        # ヒット確率の構成要素
        base_hit_prob = 0.002 * batter.contact + 0.17
        breaking_penalty = (pitcher.breaking_ball - 6) * 0.01
        speed_penalty = abs(pitcher.pitch_speed - 145) * 0.002
        defense_penalty = (defense_score - 50) * 0.002
        random_factor = random.uniform(-0.05, 0.05)

        final_hit_prob = base_hit_prob - breaking_penalty - speed_penalty - defense_penalty + random_factor
        final_hit_prob = max(0.0, min(final_hit_prob, 1.0))  # 0.0〜1.0に制限

        # ヒットするかを確率で抽選
        if random.random() < final_hit_prob:
            # ヒットした場合：長打 or ホームランを再抽選
            power = batter.power

            long_hit_chance = 0.1 + (power - 50) * 0.005  # パワー50で10%、パワー70で20%
            home_run_chance = 0.05 + (power - 80) * 0.01  # パワー80で5%、パワー90で15%

            # 弾道による補正（trajectory: 1〜4）
            trajectory = getattr(batter, 'trajectory', 2)  # 無ければ2

            trajectory_bonus_hr = (trajectory - 2) * 0.015  # 弾道3で+0.015、4で+0.03
            trajectory_bonus_ld = (trajectory - 2) * 0.02   # 弾道3で+0.02、4で+0.04

            home_run_chance += trajectory_bonus_hr
            long_hit_chance += trajectory_bonus_ld
            
            long_hit_chance = max(0.0, min(long_hit_chance, 1.0))
            home_run_chance = max(0.0, min(home_run_chance, 1.0))

            r = random.random()
            if r < home_run_chance:
                result = "ホームラン"
            elif r < home_run_chance + long_hit_chance:
                result = "長打"
            else:
                result = "ヒット"
        else:
            result = "アウト"

        return result, round(final_hit_prob, 3)


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
