from flask import Flask

from mlb_live_stats import db
from mlb_live_stats.models import Game
from mlb_live_stats.services.game_service import fetch_today_games
from mlb_live_stats.services.player_service import fetch_team_players
from mlb_live_stats.services.score_service import fetch_game_scores, fetch_game_boxscore


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mlb.db'
db.init_app(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        fetch_today_games()
        games = Game.query.all()
        for game in games:
            fetch_game_scores(game.id)
            fetch_game_boxscore(game.id)
