import shutil
import sys
from pathlib import Path
from typing import Callable, Generator, Optional, Type

import pytest

from pysandbox.spelling_bee import main, solve_puzzle

TEST_DICTIONARY: list[str] = [
    "apple",
    "banana",
    "orange",
    "grape",
    "strawberry",
    "ale",
]


@pytest.fixture(scope="session")
def test_dictionary_path(tmp_path_factory: pytest.TempPathFactory) -> Generator[Path, None, None]:
    """Creates a small, temporary dictionary text file based on `TEST_DICTIONARY`"""
    dictionary_with_newlines = [line + "\n" for line in TEST_DICTIONARY]
    dictionary_path = tmp_path_factory.getbasetemp() / "test-dictionary.txt"
    with dictionary_path.open("w") as dictionary_test_file:
        dictionary_test_file.writelines(dictionary_with_newlines)

    yield dictionary_path

    # Cleanup the temporary folder when done
    shutil.rmtree(tmp_path_factory.getbasetemp())


def test_empty(test_dictionary_path: Path) -> None:
    actual = solve_puzzle("z", "abcdef", dictionary_file=test_dictionary_path)
    assert len(actual) == 0


def test_valid(test_dictionary_path: Path) -> None:
    actual = solve_puzzle("a", "plebn", dictionary_file=test_dictionary_path)
    assert actual == ["banana", "apple"]


def test_valid_case_sensitive(test_dictionary_path: Path) -> None:
    actual = solve_puzzle("A", "pLEbN", dictionary_file=test_dictionary_path)
    assert actual == ["banana", "apple"]


def test_too_short(test_dictionary_path: Path) -> None:
    actual = solve_puzzle("a", "le", dictionary_file=test_dictionary_path)
    assert actual == []


def test_bad_input_letters(test_dictionary_path: Path) -> None:
    with pytest.raises(RuntimeError) as excinfo:
        solve_puzzle("ab", "abcdef", dictionary_file=test_dictionary_path)
    assert "must_letter=ab must be of length one" in str(excinfo.value)

    with pytest.raises(RuntimeError) as excinfo:
        solve_puzzle("", "abcdef", dictionary_file=test_dictionary_path)
    assert "must_letter= must be of length one" in str(excinfo.value)

    with pytest.raises(RuntimeError) as excinfo:
        solve_puzzle("a", "", dictionary_file=test_dictionary_path)
    assert "may_letters= cannot be empty" in str(excinfo.value)


def test_bad_dictionary(tmp_path: Path) -> None:
    not_exists = tmp_path / "non-existent-dictionary.txt"
    with pytest.raises(RuntimeError) as excinfo:
        solve_puzzle("a", "plebn", dictionary_file=not_exists)
    assert "does not exist" in str(excinfo.value)


def _run_with_argv(method: Callable[[], None], new_argv: list[str] = []) -> None:
    """Helper method that updates sys.argv (and puts it back after)"""
    old_argv = sys.argv
    try:
        sys.argv = new_argv
        method()
    finally:
        sys.argv = old_argv


def _run_and_expect(
    method: Callable[[], None],
    test_argv: list[str] = [],
    raises: Optional[Type[SystemExit]] = None,
    check_code: bool = False,
) -> None:
    """Helper that runs `method` with `test_argv`. Expects `error_class` with optional `exit_code`"""
    if raises:
        with pytest.raises(raises) as excinfo:
            _run_with_argv(method, test_argv)
        if check_code:
            assert excinfo.value.code == 0
    else:
        _run_with_argv(method, test_argv)


def test_parse_help() -> None:
    test_argv = ["pysandbox/spelling_bee.py", "--help"]
    _run_and_expect(lambda: main(), test_argv, raises=SystemExit, check_code=True)


def test_e2e(test_dictionary_path: Path) -> None:
    test_argv = [
        "pysandbox/spelling_bee.py",
        "--must-letter=a",
        "--optional-letters=plebn",
        f"--dictionary-file={test_dictionary_path}",
    ]
    _run_and_expect(lambda: main(), test_argv)
