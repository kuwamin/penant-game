from player import Player

class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.starters = []
        self.defense_positions = {}  # 例: {"一塁手": Player, "三塁手": Player, ...}

        # 成績
        self.wins = 0
        self.losses = 0
        self.draws = 0

    def set_defense_positions(self, positions: dict):
        """
        守備配置をセットする。
        positions: 例 {"一塁手": player1, "遊撃手": player2, ...}
        """
        self.defense_positions = positions

    # その他は以前と同じ（get_team_average, get_eraなど）
    def add_player(self, player: Player):
        if len(self.players) < 70:
            self.players.append(player)
        else:
            print(f"{self.name} の選手数は最大70人です。追加できません。")

    def set_starters(self, starter_list):
        if len(starter_list) not in [9, 10]:
            raise ValueError("スタメンは9人または10人で構成してください。")
        self.starters = starter_list

    def get_team_average(self):
        """チーム打率の簡易平均（打率は仮に contact / 100.0 と仮定）"""
        hitters = [p for p in self.players if not p.is_pitcher]
        if not hitters:
            return 0.0
        total = sum(p.contact for p in hitters)
        return round(total / (len(hitters) * 100.0), 3)

    def get_era(self):
        """チーム防御率の簡易平均（防御率＝(100 - control) / 10 のような計算）"""
        pitchers = [p for p in self.players if p.is_pitcher]
        if not pitchers:
            return 0.0
        total = sum((100 - p.control) / 10 for p in pitchers)
        return round(total / len(pitchers), 2)

    def __str__(self):
        return f"{self.name}：{len(self.players)}人所属 / {self.wins}勝 {self.losses}敗 {self.draws}分"
        
    def set_lineup_and_defense(self, starters: list, dh_player: Player = None):
        """
        スタメンと守備配置をセット
        - starters: 9人（DH含む）
        - dh_player: スタメン中の1人。DHに指定された選手
        """
        if len(starters) != 9:
            raise ValueError("スタメンはDH含めて9人で指定してください")

        if dh_player not in starters:
            raise ValueError("DHに指定された選手はスタメンに含めてください")

        self.starters = starters
        self.dh_player = dh_player

        # DH以外の8人を守備に配置（ポジション→選手の辞書）
        field_positions = [
            "捕手", "一塁手", "二塁手", "三塁手", "遊撃手",
            "左翼手", "中堅手", "右翼手"
        ]
        fielders = [p for p in starters if p != dh_player]
        self.defense_positions = dict(zip(field_positions, fielders))


