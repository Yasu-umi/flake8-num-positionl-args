import ast

import pytest

from src.flake8_num_positionl_args import NumPositionalArgsChecker


@pytest.mark.parametrize(
    ["source", "lineno", "col_offset", "reason"],
    [
        [
            """
def main(a: int, b, *, c):
    print('Hello, World!')
        """,
            2,
            0,
            "X001 Found 2 positional args.",
        ],
        [
            """
async def main(a: int, b, *, c):
    print('Hello, World!')
        """,
            2,
            0,
            "X002 Found 2 positional args.",
        ],
    ],
)
def test_error(source: str, lineno: int, col_offset: int, reason: str):
    checker = NumPositionalArgsChecker(ast.parse(source))
    assert [
        (lineno, col_offset, reason, NumPositionalArgsChecker),
    ] == list(checker.run())


@pytest.mark.parametrize(
    ["source"],
    [
        [
            """
async def main(*, a: int, b):
    print('xHello, World!')
        """
        ],
    ],
)
def test_success(source: str):
    checker = NumPositionalArgsChecker(ast.parse(source))
    assert [] == list(checker.run())
