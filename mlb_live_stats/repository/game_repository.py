from mlb_live_stats import db
from mlb_live_stats.models import Game, Venue


def get_or_create_venue(name):
    """球場情報を取得 or 作成"""
    venue = Venue.query.filter_by(name=name).first()
    if not venue:
        venue = Venue(name=name, location="")
        db.session.add(venue)
        db.session.commit()
    return venue

def save_game(game_id, date, venue_id):
    """試合情報を保存（存在する場合は更新）"""
    new_game = Game(id=game_id, date=date, venue_id=venue_id)
    db.session.merge(new_game)
    db.session.commit()
