from mlb_live_stats import db
from mlb_live_stats.models import Point, GameTeamStats


def save_inning_score(game_id, team_id, inning, runs):
    """イニングごとの得点を保存"""
    point = Point(game_id=game_id, team_id=team_id, inning_number=inning, runs=runs)
    db.session.merge(point)
    db.session.commit()

def save_team_stats(game_id, team_id, hits, errors):
    """試合ごとのチーム成績（ヒット数・エラー数）を保存"""
    stats = GameTeamStats(game_id=game_id, team_id=team_id, num_hits=hits, num_errors=errors)
    db.session.merge(stats)
    db.session.commit()
