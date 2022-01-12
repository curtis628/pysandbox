#
# Helpful, reusable logic across many test scripts
#

import sys
from typing import Callable, Optional, Type

import pytest


def run_with_argv(method: Callable[[], None], new_argv: list[str] = []) -> None:
    """Helper method that updates sys.argv (and puts it back after)"""
    old_argv = sys.argv
    try:
        sys.argv = new_argv
        method()
    finally:
        sys.argv = old_argv


def run_and_expect(
    method: Callable[[], None],
    test_argv: list[str] = [],
    raises: Optional[Type[SystemExit]] = None,
    check_code: bool = False,
) -> None:
    """Helper that runs `method` with `test_argv`. Expects `error_class` with optional `exit_code`"""
    if raises:
        with pytest.raises(raises) as excinfo:
            run_with_argv(method, test_argv)
        if check_code:
            assert excinfo.value.code == 0
    else:
        run_with_argv(method, test_argv)
