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
    # save
    game_id = 12345
    date = datetime(2025, 3,7)
    venue = get_or_create_venue('Yankee Stadium')
    save_game(game_id, date, venue.id)
    # get
    game = get_game_by_id(game_id)
    # test
    assert game is not None
    assert game.id == game_id
    assert game.date == date
    assert game.venue_id == venue.id

    # update
    game_id = 12346
    date = datetime(2025, 3,8)
    venue = get_or_create_venue('Yankee Stadium')
    save_game(game_id, date, venue.id)
    # get
    game = get_game_by_id(game_id)
    # test
    assert game is not None
    assert game.id == game_id
    assert game.date == date
    assert game.venue_id == venue.id











