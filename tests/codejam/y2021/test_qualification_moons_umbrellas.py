from pathlib import Path
from typing import List

import pytest

import pysandbox.codejam.y2021.qualification_moons_umbrellas as my_module
from pysandbox.codejam.y2021.qualification_moons_umbrellas import (
    calc,
    main,
    minimize,
    replace_letter,
)


@pytest.fixture
def sample_path() -> Path:
    module_path = Path(my_module.__file__).resolve()
    sample_path = module_path.parent / "moons_umbrellas_sample1.txt"
    assert sample_path.exists()
    return sample_path


def test_replace_letter() -> None:
    assert replace_letter(0, 0) == "C"
    assert replace_letter(5, 5) == "C"

    assert replace_letter(0, 2) == "C"
    assert replace_letter(2, 0) == "J"
    assert replace_letter(2, 3) == "C"
    assert replace_letter(3, 2) == "J"

    assert replace_letter(-3, 0) == "C"
    assert replace_letter(1, -3) == "J"
    assert replace_letter(-1, -3) == "J"

    assert replace_letter(None, 2) == "?"


def _str_to_list(str_value: str) -> List[str]:
    return [let for let in str_value]


def test_calc() -> None:
    assert calc(2, 3, _str_to_list("CJCCCC")) == 5
    assert calc(2, 3, _str_to_list("CJJCCC")) == 5
    assert calc(2, 3, _str_to_list("CJCCCJ")) == 7
    assert calc(2, 3, _str_to_list("CJJCCJ")) == 7

    with pytest.raises(RuntimeError):
        calc(2, 3, _str_to_list("CJJCC?"))


def test_minimize() -> None:
    assert minimize(2, 3, _str_to_list("CJ?CC?")) == 5
    assert minimize(4, 2, _str_to_list("CJCJ")) == 10
    assert minimize(1, 3, _str_to_list("C?J")) == 1
    assert minimize(2, 5, _str_to_list("??J???")) == 0
    assert minimize(2, 5, _str_to_list("??????")) == 0


def test_minimize_negative() -> None:
    assert minimize(2, -5, _str_to_list("??JJ??")) == -8
    assert minimize(100, -5, _str_to_list("??JJ??")) == -5
    assert minimize(2, -5, _str_to_list("???CJ???")) == -11


def test_main(sample_path: Path) -> None:
    main(sample_path)  # Will ensure to exceptions are thrown at least
