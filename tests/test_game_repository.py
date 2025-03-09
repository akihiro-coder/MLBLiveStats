from datetime import datetime

import pytest
from flask import current_app as app

from mlb_live_stats import db
from mlb_live_stats.models import Venue, Game, GameTeam, Team
from mlb_live_stats.repository.game_repository import (
    get_or_create_venue,
    save_game,
    save_game_team,
    get_game_by_id,
    get_game_by_date,
    get_team_by_name
)


@pytest.fixture(scope='function')
def setup_database(app):
    """各テストごとにデータを初期化"""
    with app.app_context():
        db.create_all() # データベースを作成（テーブル定義）
        yield # ここでテスト関数が実行される
        db.session.remove()
        db.drop_all() # テストが終わったらデータを削除


def test_get_or_create_venue(setup_database):
    """球場情報を取得・作成するテスト"""
    # createのテスト
    venue = get_or_create_venue('Yankee Stadium')

    assert venue is not None
    assert venue.name == 'Yankee Stadium'

    # getのテスト
    venue2 = get_or_create_venue('Yankee Stadium')
    assert venue.id == venue2.id # 同じIDを持っていることを確認


def test_save_game(setup_database):
    """試合情報の保存・更新"""
    venue1 = get_or_create_venue('Yankee Stadium')
    venue2 = get_or_create_venue('Fenway Park')
    game_id = 12345
    date1 = datetime(2024, 6, 1)
    date2 = datetime(2024, 6, 2)

    # save
    save_game(game_id, date1, venue1.id)
    # get
    game = get_game_by_id(game_id)

    assert game is not None
    assert game.id == game_id
    assert game.date == date1
    assert game.venue_id == venue1.id

    # update
    save_game(game_id, date2, venue2.id) # 日付と球場を更新
    updated_game = get_game_by_id(game_id)

    assert updated_game is not None
    assert updated_game.id == game_id
    assert updated_game.date == date2 # 日付が更新されているか
    assert updated_game.venue_id == venue2.id # 球場が更新されているか


"""試合ごとのチーム情報を保存するテスト"""
def test_save_game_team(setup_database):
    # save new team
    team = Team(id=1, name='New York Yankees')
    db.session.add(team)
    db.session.commit()

    # save new game
    game_id = 12345
    date = datetime(2024, 6, 1)
    venue = get_or_create_venue('Yankee Stadium')
    save_game(game_id, date, venue.id)

    # save team info every game
    save_game_team(game_id, team.id, is_home_team=True)

    game_team = GameTeam.query.filter_by(team_id=team.id, game_id=game_id).first()

    assert game_team is not None
    assert game_team.game_id == game_id
    assert game_team.team_id == team.id
    assert game_team.is_home_team is True