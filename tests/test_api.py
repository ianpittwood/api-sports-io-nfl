import os
import unittest

from api_sports_io_nfl import ApiNfl


class TestEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        api_key = os.getenv("TEST_API_KEY")
        if api_key is None:
            raise Exception("TEST_API_KEY environment variable not set")
        self.api = ApiNfl(api_key)


class TestStatus(TestEndpoints):
    def test_status(self):
        resp = self.api.status()
        self.assertIsInstance(resp, dict)
        self.assertIn("account", resp)
        self.assertIn("subscription", resp)
        self.assertIn("requests", resp)


class TestTimezone(TestEndpoints):
    def test_timezone(self):
        resp = self.api.timezone()
        self.assertIsInstance(resp, list)
        self.assertIn("America/Chicago", resp)


class TestSeasons(TestEndpoints):
    def test_seasons(self):
        resp = self.api.seasons()
        self.assertIsInstance(resp, list)
        self.assertIn(2020, resp)


class TestLeagues(TestEndpoints):
    def test_leagues(self):
        resp = self.api.leagues()
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 2)
        for d in resp:
            self.assertIn("league", d)
            self.assertIn("country", d)
            self.assertIn("seasons", d)

    def test_leagues_id(self):
        resp = self.api.leagues(id=1)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 1)
        for d in resp:
            self.assertIn("league", d)
            self.assertIn("country", d)
            self.assertIn("seasons", d)

    def test_leagues_season(self):
        resp = self.api.leagues(season=2023)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 2)
        for d in resp:
            self.assertIn("league", d)
            self.assertIn("country", d)
            self.assertIn("seasons", d)

    def test_leagues_current(self):
        resp = self.api.leagues(current=True)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 2)
        for d in resp:
            self.assertIn("league", d)
            self.assertIn("country", d)
            self.assertIn("seasons", d)

    def test_leagues_bad_id(self):
        with self.assertRaises(ValueError):
            self.api.leagues(id="nfl")

    def test_leagues_bad_season(self):
        with self.assertRaises(ValueError):
            self.api.leagues(season="2023-regular")

    def test_leagues_bad_current(self):
        with self.assertRaises(ValueError):
            self.api.leagues(current="yes")


class TestTeams(TestEndpoints):
    def test_teams_id(self):
        resp = self.api.teams(id=1)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 1)
        for d in resp:
            self.assertIn("id", d)
            self.assertIn("name", d)
            self.assertIn("logo", d)
            self.assertIn("city", d)
            self.assertIn("country", d)
            self.assertIn("established", d)
            self.assertIn("stadium", d)
            self.assertIn("coach", d)

    def test_teams_league_season(self):
        resp = self.api.teams(league=self.api.Leagues.NFL, season=2020)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 34)
        for d in resp:
            self.assertIn("id", d)
            self.assertIn("name", d)
            self.assertIn("logo", d)
            self.assertIn("city", d)
            self.assertIn("country", d)
            self.assertIn("established", d)
            self.assertIn("stadium", d)
            self.assertIn("coach", d)

    def test_teams_name(self):
        resp = self.api.teams(name="Las Vegas Raiders")
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 1)
        for d in resp:
            self.assertIn("id", d)
            self.assertIn("name", d)
            self.assertIn("logo", d)
            self.assertIn("city", d)
            self.assertIn("country", d)
            self.assertIn("established", d)
            self.assertIn("stadium", d)
            self.assertIn("coach", d)

    def test_teams_code(self):
        resp = self.api.teams(code="LV")
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 1)
        for d in resp:
            self.assertIn("id", d)
            self.assertIn("name", d)
            self.assertIn("logo", d)
            self.assertIn("city", d)
            self.assertIn("country", d)
            self.assertIn("established", d)
            self.assertIn("stadium", d)
            self.assertIn("coach", d)

    def test_teams_search(self):
        resp = self.api.teams(search="Los")
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 2)
        for d in resp:
            self.assertIn("id", d)
            self.assertIn("name", d)
            self.assertIn("logo", d)
            self.assertIn("city", d)
            self.assertIn("country", d)
            self.assertIn("established", d)
            self.assertIn("stadium", d)
            self.assertIn("coach", d)

    def test_teams_no_args(self):
        with self.assertRaises(ValueError):
            self.api.teams()

    def test_teams_league_season_required_together(self):
        with self.assertRaises(ValueError):
            self.api.teams(season=2023)
        with self.assertRaises(ValueError):
            self.api.teams(league=self.api.Leagues.NFL)

    def test_teams_bad_league(self):
        with self.assertRaises(ValueError):
            self.api.teams(season=2023, league="nfl")

    def test_teams_bad_season(self):
        with self.assertRaises(ValueError):
            self.api.teams(season="current", league=self.api.Leagues.NFL)

    def test_teams_search_lt_3_char(self):
        with self.assertRaises(ValueError):
            self.api.teams(search="L")


