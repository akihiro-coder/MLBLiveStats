from mlb_live_stats import db


class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    # GameTeamとのリレーション（試合ごとのチーム情報）
    games = db.relationship('GameTeam', back_populates='team')

    # Playerとのリレーション（チームの選手）
    players = db.relationship('Player', back_populates='team')


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    status = db.Column(db.String, nullable=False)

    # Venueとのリレーション
    venue = db.relationship('Venue', back_populates='games')

    # GameTeamとのリレーション（試合ごとのチーム情報）
    teams = db.relationship('GameTeam', back_populates='game')

    # Pointとのリレーション（イニングごとの得点）
    points = db.relationship('Point', back_populates='game')

    # PlayerStatsとのリレーション（試合ごとの選手成績）
    player_stats = db.relationship('PlayerStats', back_populates='game')

    # GameTeamStatsとのリレーション（試合ごとのチーム成績）
    team_stats = db.relationship('GameTeamStats', back_populates='game')


class GameTeam(db.Model):
    __tablename__ = 'game_team'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    is_home_team = db.Column(db.Boolean, nullable=False)

    # Teamとのリレーション
    team = db.relationship('Team', back_populates='games')

    # Gameとのリレーション
    game = db.relationship('Game', back_populates='teams')


class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    # Gameとのリレーション
    games = db.relationship('Game', back_populates='venue')


class Point(db.Model):
    __tablename__ = 'point'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    inning_number = db.Column(db.Integer, nullable=False)
    runs = db.Column(db.Integer, nullable=False)

    # Gameとのリレーション
    game = db.relationship('Game', back_populates='points')

    # Teamとのリレーション
    team = db.relationship('Team')


class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

    # Teamとのリレーション
    team = db.relationship('Team', back_populates='players')

    # PlayerStatsとのリレーション
    stats = db.relationship('PlayerStats', back_populates='player')


class PlayerStats(db.Model):
    __tablename__ = 'player_stats'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)

    # ピッチャー成績
    num_pitches = db.Column(db.Integer)
    num_strikeouts = db.Column(db.Integer)

    # バッター成績
    batting_avg = db.Column(db.Float)
    rbi = db.Column(db.Integer)

    # Gameとのリレーション
    game = db.relationship('Game', back_populates='player_stats')

    # Playerとのリレーション
    player = db.relationship('Player', back_populates='stats')


class GameTeamStats(db.Model):
    __tablename__ = 'game_team_stats'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    num_hits = db.Column(db.Integer, nullable=False)
    num_errors = db.Column(db.Integer, nullable=False)

    # Gameとのリレーション
    game = db.relationship('Game', back_populates='team_stats')

    # Teamとのリレーション
    team = db.relationship('Team')