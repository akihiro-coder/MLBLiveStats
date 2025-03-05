from mlb_live_stats import db
from mlb_live_stats.models import Game, Venue, GameTeam, Team


def get_or_create_venue(venue_name):
    """
    球場情報を取得する。存在しない場合は新規作成。

    :param venue_name: 球場名
    :return: Venue インスタンス
    """
    venue = Venue.query.filter_by(name=venue_name).first()
    if not venue:
        venue = Venue(name=venue_name)
        db.session.add(venue)
        db.session.commit()
    return venue


def save_game(game_id, date, venue_id):
    """
    試合情報を保存（既存データがあれば更新）

    :param game_id:  試合の一意なID
    :param date: 試合日
    :param venue_id: 球場ID
    :return: None
    """
    game = Game.query.get(id=game_id)
    if not game:
        game = Game(id=game_id, date=date, venue_id=venue_id)
        db.session.add(game)
        db.session.commit()
        return
    game.date = date
    game.venue_id = venue_id
    db.session.commit()