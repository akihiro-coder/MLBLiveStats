import statsapi
# from mlb_live_stats import db
# from mlb_live_stats.models import Game
# from datetime import date


schedule = statsapi.schedule(start_date='07/01/2018',end_date='07/31/2018',team=143,opponent=121)

for game in schedule:
    print(f"{game['game_date']}: {game['away_name']} vs {game['home_name']} - {game['status']}")