class TestPlayers(TestEndpoints):
    def test_players_id(self):
        resp = self.api.players(id=1)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 1)
        for d in resp:
            self.assertIn("id", d)
            self.assertIn("name", d)
            self.assertIn("age", d)
            self.assertIn("height", d)
            self.assertIn("weight", d)
            self.assertIn("college", d)
            self.assertIn("group", d)
            self.assertIn("position", d)
            self.assertIn("number", d)
            self.assertIn("salary", d)
            self.assertIn("experience", d)
            self.assertIn("image", d)

    def test_players_name(self):
        resp = self.api.players(name="Derek Carr")
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 1)
        for d in resp:
            self.assertIn("id", d)
            self.assertIn("name", d)
            self.assertIn("age", d)
            self.assertIn("height", d)
            self.assertIn("weight", d)
            self.assertIn("college", d)
            self.assertIn("group", d)
            self.assertIn("position", d)
            self.assertIn("number", d)
            self.assertIn("salary", d)
            self.assertIn("experience", d)
            self.assertIn("image", d)

    def test_players_team_season(self):
        resp = self.api.players(season=2021, team=1)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 92)
        for d in resp:
            self.assertIn("id", d)
            self.assertIn("name", d)
            self.assertIn("age", d)
            self.assertIn("height", d)
            self.assertIn("weight", d)
            self.assertIn("college", d)
            self.assertIn("group", d)
            self.assertIn("position", d)
            self.assertIn("number", d)
            self.assertIn("salary", d)
            self.assertIn("experience", d)
            self.assertIn("image", d)

    def test_players_search(self):
        resp = self.api.players(search="Der", season=2021, team=1)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 3)
        for d in resp:
            self.assertIn("id", d)
            self.assertIn("name", d)
            self.assertIn("age", d)
            self.assertIn("height", d)
            self.assertIn("weight", d)
            self.assertIn("college", d)
            self.assertIn("group", d)
            self.assertIn("position", d)
            self.assertIn("number", d)
            self.assertIn("salary", d)
            self.assertIn("experience", d)
            self.assertIn("image", d)

    def test_players_no_args(self):
        with self.assertRaises(ValueError):
            self.api.players()

    def test_players_bad_id(self):
        with self.assertRaises(ValueError):
            self.api.players(id="str")

    def test_players_season_team_required_together(self):
        with self.assertRaises(ValueError):
            self.api.players(season=2023)
        with self.assertRaises(ValueError):
            self.api.players(team=1)

    def test_players_bad_season(self):
        with self.assertRaises(ValueError):
            self.api.players(season="current", team=1)

    def test_players_bad_team(self):
        with self.assertRaises(ValueError):
            self.api.players(season=2021, team="str")

    def test_players_search_lt_3_char(self):
        with self.assertRaises(ValueError):
            self.api.players(search="D")


