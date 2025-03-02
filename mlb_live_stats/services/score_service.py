import requests

from mlb_live_stats.repository.score_repository import save_inning_score, save_team_stats


def fetch_game_scores(game_id):
    """試合のスコア（イニングごとの得点）を取得し、DBに保存"""
    url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/linescore"
    response = requests.get(url)
    data = response.json()

    for inning_idx, inning in enumerate(data["innings"], start=1):
        home_runs = inning["home"]["runs"]
        away_runs = inning["away"]["runs"]
        save_inning_score(game_id, home_team_id, inning_idx, home_runs)
        save_inning_score(game_id, away_team_id, inning_idx, away_runs)

def fetch_game_boxscore(game_id):
    """試合のヒット数・エラー数を取得し、DBに保存"""
    url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore"
    response = requests.get(url)
    data = response.json()

    home_hits = data["teams"]["home"]["teamStats"]["batting"]["hits"]
    away_hits = data["teams"]["away"]["teamStats"]["batting"]["hits"]
    home_errors = data["teams"]["home"]["teamStats"]["fielding"]["errors"]
    away_errors = data["teams"]["away"]["teamStats"]["fielding"]["errors"]

    save_team_stats(game_id, home_team_id, home_hits, home_errors)
    save_team_stats(game_id, away_team_id, away_hits, away_errors)
