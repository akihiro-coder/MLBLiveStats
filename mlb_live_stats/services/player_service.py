import requests

from mlb_live_stats.repository.player_repository import save_player


def fetch_team_players(team_id):
    """指定したチームの選手一覧を取得し、DBに保存"""
    url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster"
    response = requests.get(url)
    data = response.json()

    for player in data.get("roster", []):
        player_id = player["person"]["id"]
        player_name = player["person"]["fullName"]
        save_player(player_id, player_name, team_id)
