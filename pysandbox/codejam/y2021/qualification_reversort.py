# See: https://codingcompetitions.withgoogle.com/codejam/round/000000000043580a/00000000006d0a5c
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TestConfig:
    list_len: int
    int_list: List[int]


def parse_sample(sample_file: Optional[Path] = None) -> List[TestConfig]:
    tests: List[TestConfig] = []
    with sample_file.open("r") if sample_file else sys.stdin as f:
        num_tests = int(f.readline())

        for test in range(num_tests):
            list_len = int(f.readline())
            list_as_str = f.readline()
            int_list = [int(val) for val in list_as_str.split(" ")]
            tests.append(TestConfig(list_len, int_list))
        logger.debug(f"Processing {num_tests} tests: {tests}")
    return tests


def _find_lowest_ndx(int_list: List[int]) -> int:
    lowest_ndx = 0
    lowest = None
    for ndx, val in enumerate(int_list):
        if lowest is None or val < lowest:
            lowest = val
            lowest_ndx = ndx

    return lowest_ndx


def calc_cost(int_list: List[int]) -> int:
    """Given in-order list, returning "cost" of Reversort"""
    logger.debug(f"Processing list: {int_list}")
    total_cost = 0
    for ndx in range(len(int_list) - 1):
        j = ndx + _find_lowest_ndx(int_list[ndx:]) + 1
        list_begin = list(reversed(int_list[ndx:j]))
        list_end = int_list[j:]
        int_list = int_list[0:ndx] + list_begin + list_end

        cost = j - ndx
        logger.debug(f"i={ndx+1} j={j}: cost={cost} . current={int_list}")
        total_cost += cost
    return total_cost


def main(sample_file: Optional[Path] = None) -> None:
    tests: List[TestConfig] = parse_sample(sample_file)
    for ndx, test in enumerate(tests):
        print(f"Case #{ndx+1}: {calc_cost(test.int_list)}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
