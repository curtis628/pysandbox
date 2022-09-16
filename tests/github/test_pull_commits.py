import json
import sys
from pathlib import Path
from typing import Any

import pytest
import responses

import pysandbox.github.pull_commits as pull_commits
from pysandbox.common_test import run_and_expect

EXPECTED_PAGE_2_LINK = "https://api.github.com/repositories/1362490/commits?per_page=4&page=2"
EXPECTED_PAGE_3_LINK = "https://api.github.com/repositories/1362490/commits?per_page=4&page=3"

PAGE_1_HEADER = f'<{EXPECTED_PAGE_2_LINK}>; rel="next", <https://ignore/commits?per_page=4&page=1524>; rel="last"'
PAGE_2_HEADER = (
    f'<{EXPECTED_PAGE_3_LINK}>; rel="next", <ignore/commits?per_page=4&page=1524>; rel="last", '
    f'<ignore/commits?per_page=4&page=1>; rel="first", <ignore/commits?per_page=4&page=1>; rel="prev"'
)
PAGE_3_HEADER = (
    '<ignore/commits?per_page=4&page=4>; rel="next", <ignore/commits?per_page=4&page=1524>; rel="last", '
    '<ignore/commits?per_page=4&page=1>; rel="first", <ignore/commits?per_page=4&page=2>; rel="prev"'
)

OWNER = "test_owner"
REPO = "test_repo"
TEST_PER_PAGE = 4

# Hack to modify per_page constant for easier testing...
pull_commits.DEFAULT_PER_PAGE = TEST_PER_PAGE


def _mock_response_from_file(filename: str) -> Any:
    """Returns decoded JSON from `filename`"""
    this_file = sys.modules[__name__].__file__
    this_file_path = Path(this_file)  # type: ignore
    mock_1_file = this_file_path.parent / filename
    with mock_1_file.open() as f:
        response = json.load(f)
    return response


@pytest.fixture
def single_call_first_link() -> str:
    return f"{pull_commits.GIT_BASE_URL}/repos/{OWNER}/{REPO}/commits?per_page={TEST_PER_PAGE}"


@pytest.fixture
def mock_response(single_call_first_link: str) -> Any:
    page_1 = _mock_response_from_file("mock_page_1.json")
    responses.add(responses.GET, single_call_first_link, json=page_1, status=200, headers={"Link": PAGE_1_HEADER})
    return responses


@pytest.fixture
def multi_call_first_link() -> str:
    return f"{pull_commits.GIT_BASE_URL}/repos/{OWNER}/{REPO}/commits?per_page=10"


@pytest.fixture
def mock_responses(multi_call_first_link: str) -> Any:
    page_1 = _mock_response_from_file("mock_page_1.json")
    page_2 = _mock_response_from_file("mock_page_2.json")
    page_3 = _mock_response_from_file("mock_page_3.json")

    responses.add(responses.GET, multi_call_first_link, json=page_1, status=200, headers={"Link": PAGE_1_HEADER})
    responses.add(responses.GET, EXPECTED_PAGE_2_LINK, json=page_2, status=200, headers={"Link": PAGE_2_HEADER})
    responses.add(responses.GET, EXPECTED_PAGE_3_LINK, json=page_3, status=200, headers={"Link": PAGE_3_HEADER})
    return responses


@responses.activate
def test_single_call(single_call_first_link: str, mock_response: Any) -> None:
    actual = pull_commits.pull_commits(OWNER, REPO, TEST_PER_PAGE)
    assert len(actual) == TEST_PER_PAGE
    assert actual[0].sha == "d15a3b"
    assert actual[3].commit_date == "2022-01-06T17:57:59Z"

    # ensure expected API calls
    assert len(mock_response.calls) == 1
    assert mock_response.calls[0].request.url == single_call_first_link


@responses.activate
def test_multi_call(multi_call_first_link: str, mock_responses: Any) -> None:
    actual = pull_commits.pull_commits(OWNER, REPO, 10)
    assert len(actual) == 10
    assert actual[0].sha == "d15a3b"
    assert actual[3].commit_date == "2022-01-06T17:57:59Z"
    assert actual[5].author == "test@gmail.com"
    assert actual[9].message == "General cleanup for 2.27.0"

    # ensure expected API calls. per_page=4 + num_commits=10 ==> 3 API calls
    assert len(mock_responses.calls) == 3
    assert mock_responses.calls[0].request.url == multi_call_first_link
    assert mock_responses.calls[1].request.url == EXPECTED_PAGE_2_LINK
    assert mock_responses.calls[2].request.url == EXPECTED_PAGE_3_LINK


def test_parse_help() -> None:
    test_argv = ["pysandbox/github/pull_commits.py", "--help"]
    run_and_expect(lambda: pull_commits.main(), test_argv, raises=SystemExit, check_code=True)
