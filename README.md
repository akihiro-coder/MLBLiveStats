# MLBLiveStats

## ER図
```
Game ───> GameTeam ───> Team
├───> Venue
├───> Point ───> Team
├───> PlayerStats ───> Player
├───> GameTeamStats ───> Team

Team ───> Player
```

## 📌 `db.relationship` の対応関係

以下の表は、各 `db.relationship` の設定と、それがどのようにデータ取得を簡潔にするかをまとめたものです。

| **リレーション** | **関連する `db.relationship`** | **説明** |
|--------------|------------------------------|----------|
| **`Game` ⇄ `GameTeam`** | `game.teams` ⇄ `team.games` | ある試合に出場するチームを取得する |
| **`Game` ⇄ `Venue`** | `game.venue` ⇄ `venue.games` | ある試合が開催される球場を取得する |
| **`Game` ⇄ `Point`** | `game.points` ⇄ `point.game` | ある試合のイニングごとの得点を取得する |
| **`Point` ⇄ `Team`** | `point.team` ⇄ `team.points` | あるチームの得点情報を取得する |
| **`Game` ⇄ `PlayerStats`** | `game.player_stats` ⇄ `player.stats` | ある試合の選手成績を取得する |
| **`PlayerStats` ⇄ `Player`** | `player.stats` ⇄ `stats.player` | ある選手の成績を取得する |
| **`Game` ⇄ `GameTeamStats`** | `game.team_stats` ⇄ `team.stats` | ある試合のチーム成績を取得する |

---

### **📌 `db.relationship` の活用例**
```python
# ある試合の参加チームを取得
game = Game.query.get(game_id)
teams = [gt.team for gt in game.teams]  # `game.teams` でチーム一覧を取得

# あるチームの試合履歴を取得
team = Team.query.get(team_id)
games = [gt.game for gt in team.games]  # `team.games` で出場した試合を取得
```