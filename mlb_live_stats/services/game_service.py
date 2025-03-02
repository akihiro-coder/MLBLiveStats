import requests
from datetime import datetime

from mlb_live_stats.repository.game_repository import get_or_create_venue, save_game


def fetch_today_games():
    """MLB Stats APIから今日の試合を取得し、DBに保存する"""
    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=" + datetime.today().strftime('%Y-%m-%d')
    response = requests.get(url)
    data = response.json()

    for date_info in data.get("dates", []):
        for game in date_info.get("games", []):
            game_id = game["gamePk"]
            game_date = game["officialDate"]
            venue_name = game["venue"]["name"]

            venue = get_or_create_venue(venue_name)
            save_game(game_id, datetime.strptime(game_date, "%Y-%m-%d"), venue.id)
