import os
from datetime import date
from typing import Any

import pytest
import responses

from pysandbox.common_test import mock_response_from_file
from pysandbox.nflpickem.picker import (
    ENV_API_TOKEN,
    GET_ODDS_URL,
    _call_odds_api,
    generate_picks,
)


@pytest.fixture(autouse=True)
def mock_api_token() -> None:
    os.environ[ENV_API_TOKEN] = "mock-api-token"


@pytest.fixture
def mock_today() -> date:
    """Support mocking 'today' to for easier unit testing"""
    return date.fromisoformat("2022-09-15")


@pytest.fixture
def mock_response() -> Any:
    mock_response = mock_response_from_file("nflpickem/mock_odds.json")
    responses.add(responses.GET, GET_ODDS_URL, json=mock_response, status=200)
    return responses


@responses.activate
def test_call_odds_api(mock_response: Any) -> None:
    """Ensure that the mock API call works and returns all 30 games in mock_odds.json"""
    games_from_mock_json = _call_odds_api()
    assert len(games_from_mock_json) == 30
    assert len(mock_response.calls) == 1


@responses.activate
def test_e2e(mock_today: date, mock_response: Any) -> None:
    os.environ[ENV_API_TOKEN] = "mock-api-token"
    sorted_games = generate_picks(mock_today)
    assert len(sorted_games) == 15

    # ensure games are in sorted order
    for ndx in range(1, len(sorted_games)):
        game = sorted_games[ndx]
        prev_game = sorted_games[ndx - 1]
        assert abs(game.home_spread_avg) <= abs(prev_game.home_spread_avg)

    assert len(mock_response.calls) == 1
