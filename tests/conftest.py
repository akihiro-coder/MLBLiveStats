import pytest

from mlb_live_stats import create_app, db


@pytest.fixture(scope='function')
def app():
    """テスト用のFlaskアプリを作成"""
    app = create_app(testing=True) #  テスト用のFlaskアプリを作成
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://test_user:test_pass@localhost:3307/test_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context(): # Flaskのアプリケーションコンテキストを作成（DBにアクセス可能にする）
        db.create_all() # データベースのテーブルを作成
        yield app # テスト関数を実行
        db.session.remove() # セッションを削除（メモリ解放）
        db.drop_all() # テストデータベースを削除（クリーンな状態に戻す）


@pytest.fixture(scope='function')
def client(app):
    """
    Flaskのテストクライアントを提供
    APIテスト時にHTTPリクエストを送るために使用する
    """
    return app.test_client()