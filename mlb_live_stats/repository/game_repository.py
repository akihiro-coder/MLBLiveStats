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
    game = Game(id=game_id, date=date, venue_id=venue_id)
    db.session.merge(game)
    db.session.commit()


def save_game_team(game_id, team_id, is_home_team):
    """
    試合ごとのチーム情報を保存

    :param game_id: 試合ID
    :param team_id: チームID
    :param is_home_team: ホームチームかどうか
    :return: None
    """
    game_team = GameTeam.query.filter_by(game_id=game_id, team_id=team_id).first()
    if not game_team:
        game_team = GameTeam(game_id=game_id, team_id=team_id)
        db.session.add(game_team)
        db.session.commit()


def get_game_by_id(game_id):
    """
    試合IDで試合情報を取得

    :param game_id: 試合ID
    :return: Game インスタンス
    """
    return Game.query.get(id=game_id)


def get_game_by_date(date):
    """
    指定された日付の試合を取得

    :param date: 試合日
    :return: List[Game]
    """
    return Game.query.filter_by(date=date).all()


def get_team_by_name(team_name):
    """
    チーム名でチーム情報を取得（存在しなければ None）

    :param team_name:
    :return: Team インスタンス
    """
    return Team.query.filter_by(name=team_name).first()