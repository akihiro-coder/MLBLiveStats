from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy のインスタンスを作成
db = SQLAlchemy()

# ✅ チーム情報テーブル
class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    name = db.Column(db.String(100), nullable=False)  # チーム名
    abbreviation = db.Column(db.String(10), nullable=False)  # チーム略称
    league = db.Column(db.String(20), nullable=False)  # 所属リーグ

    # 1対多: 1チームは複数の試合に出場
    home_games = db.relationship('Game', back_populates='home_team_rel', foreign_keys='Game.home_team_id')
    away_games = db.relationship('Game', back_populates='away_team_rel', foreign_keys='Game.away_team_id')

# ✅ 試合情報テーブル
class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    game_date = db.Column(db.DateTime, nullable=False)  # 試合日
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='SET NULL'), nullable=True)  # ホームチーム
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='SET NULL'), nullable=True)  # アウェイチーム
    home_score = db.Column(db.Integer, nullable=True)  # ホームチームの得点
    away_score = db.Column(db.Integer, nullable=True)  # アウェイチームの得点
    status = db.Column(db.String(20), nullable=False)  # 試合状況（予定・進行中・終了など）

    # リレーション
    home_team_rel = db.relationship('Team', foreign_keys=[home_team_id])
    away_team_rel = db.relationship('Team', foreign_keys=[away_team_id])
    plays = db.relationship('Play', back_populates='game')  # 試合に紐づくプレー

# ✅ 選手情報テーブル
class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    name = db.Column(db.String(100), nullable=False)  # 選手名
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='SET NULL'), nullable=True)  # 所属チーム
    position = db.Column(db.String(50), nullable=False)  # ポジション

    team = db.relationship('Team')  # チームとのリレーション

# ✅ 試合中のプレーデータテーブル
class Play(db.Model):
    __tablename__ = 'plays'
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)  # 試合ID
    inning = db.Column(db.Integer, nullable=False)  # 何回のプレーか
    description = db.Column(db.String(255), nullable=False)  # プレーの詳細
    is_scoring_play = db.Column(db.Boolean, default=False)  # 得点プレーかどうか

    game = db.relationship('Game', back_populates='plays')  # 試合とのリレーション

# ✅ 選手の試合ごとの成績テーブル
class PlayerStats(db.Model):
    __tablename__ = 'player_stats'
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)  # 選手ID
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)  # 試合ID
    batting_avg = db.Column(db.Float, nullable=True)  # 打率
    home_runs = db.Column(db.Integer, nullable=True)  # 本塁打
    era = db.Column(db.Float, nullable=True)  # 防御率（投手用）

    player = db.relationship('Player')  # 選手とのリレーション
    game = db.relationship('Game')  # 試合とのリレーション
