class Player:
    def __init__(self, name, position, is_pitcher=False, stats=None, position_role=None):
        self.at_bats = 0
        self.hits = 0
        self.walks = 0
        self.strikeouts = 0
        self.home_runs = 0
        self.id = id  # ← ここを追加
        self.name = name
        self.position = position  # 投手 or 野手
        self.is_pitcher = is_pitcher
        self.position_role = position_role  # 捕手、一塁手など（野手のみ）

        # （略） stats の部分は前回と同様

        # 投手能力
        self.pitch_speed = 0
        self.control = 0
        self.stamina = 0
        self.breaking_ball = 0  # 変化量

        # 野手能力
        self.contact = 0  # ミート
        self.power = 0
        self.speed = 0  # 走力
        self.arm = 0    # 肩力
        self.defense = 0  # 守備力
        self.catch = 0  # 捕球

        if stats:
            self.set_stats(stats)

    def set_stats(self, stats):
        # stats: 辞書形式で初期値を受け取る
        if self.is_pitcher:
            self.pitch_speed = stats.get('pitch_speed', 0)
            self.control = stats.get('control', 0)
            self.stamina = stats.get('stamina', 0)
            self.breaking_ball = stats.get('breaking_ball', 0)
        else:
            self.contact = stats.get('contact', 0)
            self.power = stats.get('power', 0)
            self.speed = stats.get('speed', 0)
            self.arm = stats.get('arm', 0)
            self.defense = stats.get('defense', 0)
            self.catch = stats.get('catch', 0)

    def __str__(self):
        return f"{self.name} ({'投手' if self.is_pitcher else '野手'})"
