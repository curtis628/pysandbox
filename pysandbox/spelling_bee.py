import argparse
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_DICTIONARY_PATH: Path = Path("etc/dictionary-usa.txt")

"""Script that solves https://www.nytimes.com/puzzles/spelling-bee puzzles!"""


def acceptable_word(word: str, must_letter: str, may_letters: list[str]) -> bool:
    if len(word) < 4:
        return False
    acceptable_letters = [must_letter] + may_letters
    valid = must_letter in word
    if valid:
        for letter in word.lower():
            valid = letter in acceptable_letters
            if not valid:
                return False
    return valid


def solve_puzzle(must_letter: str, may_letters: str, dictionary_file: Path = DEFAULT_DICTIONARY_PATH) -> list[str]:
    dictionary_path = Path(dictionary_file)
    if not dictionary_path.exists():
        raise RuntimeError(f"Dictionary file: '{dictionary_path}' does not exist")
    if len(must_letter) != 1:
        raise RuntimeError(f"must_letter={must_letter} must be of length one")
    if len(may_letters) == 0:
        raise RuntimeError(f"may_letters={may_letters} cannot be empty")

    must_letter_low = must_letter.lower()
    may_letters_low = [letter.lower() for letter in may_letters]
    logger.debug(
        f"Solving puzzle with must_letter={must_letter_low} may_letters={may_letters_low} dict_file={dictionary_file}"
    )

    words = []
    with open(dictionary_path) as f:
        for line in f:
            word = line.strip()  # Strip newline char
            if acceptable_word(word, must_letter_low, may_letters_low):
                words.append(word)

    words.sort(key=lambda s: -len(s))
    for word in words:
        print(word)
    return words


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Logging initialized")

    parser = argparse.ArgumentParser("Spelling Bee Solver")
    parser.add_argument(
        "--dictionary-file",
        "-df",
        type=Path,
        default=DEFAULT_DICTIONARY_PATH,
        help=f"The dictionary text file to use. One word per line. Default: {DEFAULT_DICTIONARY_PATH}",
    )

    parser.add_argument(
        "--must-letter",
        help="The letter in the center of the puzzle, which must be in the answer at least once.",
    )

    parser.add_argument(
        "--optional-letters",
        help="The other letters that may be in the answer one or more times",
    )

    args = parser.parse_args()
    must_letter = args.must_letter or input("Must Letter: ")
    may_letters = args.optional_letters or input("May Letters: ")
    solve_puzzle(must_letter, may_letters, args.dictionary_file)


if __name__ == "__main__":
    main()
