from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

import config


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=config.Config):
    # Flaskアプリケーションのインスタンス作成
    app = Flask(__name__)

    # アプリケーションの設定読み込み
    app.config.from_object(config_class)

    # 拡張機能の初期化
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # ルーティングのインポート
    with app.app_context():
        from mlb_live_stats import routes, forms, models

    return app