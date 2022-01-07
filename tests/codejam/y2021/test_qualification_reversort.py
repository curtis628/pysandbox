from pathlib import Path

import pytest

import pysandbox.codejam.y2021.qualification_reversort as qualification_reversort
from pysandbox.codejam.y2021.qualification_reversort import (
    calc_cost,
    main,
    parse_sample,
)


@pytest.fixture
def sample_path() -> Path:
    module_path = Path(qualification_reversort.__file__).resolve()
    sample_path = module_path.parent / "reversort_sample1.txt"
    assert sample_path.exists()
    return sample_path


def test_calc_cost() -> None:
    assert calc_cost([4, 2, 1, 3]) == 6
    assert calc_cost([1, 2]) == 1
    assert calc_cost([7, 6, 5, 4, 3, 2, 1]) == 12


def test_parse_sample(sample_path: Path) -> None:
    tests = parse_sample(sample_path)
    assert len(tests) == 3
    assert tests[0].int_list == [4, 2, 1, 3]
    assert tests[1].int_list == [1, 2]
    assert tests[2].int_list == [7, 6, 5, 4, 3, 2, 1]


def test_main(sample_path: Path) -> None:
    main(sample_path)  # Will ensure to exceptions are thrown at least
