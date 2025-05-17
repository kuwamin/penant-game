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
                self.current_outs = outs


            batter_index += 1

        return score
    
    def simulate_half_inning_with_log(self, offense_team: Team, defense_team: Team):
        score = 0
        outs = 0
        bases = [False, False, False]

        self.current_outs = outs
        self.current_bases = bases

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

            base_display = "".join([str(i + 1) for i, b in enumerate(bases) if b]) or "なし"
            situation = f"【{outs}アウト {base_display}塁】"

            result, hit_prob, direction = self.at_bat_result(batter, pitcher, defense_team)

            # 表示用に打球方向を取得（ログだけに使う）
            if result in ["ゴロ", "飛", "直", "ヒット", "2塁打", "3塁打", "本塁打"]:
                direction = Game.decide_hit_direction(result, batter)

            log_line = f"{situation}{batter.name} の打席結果：{direction}{result}（hit_prob: {hit_prob}）"

            # アウトカウントの判定は direction 抜きで行えるようになる
            if result in ["三振", "ゴロ", "飛", "直", "フライアウト"]:
                outs += 1
                self.current_outs = outs
                batter_index += 1
                self.log.append(log_line)
                continue


            elif result == "四球" or result == "死球":
                if all(bases):  # 満塁で押し出し
                    score += 1
                    log_line += " → 押し出しで1点"

                # ランナーを後ろから前へ進める（前の塁が空いていれば）
                if bases[2] == False and bases[1]:
                    bases[2] = True
                    bases[1] = False
                if bases[1] == False and bases[0]:
                    bases[1] = True
                    bases[0] = False
                bases[0] = True  # 打者が1塁へ


            elif result == "ヒット":
                if bases[2]:
                    score += 1
                    log_line += " → 3塁ランナー生還"
                bases[2] = bases[1]
                bases[1] = bases[0]
                bases[0] = True

            elif result == "2塁打":
                if bases[2]:
                    score += 1
                    log_line += " → 3塁ランナー生還"
                if bases[1]:
                    score += 1
                    log_line += " → 2塁ランナー生還"
                if bases[0]:
                    bases[2] = True
                else:
                    bases[2] = False
                bases[1] = True
                bases[0] = False

            elif result == "3塁打":
                score += sum(bases)
                log_line += f" → {sum(bases)}人が生還"
                bases = [False, False, True]

            elif result == "本塁打":
                runs = 1 + sum(bases)
                score += runs
                log_line += f" → ホームランで {runs} 点"
                bases = [False, False, False]

            elif result == "犠飛":
                if outs < 2 and bases[2]:
                    score += 1
                    outs += 1
                    self.current_outs = outs

                    bases[2] = False
                    log_line += " → 3塁ランナー生還（犠飛）"
                else:
                    result = "フライアウト"
                    outs += 1
                    self.current_outs = outs

                    log_line = f"{situation}{batter.name} の打席結果：{result}（hit_prob: {hit_prob}）"
                    batter_index += 1
                    self.log.append(log_line)
                    continue

            elif result == "犠打":
                outs += 1
                self.current_outs = outs
                if bases[0]:
                    bases = [False, bases[0], bases[1]]
                log_line += " → 犠打で進塁"

            elif result == "併打":
                outs += 2
                bases = [False, False, bases[2]]  # 最も単純な処理：1,2塁消える
                log_line += " → 併殺打"

            batter_index += 1
            self.log.append(log_line)

        if offense_team == self.team_home:
            self.batter_index_home = batter_index % len(batters)
        else:
            self.batter_index_away = batter_index % len(batters)

        self.log.append(f"{offense_team.name} の得点：{score}点")
        return score

    def at_bat_result(self, batter: Player, pitcher: Player, defense_team: Team):
        r = random.random()

        # パラメータ
        contact = batter.contact
        power = batter.power
        speed = batter.speed
        trajectory = getattr(batter, 'trajectory', 2)

        control = pitcher.control
        breaking = pitcher.breaking_ball
        velocity = pitcher.pitch_speed

        defenders = list(defense_team.defense_positions.values())
        defense = sum(p.defense for p in defenders) / len(defenders) if defenders else 50

        # ---- 各要素の確率設計 ----
        hbp_chance = max(0.01, 0.06 - control * 0.001)
        # 四球
        bb_chance = max(0.01, 0.03 + (100 - control) * 0.0015 + power * 0.0005)
        so_chance = max(0.05, 0.10 + (100 - contact) * 0.001 + control * 0.001)

        # 犠打（ランナーあり＆2アウト未満のみ）
        has_runner = any(self.current_bases)
        sac_bunt_chance = 0.015 if has_runner and self.current_outs < 2 and speed > 70 else 0.005 if has_runner and self.current_outs < 2 else 0.0
        sac_fly_chance = 0.015 + trajectory * 0.005

        # ヒット確率計算
        # ヒット確率計算（改良版）
        base_hit_prob = 0.002 * contact + 0.17
        breaking_penalty = (breaking - 7) * 0.012
        speed_penalty = (145 - velocity) * 0.0047
        control_penalty = (50 - control) * 0.0023
        defense_penalty = (defense - 50) * 0.002
        hit_random = random.uniform(-0.03, 0.03)

        final_hit_prob = base_hit_prob - breaking_penalty - speed_penalty - control_penalty - defense_penalty + hit_random
        final_hit_prob = max(0.0, min(final_hit_prob, 1.0))


        # ヒットの中身の配分（調整）
        long_hit_chance = 0.12 + (power - 50) * 0.005 + (trajectory - 2) * 0.02
        home_run_chance = max(0.0, 0.002 * (power - 20))
        triple_chance = 0.01 + speed * 0.001

        ground_out_chance = 0.15 + (3 - trajectory) * 0.03
        fly_out_chance = 0.1 + trajectory * 0.02
        line_out_chance = 0.05 + (contact / 100) * 0.05

        double_play_chance = 0.03 if speed < 50 and self.current_outs < 2 and self.current_bases[0] else 0.0

        p = random.random()
        if p < hbp_chance:
            return "死球", round(final_hit_prob, 3), ""
        p -= hbp_chance
        if p < bb_chance:
            return "四球", round(final_hit_prob, 3), ""
        p -= bb_chance
        if p < so_chance:
            return "三振", round(final_hit_prob, 3), ""
        p -= so_chance
        if p < sac_bunt_chance:
            return "犠打", round(final_hit_prob, 3), ""
        p -= sac_bunt_chance
        if p < sac_fly_chance:
            return "犠飛", round(final_hit_prob, 3), ""
        p -= sac_fly_chance

        if random.random() < final_hit_prob:
            r2 = random.random()
            if r2 < home_run_chance:
                direction = Game.decide_hit_direction("本塁打", batter)
                return "本塁打", round(final_hit_prob, 3), direction
            elif r2 < home_run_chance + triple_chance:
                direction = Game.decide_hit_direction("3塁打", batter)
                return "3塁打", round(final_hit_prob, 3), direction
            elif r2 < home_run_chance + triple_chance + long_hit_chance:
                direction = Game.decide_hit_direction("2塁打", batter)
                return "2塁打", round(final_hit_prob, 3), direction
            else:
                direction = Game.decide_hit_direction("ヒット", batter)
                return "ヒット", round(final_hit_prob, 3), direction
        else:
            r3 = random.random()
            if r3 < double_play_chance:
                return "併打", round(final_hit_prob, 3), ""
            elif r3 < double_play_chance + ground_out_chance:
                direction = Game.decide_hit_direction("ゴロ", batter)
                return "ゴロ", round(final_hit_prob, 3), direction
            elif r3 < double_play_chance + ground_out_chance + fly_out_chance:
                direction = Game.decide_hit_direction("飛", batter)
                return "飛", round(final_hit_prob, 3), direction
            else:
                direction = Game.decide_hit_direction("直", batter)
                return "直", round(final_hit_prob, 3), direction





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
    

