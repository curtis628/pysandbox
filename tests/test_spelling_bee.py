import shutil
from pathlib import Path

import pytest
from python_sandbox.spelling_bee import solve_puzzle

TEST_DICTIONARY: list[str] = [
    "apple",
    "banana",
    "orange",
    "grape",
    "strawberry",
    "ale",
]


@pytest.fixture(scope="session")
def test_dictionary_path(tmp_path_factory: pytest.TempPathFactory):
    dictionary_with_newlines = [line + "\n" for line in TEST_DICTIONARY]
    dictionary_path = tmp_path_factory.getbasetemp() / "test-dictionary.txt"
    with dictionary_path.open("w") as dictionary_test_file:
        dictionary_test_file.writelines(dictionary_with_newlines)

    yield dictionary_path

    shutil.rmtree(tmp_path_factory.getbasetemp())


def test_empty(test_dictionary_path: Path):
    actual = solve_puzzle("z", "abcdef", dictionary_file=test_dictionary_path)
    assert len(actual) == 0


def test_valid(test_dictionary_path: Path):
    actual = solve_puzzle("a", "plebn", dictionary_file=test_dictionary_path)
    assert actual == ["banana", "apple"]

def test_valid_case_sensitive(test_dictionary_path: Path):
    actual = solve_puzzle("A", "pLEbN", dictionary_file=test_dictionary_path)
    assert actual == ["banana", "apple"]

def test_too_short(test_dictionary_path: Path):
    actual = solve_puzzle("a", "le", dictionary_file=test_dictionary_path)
    assert actual == []