class TeamPlayersStatistics(TestEndpoints):
    def test_players_statistics_single_player(self):
        resp = self.api.players_statistics(id=1, season=2023)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 1)
        for d in resp:
            self.assertIn("player", d)
            self.assertIsInstance(d["player"], dict)
            self.assertIn("teams", d)
            self.assertIsInstance(d["teams"], list)
            for team in d["teams"]:
                self.assertIn("team", team)
                self.assertIn("groups", team)

    def test_players_statistics_team(self):
        resp = self.api.players_statistics(team=1, season=2023)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 87)
        for d in resp:
            self.assertIn("player", d)
            self.assertIsInstance(d["player"], dict)
            self.assertIn("teams", d)
            self.assertIsInstance(d["teams"], list)
            for team in d["teams"]:
                self.assertIn("team", team)
                self.assertIn("groups", team)

    def test_players_statistics_no_args(self):
        with self.assertRaises(ValueError):
            self.api.players_statistics()

    def test_players_statistics_bad_id(self):
        with self.assertRaises(ValueError):
            self.api.players_statistics(id="str")

    def test_players_statistics_bad_season(self):
        with self.assertRaises(ValueError):
            self.api.players_statistics(season="current")

    def test_players_statistics_bad_team(self):
        with self.assertRaises(ValueError):
            self.api.players_statistics(team="str")

    def test_players_statistics_id_not_alone(self):
        with self.assertRaises(ValueError):
            self.api.players_statistics(id=1)

    def test_players_statistics_team_not_alone(self):
        with self.assertRaises(ValueError):
            self.api.players_statistics(team=1)

    def test_players_statistics_season_not_alone(self):
        with self.assertRaises(ValueError):
            self.api.players_statistics(season=2023)


class TestInjuries(TestEndpoints):
    def test_injuries_team(self):
        resp = self.api.injuries(team=1)
        self.assertIsInstance(resp, list)

    def test_injuries_player(self):
        resp = self.api.injuries(player=1)
        self.assertIsInstance(resp, list)

    def test_injuries_no_args(self):
        with self.assertRaises(ValueError):
            self.api.injuries()

    def test_injuries_bad_team(self):
        with self.assertRaises(ValueError):
            self.api.injuries(team="str")

    def test_injuries_bad_player(self):
        with self.assertRaises(ValueError):
            self.api.injuries(player="str")


class TestGames(TestEndpoints):
    def test_games_season(self):
        resp = self.api.games(league=self.api.Leagues.NFL, season=2022)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 335)
        for d in resp:
            self.assertIn("game", d)
            self.assertIn("league", d)
            self.assertIn("teams", d)
            self.assertIn("scores", d)

    def test_games_date(self):
        resp = self.api.games(date="2024-01-14")
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 2)
        for d in resp:
            self.assertIn("game", d)
            self.assertIn("league", d)
            self.assertIn("teams", d)
            self.assertIn("scores", d)

    def test_games_team(self):
        resp = self.api.games(team=1, season=2023)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 20)
        for d in resp:
            self.assertIn("game", d)
            self.assertIn("league", d)
            self.assertIn("teams", d)
            self.assertIn("scores", d)

    def test_games_h2h(self):
        resp = self.api.games(h2h="1-4")
        self.assertIsInstance(resp, list)
        self.assertGreaterEqual(len(resp), 4)
        for d in resp:
            self.assertIn("game", d)
            self.assertIn("league", d)
            self.assertIn("teams", d)
            self.assertIn("scores", d)

    def test_games_bad_league(self):
        with self.assertRaises(ValueError):
            self.api.games(league="nfl", season=2023)

    def test_games_bad_season(self):
        with self.assertRaises(ValueError):
            self.api.games(league=self.api.Leagues.NFL, season="current")

    def test_games_bad_team(self):
        with self.assertRaises(ValueError):
            self.api.games(team="str")

    def test_games_bad_date(self):
        with self.assertRaises(ValueError):
            self.api.games(date="Jan 3 2024")

    def test_games_bad_h2h(self):
        with self.assertRaises(ValueError):
            self.api.games(h2h="1-4-5")


