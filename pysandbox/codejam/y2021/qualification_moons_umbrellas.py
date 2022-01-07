# https://codingcompetitions.withgoogle.com/codejam/round/000000000043580a/00000000006d1145
import logging
import sys
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


def calc(cj_cost: int, jc_cost: int, mural: List[str]) -> int:
    """NOTE: `mural` must not have any ? in it"""
    cost = 0
    for ndx, let in enumerate(mural):
        if let not in "CJ":
            raise RuntimeError(f"mural={mural} must only have C's and J's")
        if let == "C" and (ndx + 1 < len(mural) and mural[ndx + 1] == "J"):
            cost += cj_cost
        if let == "J" and (ndx + 1 < len(mural) and mural[ndx + 1] == "C"):
            cost += jc_cost
    return cost


def replace_letter(c_status: Optional[int], j_status: Optional[int]) -> str:
    if c_status is not None and j_status is not None and c_status <= j_status:
        return "C"
    elif c_status is not None and j_status is not None and c_status > j_status:
        return "J"

    return "?"


def minimize(cj_cost: int, jc_cost: int, mural: List[str]) -> int:
    logger.debug(f"Minimizing cost for: cj_cost={cj_cost} jc_cost={jc_cost} mural={mural}")

    mural_copy = mural.copy()
    questions_s = len(["?" for let in mural_copy if let == "?"])
    expensive_combo = ["C", "J"] if cj_cost >= jc_cost else ["J", "C"]
    expensive_cost = cj_cost if cj_cost >= jc_cost else jc_cost
    cheaper_combo = ["J", "C"] if cj_cost >= jc_cost else ["C", "J"]
    cheaper_cost = jc_cost if cj_cost >= jc_cost else cj_cost
    c_zero_combo = ["C", "C"]
    j_zero_combo = ["J", "J"]
    try_bonus = None

    if mural_copy[0:2] == ["?", "?"] and cheaper_cost < 0:
        logger.debug("Detected bonus opportunity!")
        try_bonus = cheaper_combo + mural_copy[2:]

    pass_num = 0
    while "?" in mural_copy:
        pass_num += 1
        for ndx in range(len(mural_copy)):
            let = mural_copy[ndx]
            if let == "?":
                prev_let = mural_copy[ndx - 1] if ndx > 0 else None
                next_let = mural_copy[ndx + 1] if ndx + 1 < len(mural_copy) else None
                logger.debug(f"Found let={let} at ndx={ndx}. prev={prev_let} next={next_let}: {mural_copy}")

                c_status = None
                j_status = None

                # Try "C" first...
                try_c = [[prev_let, "C"], ["C", next_let]]
                if cheaper_cost < 0 and cheaper_combo in try_c:
                    c_status = cheaper_cost
                elif c_zero_combo in try_c:
                    c_status = 0
                elif expensive_combo in try_c:
                    c_status = expensive_cost
                elif cheaper_combo in try_c:
                    c_status = cheaper_cost

                # Try "J" next...
                try_j = [[prev_let, "J"], ["J", next_let]]
                if cheaper_cost < 0 and cheaper_combo in try_j:
                    j_status = cheaper_cost
                elif j_zero_combo in try_j:
                    j_status = 0
                elif expensive_combo in try_j:
                    j_status = expensive_cost
                elif cheaper_combo in try_j:
                    j_status = cheaper_cost

                logger.debug(f"   Trying 'C' for ndx={ndx} --> {c_status}")
                logger.debug(f"   Trying 'J' for ndx={ndx} --> {j_status}")
                mural_copy[ndx] = replace_letter(c_status, j_status)

        questions_e = len(["?" for let in mural_copy if let == "?"])
        logging.debug(f"After pass={pass_num}, we have: {mural_copy} start?={questions_s} end?={questions_e}")
        if questions_s == questions_e:
            logging.debug("We didn't figure out any new '?'... Guess 'C'")
            ndx = mural_copy.index("?")
            mural_copy[ndx] = "C"

    cost = calc(cj_cost, jc_cost, mural_copy)
    logger.debug(f"Minimized mural: {mural_copy} with cost={cost}")

    if try_bonus:
        logger.debug("Seeing if capitalizing on 'bonus' helps us...")
        new_cost = minimize(cj_cost, jc_cost, try_bonus)
        logger.debug(f"orig_cost={cost} ; bonus_cost={new_cost}")
        cost = new_cost if new_cost < cost else cost

    return cost


def main(sample_file: Optional[Path] = None) -> None:
    with sample_file.open("r") if sample_file else sys.stdin as f:
        num_tests = int(f.readline())

        for case in range(1, num_tests + 1):
            cj_cost, jc_cost, mural = f.readline().split()
            mural_list = [let for let in mural]
            print(f"Case #{case}: {minimize(int(cj_cost), int(jc_cost), mural_list)}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
