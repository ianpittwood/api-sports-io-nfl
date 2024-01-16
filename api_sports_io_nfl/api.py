from datetime import datetime
from enum import Enum, EnumMeta
from urllib.parse import urljoin

import requests

from api_sports_io_nfl import exceptions


class ApiNfl:
    ENDPOINTS = {
        "status": "/status",
        "timezone": "/timezone",
        "seasons": "/seasons",
        "leagues": "/leagues",
        "teams": "/teams",
        "players": "/players",
        "players_statistics": "/players/statistics",
        "injuries": "/injuries",
        "games": "/games",
        "games_events": "/games/events",
        "games_teams_statistics": "/games/statistics/teams",
        "games_players_statistics": "/games/statistics/players",
        "standings": "/standings",
        "standings_conferences": "/standings/conferences",
        "standings_divisions": "/standings/divisions",
        "odds": "/odds",
        "odds_bets": "/odds/bets",
        "odds_bookmakers": "/odds/bookmakers",
    }

    class Leagues(Enum):
        NFL = 1
        NCAA = 2

    class PlayersStatisticsGroups(Enum):
        DEFENSIVE = "defensive"
        FUMBLES = "fumbles"
        INTERCEPTIONS = "interceptions"
        KICK_RETURNS = "kick_returns"
        KICKING = "kicking"
        PASSING = "passing"
        PUNT_RETURNS = "punt_returns"
        PUNTING = "punting"
        RECEIVING = "receiving"
        RUSHING = "rushing"

    class Conferences(Enum):
        AFC = "American Football Conference"
        NFC = "National Football Conference"

    class Divisions(Enum):
        NORTH = "North"
        SOUTH = "South"
        EAST = "East"
        WEST = "West"

    def __init__(self, api_key, use_rapid_api=False, timezone="America/New_York"):
        """Initialize the API wrapper.

        Args:
            api_key: API key for the API.
            use_rapid_api: Whether to use the Rapid API host or the API Sports host.
        """
        self.protocol = "https://"
        self.api_key = api_key
        if use_rapid_api:
            self.api_host = "api-nfl-v1.p.rapidapi.com"
        else:
            self.api_host = "v1.american-football.api-sports.io"
        self._timezone = timezone

    @staticmethod
    def _clean_season(season):
        """Clean the season argument."""
        if len(str(season)) != 4:
            raise ValueError("season must be a valid year")
        try:
            season = int(season)
        except ValueError:
            raise ValueError("season must be a valid year")
        return season

    @staticmethod
    def _clean_league(league):
        try:
            league = league.value
        except AttributeError:
            pass
        try:
            league = int(league)
        except ValueError:
            raise ValueError("league must be an integer")
        if league not in [1, 2]:
            raise ValueError("league must be a valid league: 1 for NFL, 2 for NCAA")
        return league

    def _get_default_headers(self):
        """Get default headers for the API request."""
        return {"x-rapidapi-host": self.api_host, "x-rapidapi-key": self.api_key}

    def get(self, url, params=None, headers=None):
        """Handler for GET requests to the API."""
        if headers is None:
            headers = self._get_default_headers()
        resp = requests.get(url, params=params, headers=headers)
        if resp.status_code != 200:
            exception_type = exceptions.EXCEPTION_MAP.get(resp.status_code, exceptions.ApiError)
            raise exception_type(response=resp)
        if resp.json().get("errors"):
            raise exceptions.ApiError(response=resp)
        return resp

    def status(self):
        """Call the status endpoint."""
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["status"])
        resp = self.get(url)
        return resp.json()["response"]

    def timezone(self):
        """Call the timezone endpoint.

        https://api-sports.io/documentation/nfl/v1#tag/Timezone/operation/get-timezone
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["timezone"])
        resp = self.get(url)
        return resp.json()["response"]

    def seasons(self):
        """Call the seasons endpoint.

        https://api-sports.io/documentation/nfl/v1#tag/Seasons
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["seasons"])
        resp = self.get(url)
        return resp.json()["response"]

    def leagues(self, id=None, season=None, current=None):
        """Call the leagues endpoint.

        https://api-sports.io/documentation/nfl/v1#tag/Leagues

        Args:
            id: The ID of the league (e.g. 1 for NFL, 2 for NCAA)
            season: A valid season year (e.g. 2020)
            current: If true, only return current season for leagues
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["leagues"])
        params = {}
        if id is not None:
            try:
                id = id.value
            except AttributeError:
                pass
            try:
                id = int(id)
            except ValueError:
                raise ValueError("id must be an integer")
            if id not in [1, 2]:
                raise ValueError("id must be a valid league: 1 for NFL, 2 for NCAA")
            params["id"] = id
        if season is not None:
            season = self._clean_season(season)
            params["season"] = season
        if current is not None:
            if type(current) is not bool and current not in ["true", "false"]:
                raise ValueError("current must be a boolean value")
            params["current"] = current
        resp = self.get(url, params=params)
        return resp.json()["response"]

    def teams(self, id=None, league=None, season=None, name=None, code=None, search=None):
        """Call the teams endpoint.

        https://api-sports.io/documentation/nfl/v1#tag/Teams/operation/get-teams

        Args:
            id: The ID of the team
            league: A valid League id (e.g. 1 for NFL, 2 for NCAA)
            season: A valid season year (e.g. 2020)
            name: The name of the team
            code: The code of the team (e.g. LV for Las Vegas Raiders)
            search: A search term to search for teams (>= 3 char)
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["teams"])
        params = {}
        min_arguments_met = False
        if id is not None:
            try:
                id = int(id)
            except ValueError:
                raise ValueError("id must be an integer")
            params["id"] = id
            min_arguments_met = True
        if league is not None:
            league = self._clean_league(league)
            if season is None:
                raise ValueError("season must be provided if league is provided")
            params["league"] = league
            min_arguments_met = True
        if season is not None:
            season = self._clean_season(season)
            params["season"] = season
            if league is None:
                raise ValueError("league must be provided if season is provided")
            min_arguments_met = True
        if name is not None:
            params["name"] = name
            min_arguments_met = True
        if code is not None:
            params["code"] = code
            min_arguments_met = True
        if search is not None:
            if len(search) < 3:
                raise ValueError("search must be at least 3 characters")
            params["search"] = search
            min_arguments_met = True
        if not min_arguments_met:
            raise ValueError("Must provide at least one of: id, league, season, name, code, search")
        resp = self.get(url, params=params)
        return resp.json()["response"]

    def players(self, id=None, name=None, team=None, season=None, search=None):
        """Call the players endpoint.

        https://api-sports.io/documentation/nfl/v1#tag/Players

        Args:
            id: The ID of the player
            name: The name of the player
            team: The ID of the team
            season: A valid season year (e.g. 2020)
            search: A search term to search for players (>= 3 char)
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["players"])
        params = {}
        min_arguments_met = False
        if id is not None:
            try:
                id = int(id)
            except ValueError:
                raise ValueError("id must be an integer")
            params["id"] = id
            min_arguments_met = True
        if name is not None:
            params["name"] = name
            min_arguments_met = True
        if team is not None:
            try:
                team = int(team)
            except ValueError:
                raise ValueError("team must be an integer")
            if season is None:
                raise ValueError("season must be provided if team is provided")
            params["team"] = team
            min_arguments_met = True
        if season is not None:
            season = self._clean_season(season)
            if team is None:
                raise ValueError("team must be provided if season is provided")
            params["season"] = season
            min_arguments_met = True
        if search is not None:
            if len(search) < 3:
                raise ValueError("search must be at least 3 characters")
            params["search"] = search
            min_arguments_met = True
        if not min_arguments_met:
            raise ValueError("Must provide at least one of: id, name, team, season, search")
        resp = self.get(url, params=params)
        return resp.json()["response"]

    def players_statistics(self, id=None, team=None, season=None):
        """Call the players statistics endpoint.

        Statistics are not available for every season in the API. Check the leagues endpoint for availability info.

        https://api-sports.io/documentation/nfl/v1#tag/Players/operation/get-players-statistics

        Args:
            id: The ID of the player
            team: The ID of the team
            season: A valid season year (e.g. 2020)
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["players_statistics"])
        params = {}
        min_arguments_met = False
        if id is not None:
            try:
                id = int(id)
            except ValueError:
                raise ValueError("id must be an integer")
            params["id"] = id
            if team is None and season is None:
                raise ValueError("team or season must be provided if id is provided")
            min_arguments_met = True
        if team is not None:
            try:
                team = int(team)
            except ValueError:
                raise ValueError("team must be an integer")
            if season is None:
                raise ValueError("season must be provided if team is provided")
            params["team"] = team
            min_arguments_met = True
        if season is not None:
            season = self._clean_season(season)
            if team is None and id is None:
                raise ValueError("id or team must be provided if season is provided")
            params["season"] = season
            min_arguments_met = True
        if not min_arguments_met:
            raise ValueError("Must provide at least one of: id, team, season")
        resp = self.get(url, params=params)
        return resp.json()["response"]

    def injuries(self, player=None, team=None):
        """Call the injuries endpoint.

        Only retrieves *current* injuries, no historic data is provided.

        https://api-sports.io/documentation/nfl/v1#tag/Injuries/operation/get-teams

        Args:
            player: The ID of the player
            team: The ID of the team
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["injuries"])
        params = {}
        min_arguments_met = False
        if player is not None:
            try:
                player = int(player)
            except ValueError:
                raise ValueError("player must be an integer")
            params["player"] = player
            min_arguments_met = True
        if team is not None:
            try:
                team = int(team)
            except ValueError:
                raise ValueError("team must be an integer")
            params["team"] = team
            min_arguments_met = True
        if not min_arguments_met:
            raise ValueError("Must provide at least one of: player, team")
        resp = self.get(url, params=params)
        return resp.json()["response"]

    def games(self, id=None, date=None, league=None, season=None, team=None, h2h=None, live=None, timezone=None):
        """Call the games endpoint.

        https://api-sports.io/documentation/nfl/v1#tag/Games/operation/get-games

        Args:
            id: The ID of the game
            date: A valid date in YYYY-MM-DD format
            league: A valid League id (e.g. 1 for NFL, 2 for NCAA)
            season: A valid season year (e.g. 2020)
            team: The ID of the team
            h2h: Two teams IDs separated by a dash (e.g. 1-2)
            live: If true, only return live games
            timezone: A valid timezone (e.g. America/New_York)
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["games"])
        params = {}
        min_arguments_met = False
        if id is not None:
            try:
                id = int(id)
            except ValueError:
                raise ValueError("id must be an integer")
            params["id"] = id
            min_arguments_met = True
        if date is not None:
            if type(date) is str:
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("date must be a valid date in YYYY-MM-DD format")
            elif type(date) is datetime:
                date = date.strftime("%Y-%m-%d")
            else:
                raise ValueError("date must be a valid date in YYYY-MM-DD format")
            params["date"] = date
            min_arguments_met = True
        if league is not None:
            league = self._clean_league(league)
            if season is None:
                raise ValueError("season must be provided if league is provided")
            params["league"] = league
            min_arguments_met = True
        if season is not None:
            season = self._clean_season(season)
            params["season"] = season
            if id is None and league is None and team is None and date is None and h2h is None and live is None:
                raise ValueError("one of id, league, team, date, h2h, or live must be provided if season is provided")
            min_arguments_met = True
        if team is not None:
            try:
                team = int(team)
            except ValueError:
                raise ValueError("team must be an integer")
            if season is None:
                raise ValueError("season must be provided if team is provided")
            params["team"] = team
            min_arguments_met = True
        if h2h is not None:
            split_h2h = h2h.split("-")
            if len(split_h2h) != 2:
                raise ValueError("h2h must be two team IDs separated by a dash (e.g. 1-2)")
            try:
                [int(x) for x in split_h2h]
            except ValueError:
                raise ValueError("h2h must be two team IDs separated by a dash (e.g. 1-2)")
            params["h2h"] = h2h
            min_arguments_met = True
        if live is not None:
            if type(live) is not bool and live not in ["true", "false"]:
                raise ValueError("live must be a boolean value")
            if live == "true" or live is True:
                live = "all"
            else:
                live = None
            params["live"] = live
            if live is not None:
                min_arguments_met = True
        if timezone is not None:
            params["timezone"] = timezone
        else:
            params["timezone"] = self._timezone
        if not min_arguments_met:
            raise ValueError("Must provide at least one of: id, date, league, season, team, h2h, live, timezone")
        resp = self.get(url, params=params)
        return resp.json()["response"]

    def games_events(self, id=None):
        """Call the games events endpoint.

        https://api-sports.io/documentation/nfl/v1#tag/Games/operation/get-games-events

        Args:
            id: The ID of the game
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["games_events"])
        params = {}
        if id is None:
            raise ValueError("id must be provided")
        try:
            id = int(id)
        except ValueError:
            raise ValueError("id must be an integer")
        params["id"] = id
        resp = self.get(url, params=params)
        return resp.json()["response"]

    def games_teams_statistics(self, id=None, team=None):
        """Call the games teams statistics endpoint.

        https://api-sports.io/documentation/nfl/v1#tag/Games/operation/get-games-statistics-teams

        Args:
            id: The ID of the game
            team: The ID of the team
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["games_teams_statistics"])
        params = {}
        if id is None:
            raise ValueError("id must be provided")
        try:
            id = int(id)
        except ValueError:
            raise ValueError("id must be an integer")
        params["id"] = id
        if team is not None:
            try:
                team = int(team)
            except ValueError:
                raise ValueError("team must be an integer")
            params["team"] = team
        resp = self.get(url, params=params)
        return resp.json()["response"]

    def games_players_statistics(self, id=None, group=None, team=None, player=None):
        """Call the games players statistics endpoint.

        https://api-sports.io/documentation/nfl/v1#tag/Games/operation/get-games-statistics-players

        Args:
            id: The ID of the game
            group: The statistics group to lookup (e.g. defensive, passing, kicking)
            team: The ID of the team
            player: The ID of the player
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["games_players_statistics"])
        params = {}
        if id is None:
            raise ValueError("id must be provided")
        try:
            id = int(id)
        except ValueError:
            raise ValueError("id must be an integer")
        params["id"] = id
        if group is not None:
            try:
                group = group.value
            except AttributeError:
                pass
            if group not in [x.value for x in self.PlayersStatisticsGroups]:
                raise ValueError(f"group must be one of: {', '.join([x.value for x in self.PlayersStatisticsGroups])}")
            params["group"] = group
        if team is not None:
            try:
                team = int(team)
            except ValueError:
                raise ValueError("team must be an integer")
            params["team"] = team
        if player is not None:
            try:
                player = int(player)
            except ValueError:
                raise ValueError("player must be an integer")
            params["player"] = player
        resp = self.get(url, params=params)
        return resp.json()["response"]

    def standings(self, league=None, season=None, team=None, conference=None, division=None):
        """Call the standings endpoint.

        https://api-sports.io/documentation/nfl/v1#tag/Standings/operation/get-standings

        Args:
            league: A valid League id (e.g. 1 for NFL, 2 for NCAA)
            season: A valid season year (e.g. 2020)
            team: The ID of the team
            conference: The ID of the conference
            division: The ID of the division
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["standings"])
        params = {}
        if league is None:
            raise ValueError("league must be provided")
        league = self._clean_league(league)
        params["league"] = league
        if season is None:
            raise ValueError("season must be provided")
        season = self._clean_season(season)
        params["season"] = season
        if team is not None:
            try:
                team = int(team)
            except ValueError:
                raise ValueError("team must be an integer")
            params["team"] = team
        if conference is not None:
            try:
                conference = conference.value
            except AttributeError:
                pass
            if conference not in [x.value for x in self.Conferences]:
                raise ValueError(f"conference must be one of: {', '.join([x.value for x in self.Conferences])}")
            params["conference"] = conference
        if division is not None:
            try:
                division = division.value
            except AttributeError:
                pass
            if division not in [x.value for x in self.Divisions]:
                raise ValueError(f"division must be one of: {', '.join([x.value for x in self.Divisions])}")
            params["division"] = division
        resp = self.get(url, params=params)
        return resp.json()["response"]

    def standings_conferences(self, league=None, season=None):
        """Call the conferences endpoint.

        https://api-sports.io/documentation/nfl/v1#tag/Standings/operation/get-standings-conferences

        Args:
            league: A valid League id (e.g. 1 for NFL, 2 for NCAA)
            season: A valid season year (e.g. 2020)
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["standings_conferences"])
        params = {}
        if league is None:
            raise ValueError("league must be provided")
        league = self._clean_league(league)
        params["league"] = league
        if season is None:
            raise ValueError("season must be provided")
        season = self._clean_season(season)
        params["season"] = season
        resp = self.get(url, params=params)
        return resp.json()["response"]

    # Alias for standings_conferences
    conference = standings_conferences

    def standings_divisions(self, league=None, season=None):
        """Call the divisions endpoint.

        Divisions are not enumerated by conferences in the API, so this endpoint is not very useful by itself.

        https://api-sports.io/documentation/nfl/v1#tag/Standings/operation/get-standings-divisions

        Args:
            league: A valid League id (e.g. 1 for NFL, 2 for NCAA)
            season: A valid season year (e.g. 2020)
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["standings_divisions"])
        params = {}
        if league is None:
            raise ValueError("league must be provided")
        league = self._clean_league(league)
        params["league"] = league
        if season is None:
            raise ValueError("season must be provided")
        season = self._clean_season(season)
        params["season"] = season
        resp = self.get(url, params=params)
        return resp.json()["response"]

    # Alias for standings_divisions
    division = standings_divisions

    def odds(self, game=None, bookmaker=None, bet=None):
        """Call the odds endpoint.

        Odds are only retained for 7 days after the closure of an event.

        https://api-sports.io/documentation/nfl/v1#tag/Odds

        Args:
            game: The ID of the game
            bookmaker: The ID of the bookmaker
            bet: The ID of the bet
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["odds"])
        params = {}
        if game is None:
            raise ValueError("game must be provided")
        try:
            game = int(game)
        except ValueError:
            raise ValueError("game must be an integer")
        params["game"] = game
        if bookmaker is not None:
            try:
                bookmaker = int(bookmaker)
            except ValueError:
                raise ValueError("bookmaker must be an integer")
            params["bookmaker"] = bookmaker
        if bet is not None:
            try:
                bet = int(bet)
            except ValueError:
                raise ValueError("bet must be an integer")
            params["bet"] = bet
        resp = self.get(url, params=params)
        return resp.json()["response"]

    def odds_bets(self, id=None, search=None):
        """Call the odds bets endpoint.

        https://api-sports.io/documentation/nfl/v1#tag/Odds/operation/get-odds-bets

        Args:
            id: The ID of the bet
            search: A search term to search for bets (>= 3 char)
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["odds_bets"])
        params = {}
        if id is not None:
            try:
                id = int(id)
            except ValueError:
                raise ValueError("id must be an integer")
            params["id"] = id
        if search is not None:
            if len(search) < 3:
                raise ValueError("search must be at least 3 characters")
            params["search"] = search
        resp = self.get(url, params=params)
        return resp.json()["response"]

    # Alias for odds_bets
    bets = odds_bets

    def odds_bookmakers(self, id=None, search=None):
        """Call the odds bookmakers endpoint.

        https://api-sports.io/documentation/nfl/v1#tag/Odds/operation/get-odds-bookmakers

        Args:
            id: The ID of the bookmaker
            search: A search term to search for bookmakers (>= 3 char)
        """
        url = urljoin(self.protocol + self.api_host, self.ENDPOINTS["odds_bookmakers"])
        params = {}
        if id is not None:
            try:
                id = int(id)
            except ValueError:
                raise ValueError("id must be an integer")
            params["id"] = id
        if search is not None:
            if len(search) < 3:
                raise ValueError("search must be at least 3 characters")
            params["search"] = search
        resp = self.get(url, params=params)
        return resp.json()["response"]

    # Alias for odds_bookmakers
    bookmakers = odds_bookmakers