class TestGamesEvents(TestEndpoints):
    def test_games_events(self):
        resp = self.api.games_events(id=7820)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 7)
        for d in resp:
            self.assertIn("quarter", d)
            self.assertIn("minute", d)
            self.assertIn("team", d)
            self.assertIn("player", d)
            self.assertIn("type", d)
            self.assertIn("comment", d)
            self.assertIn("score", d)

    def test_games_events_no_args(self):
        with self.assertRaises(ValueError):
            self.api.games_events()

    def test_games_events_bad_id(self):
        with self.assertRaises(ValueError):
            self.api.games_events(id="str")


class TestGameStatistics(TestEndpoints):
    def test_games_teams_statistics(self):
        resp = self.api.games_teams_statistics(id=7820)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 2)
        for d in resp:
            self.assertIn("team", d)
            self.assertIn("statistics", d)

    def test_games_teams_statistics_no_args(self):
        with self.assertRaises(ValueError):
            self.api.games_teams_statistics()

    def test_games_teams_statistics_no_id(self):
        with self.assertRaises(ValueError):
            self.api.games_teams_statistics(team=1)


class TestGamesPlayersStatistics(TestEndpoints):
    def test_games_players_statistics(self):
        resp = self.api.games_players_statistics(id=7820)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 2)
        for d in resp:
            self.assertIn("team", d)
            self.assertIn("groups", d)

    def test_games_players_statistics_no_args(self):
        with self.assertRaises(ValueError):
            self.api.games_players_statistics()

    def test_games_players_statistics_no_id(self):
        with self.assertRaises(ValueError):
            self.api.games_players_statistics(team=1)


class TestStandings(TestEndpoints):
    def test_standings(self):
        resp = self.api.standings(league=self.api.Leagues.NFL, season=2022)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 32)
        for d in resp:
            self.assertIn("league", d)
            self.assertIn("conference", d)
            self.assertIn("division", d)
            self.assertIn("position", d)
            self.assertIn("team", d)
            self.assertIn("won", d)
            self.assertIn("lost", d)
            self.assertIn("ties", d)
            self.assertIn("points", d)
            self.assertIn("records", d)
            self.assertIn("streak", d)

    def test_standings_conference(self):
        resp = self.api.standings(conference=self.api.Conferences.AFC, league=self.api.Leagues.NFL, season=2022)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 16)
        for d in resp:
            self.assertIn("league", d)
            self.assertIn("conference", d)
            self.assertIn("division", d)
            self.assertIn("position", d)
            self.assertIn("team", d)
            self.assertIn("won", d)
            self.assertIn("lost", d)
            self.assertIn("ties", d)
            self.assertIn("points", d)
            self.assertIn("records", d)
            self.assertIn("streak", d)

    def test_standings_division(self):
        resp = self.api.standings(division=self.api.Divisions.WEST, league=self.api.Leagues.NFL, season=2022)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 8)
        for d in resp:
            self.assertIn("league", d)
            self.assertIn("conference", d)
            self.assertIn("division", d)
            self.assertIn("position", d)
            self.assertIn("team", d)
            self.assertIn("won", d)
            self.assertIn("lost", d)
            self.assertIn("ties", d)
            self.assertIn("points", d)
            self.assertIn("records", d)
            self.assertIn("streak", d)

    def test_standings_conference_division(self):
        resp = self.api.standings(
            conference=self.api.Conferences.AFC,
            division=self.api.Divisions.WEST,
            league=self.api.Leagues.NFL,
            season=2022,
        )
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 4)
        for d in resp:
            self.assertIn("league", d)
            self.assertIn("conference", d)
            self.assertIn("division", d)
            self.assertIn("position", d)
            self.assertIn("team", d)
            self.assertIn("won", d)
            self.assertIn("lost", d)
            self.assertIn("ties", d)
            self.assertIn("points", d)
            self.assertIn("records", d)
            self.assertIn("streak", d)

    def test_standings_no_args(self):
        with self.assertRaises(ValueError):
            self.api.standings()

    def test_standings_bad_league(self):
        with self.assertRaises(ValueError):
            self.api.standings(league="nfl", season=2023)

    def test_standings_bad_season(self):
        with self.assertRaises(ValueError):
            self.api.standings(league=self.api.Leagues.NFL, season="current")

    def test_standings_bad_conference(self):
        with self.assertRaises(ValueError):
            self.api.standings(conference="nfc", season=2023, league=self.api.Leagues.NFL)

    def test_standings_bad_division(self):
        with self.assertRaises(ValueError):
            self.api.standings(division="nfc-east", season=2023, league=self.api.Leagues.NFL)


