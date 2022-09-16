"""Automates my runyourpool NFL picks using spreads from the-odds-api"""

import logging
import os
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any, Optional
from zoneinfo import ZoneInfo

import requests

import pysandbox.common as common

# See: https://the-odds-api.com/liveapi/guides/v4/#overview
ENV_API_TOKEN = "ODDS_API_KEY"
GET_ODDS_URL = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds"
PDT = ZoneInfo("America/Los_Angeles")

"""Represents the JSON coming from the-odds-api that represents a game."""
GameType = dict[str, Any]

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Game:
    """Represents a summarized view of a upcoming game"""

    home_team: str
    home_spread_avg: float
    away_team: str
    away_spread_avg: float
    start_time: datetime

    def __str__(self) -> str:
        away_avg = f"{self.away_spread_avg:6.2f}" if self.away_spread_avg < 0 else "      "
        home_avg = f"{self.home_spread_avg:6.2f}" if self.home_spread_avg < 0 else "      "
        start_time = self.start_time.astimezone(PDT)
        start_time_str = start_time.strftime("%a, %m/%d %I:%M%p PDT")
        return f"Game: {self.away_team:22} {away_avg}  @  {self.home_team:22} {home_avg} [{start_time_str}]"


def _call_odds_api() -> list[GameType]:
    if ENV_API_TOKEN not in os.environ:
        raise Exception(f"'{ENV_API_TOKEN}' not found in environment variables.")

    params = {"apiKey": os.environ[ENV_API_TOKEN], "regions": "us", "oddsFormat": "american", "markets": "spreads"}
    response = requests.get(GET_ODDS_URL, params=params)
    response.raise_for_status()
    logger.debug(f"GET {GET_ODDS_URL} returned {response}")
    games_json: list[GameType] = response.json()
    logger.info(f"Retrieved recent data for {len(games_json)} games from {GET_ODDS_URL}")
    return games_json


def _parse_start_time(game: GameType) -> datetime:
    """Parses the `game`'s (the-odds-api Game API object) start time, returning a timezone-aware date"""
    start_time_str = game["commence_time"]
    start_time_str = start_time_str.replace("Z", "+00:00")  # replace trailing Z with TZ that's datetime-friendly
    return datetime.fromisoformat(start_time_str)


def _filter_games(games_json: list[GameType], today: date) -> list[GameType]:
    """Filter out any games that take place after the upcoming Monday."""
    days_until_monday = 7 - today.weekday()  # NOTE: Monday == 0 for datetime.weekday()
    next_monday = today + timedelta(days=days_until_monday)

    include_games = list()
    for game in games_json:
        start_time = _parse_start_time(game)
        if start_time.astimezone(PDT).date() <= next_monday:
            include_games.append(game)
    return include_games


def generate_picks(today_input: Optional[date] = None) -> list[Game]:
    # makes unit testing easier if we can mock what day it is...
    today: date = today_input if today_input else date.today()

    common.initialize_logging_from_file()
    logger.level = logging.INFO
    games_json: list[GameType] = _call_odds_api()
    games_list = list()

    # filter out games that are after Monday...
    filtered_games = _filter_games(games_json, today)

    for game in filtered_games:
        home_team = game["home_team"]
        away_team = game["away_team"]
        start_time = _parse_start_time(game)
        logger.debug(f"   Processing game: {away_team} @ {home_team}")
        bookmakers = game["bookmakers"]
        logger.debug(f"      Consolidating {len(bookmakers)} bookmaker odds...")
        home_points = 0.0
        away_points = 0.0

        for bm in bookmakers:
            # logger.debug(f"         {bm['title']:20} as of {bm['last_update']}")
            spread_markets = [market for market in bm["markets"] if market["key"] == "spreads"]
            spread_market = spread_markets[0]
            for outcome in spread_market["outcomes"]:
                if outcome["name"] == home_team:
                    home_points += outcome["point"]
                if outcome["name"] == away_team:
                    away_points += outcome["point"]

        home_avg = home_points / len(bookmakers)
        away_avg = away_points / len(bookmakers)
        game_obj = Game(home_team, home_avg, away_team, away_avg, start_time)
        games_list.append(game_obj)
        logger.debug(f"      {game_obj}")

    games_list.sort(key=lambda game: abs(game.home_spread_avg), reverse=True)
    for ndx, sorted_game in enumerate(games_list):
        logger.info(f"Game {ndx+1:2}: {sorted_game}")

    return games_list


def main() -> None:
    generate_picks()


if __name__ == "__main__":
    main()
