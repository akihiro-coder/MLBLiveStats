from mlb_live_stats import db
from mlb_live_stats.models import Player


def save_player(player_id, name, team_id):
    """選手情報を保存（存在する場合は更新）"""
    new_player = Player(id=player_id, name=name, team_id=team_id)
    db.session.merge(new_player)
    db.session.commit()