class TestConferences(TestEndpoints):
    def test_conferences_nfl(self):
        resp = self.api.standings_conferences(league=self.api.Leagues.NFL, season=2022)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 2)

    def test_conferences_ncaa(self):
        resp = self.api.standings_conferences(league=self.api.Leagues.NCAA, season=2022)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 28)

    def test_conferences_no_args(self):
        with self.assertRaises(ValueError):
            self.api.standings_conferences()

    def test_conferences_bad_league(self):
        with self.assertRaises(ValueError):
            self.api.standings_conferences(league="str", season=2023)

    def test_conferences_bad_season(self):
        with self.assertRaises(ValueError):
            self.api.standings_conferences(season="current", league=self.api.Leagues.NFL)


class TestDivisions(TestEndpoints):
    def test_divisions_nfl(self):
        resp = self.api.standings_divisions(league=self.api.Leagues.NFL, season=2022)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 4)

    def test_divisions_ncaa(self):
        resp = self.api.standings_divisions(league=self.api.Leagues.NCAA, season=2022)
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 8)

    def test_divisions_no_args(self):
        with self.assertRaises(ValueError):
            self.api.standings_divisions()

    def test_divisions_bad_league(self):
        with self.assertRaises(ValueError):
            self.api.standings_divisions(league="str", season=2023)

    def test_divisions_bad_season(self):
        with self.assertRaises(ValueError):
            self.api.standings_divisions(season="current", league=self.api.Leagues.NFL)


class TestOdds(TestEndpoints):
    # TODO: Add more tests for this endpoint. It's tricky to test since data is pulled down after 7 days post-game.
    def test_odds(self):
        resp = self.api.odds(game=10940)
        self.assertIsInstance(resp, list)

    def test_odds_no_args(self):
        with self.assertRaises(ValueError):
            self.api.odds()

    def test_odds_bad_bookmaker(self):
        with self.assertRaises(ValueError):
            self.api.odds(game=10940, bookmaker="str")

    def test_odds_bad_bet(self):
        with self.assertRaises(ValueError):
            self.api.odds(game=10940, bet="str")


class TestOddsBets(TestEndpoints):
    def test_odds_bets(self):
        resp = self.api.odds_bets()
        self.assertIsInstance(resp, list)
        self.assertGreaterEqual(len(resp), 114)


class TestOddsBookmakers(TestEndpoints):
    def test_odds_bookmakers(self):
        resp = self.api.odds_bookmakers()
        self.assertIsInstance(resp, list)
        self.assertGreaterEqual(len(resp), 20)


class TestValidation(TestEndpoints):
    def test_clean_season(self):
        with self.assertRaises(ValueError):
            self.api._clean_season(100)
        with self.assertRaises(ValueError):
            self.api._clean_season(40000)
        self.assertEqual(self.api._clean_season("2023"), 2023)

    def test_clean_league(self):
        with self.assertRaises(ValueError):
            self.api._clean_league("nfl")
        with self.assertRaises(ValueError):
            self.api._clean_league(3)
        self.assertEqual(self.api._clean_league(self.api.Leagues.NFL), 1)
        self.assertEqual(self.api._clean_league(self.api.Leagues.NCAA), 2)
