import ast
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Generator, Iterator

CODE = "X"
VERSION = "0.0.2"
FUNCTION_ARGS_CODE = f"{CODE}001"
ASYNC_FUNCTION_ARGS_CODE = f"{CODE}002"

IGNORE_ARG_NAMES = [
    "self",
    "cls",
]


@dataclass
class Problem:
    lineno: "int"
    col_offset: "int"
    reason: "str"


class NumPositionalArgsVisitor(ast.NodeVisitor):
    _problems: "list[Problem]"

    def __init__(self, max_n_args: "int" = 1) -> "None":
        self._max_n_args = max_n_args
        self._problems = []

    def visit_FunctionDef(self, node: "ast.FunctionDef") -> "None":
        n_args = len([arg for arg in node.args.args if arg.arg not in IGNORE_ARG_NAMES])
        if self._max_n_args < n_args:
            self._problems.append(
                Problem(
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                    reason=self._build_reason(
                        code=FUNCTION_ARGS_CODE,
                        n_args=n_args,
                    ),
                ),
            )

    def visit_AsyncFunctionDef(self, node: "ast.AsyncFunctionDef") -> "None":
        n_args = len([arg for arg in node.args.args if arg.arg not in IGNORE_ARG_NAMES])
        if self._max_n_args < n_args:
            self._problems.append(
                Problem(
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                    reason=self._build_reason(
                        code=ASYNC_FUNCTION_ARGS_CODE,
                        n_args=n_args,
                    ),
                ),
            )

    @classmethod
    def _build_reason(cls, *, code: "str", n_args: "int") -> "str":
        return f"{code} Found {n_args} positional args."

    def iter_problem(self) -> "Iterator[Problem]":
        yield from self._problems


class NumPositionalArgsChecker:
    name = "num_positional_args"
    version = VERSION
    code = CODE

    def __init__(self, tree: "ast.AST") -> "None":
        self.tree = tree

    def run(self) -> "Generator[tuple[int, int, str, type[Any]], None, None]":
        visitor = NumPositionalArgsVisitor()
        visitor.visit(self.tree)
        for problem in visitor.iter_problem():
            yield problem.lineno, problem.col_offset, problem.reason, type(self)
