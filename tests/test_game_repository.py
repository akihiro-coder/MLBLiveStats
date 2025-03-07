import pytest

from flask import current_app as app

from mlb_live_stats import db
from mlb_live_stats.repository.game_repository import (
    get_or_create_venue,
    save_game,
    save_game_team,
    get_game_by_id,
    get_game_by_date,
    get_team_by_name
)
from mlb_live_stats.models import Venue, Game, GameTeam, Team


@pytest.fixture
def client():
    """テスト用のFlaskアプリの設定"""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:" # メモリ上のDB使用
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_get_or_create_venue(client):
    """球場情報の作成と取得のテスト"""