def decide_hit_direction(result_type, batter):
        power = batter.power
        trajectory = getattr(batter, 'trajectory', 2)
        pt_ratio = ((trajectory - 1) / 3) * 0.3 + (power / 100) * 0.7
        pt_ratio = min(1.0, max(0.0, pt_ratio)) 

        def weighted_choice(options):
            r = random.random()
            cumulative = 0
            for direction, weight in options:
                cumulative += weight
                if r < cumulative:
                    return direction
            return options[-1][0]

        if result_type == "ゴロ":
            table = [("投", 0.07), ("捕", 0.01), ("一", 0.20), ("二", 0.26), ("遊", 0.26), ("三", 0.20)]

        elif result_type == "飛":
            base = [("投", 0.06), ("捕", 0.01), ("一", 0.15), ("二", 0.19), ("遊", 0.19), ("三", 0.15),
                    ("左", 0.07), ("中", 0.11), ("右", 0.07)]
            table = []
            for pos, weight in base:
                if pos in ["左", "中", "右"]:
                    weight += pt_ratio * weight * 0.2  # 外野は最大+20%
                else:
                    weight -= pt_ratio * weight * 0.2  # 内野は最大-20%
                table.append((pos, weight))
            total = sum(w for _, w in table)
            table = [(pos, w / total) for pos, w in table]

        elif result_type == "ヒット":
            table = [("投", 0.01), ("捕", 0.01), ("一", 0.02), ("二", 0.03), ("遊", 0.04), ("三", 0.04),
                    ("左", 0.28), ("中", 0.29), ("右", 0.28)]
        elif result_type in ["2塁打", "3塁打"]:
            table = [("左", 0.32), ("中", 0.33), ("右", 0.35)]
        elif result_type == "本塁打":
            table = [("左", 0.30), ("中", 0.40), ("右", 0.30)]
        elif result_type == "直":
            table = [("投", 0.08), ("一", 0.20), ("二", 0.20), ("遊", 0.20), ("三", 0.20),
             ("左", 0.04), ("中", 0.04), ("右", 0.04)]

        else:
            return ""

        return weighted_choice(table)
# Gameクラスの外（ファイルの最後）に追加
Game.decide_hit_direction = staticmethod(decide_hit_direction)