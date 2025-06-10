import re
from os import linesep
from typing import Literal, TypeAlias

from pydantic import validate_call
from pydantic.alias_generators import to_pascal

from .typing import Skeleton, Table, Tables

_ClassKind: TypeAlias = Literal["Column", "Table"]


def _identifier(name: str, /, *, kind: Literal["attribute", "class"]) -> str:
    identifier = re.sub(r"\W|^(?=\d)", "_", name)
    match kind:
        case "attribute":
            return identifier.upper()
        case "class":
            return to_pascal(identifier)


def _private(identifier: str, /) -> str:
    return f"_{identifier}"


def _class_name(*parts: str, kind: _ClassKind) -> str:
    return _private(f"{_identifier(' '.join(parts), kind='class')}{kind}")


def _indent(code: str, /) -> str:
    return f"{' ' * 4}{code}"


_CONTEXT_VAR_NAME = _private("CONTEXT_VAR")
_KEY_PROPERTY_NAME = "key"
_SESSION_FUNCTION_NAME = _private("session")
_SKELETON_CLASS_NAME = _private("Skeleton")
_SKELETON_OF_METHOD_NAME = "of"
_TABLES_CLASS_NAME = _private("Tables")
_VALUE_PROPERTY_NAME = "value"


def _generate_abstract_class(
    kind: _ClassKind,
    /,
    *,
    key_type: str,
    parent_type: str | None = None,
    path: str,
) -> list[str]:
    match parent_type:
        case str():
            parent_attribute_name = _private(_private("parent"))
            init_lines = [
                f"def __init__(self, *, parent: {parent_type}) -> None:",
                _indent(f"self.{parent_attribute_name}: Final = parent"),
            ]
            parent = f"self.{parent_attribute_name}"
        case None:
            init_lines = []
            parent = f"{_SESSION_FUNCTION_NAME}()"

    return [
        f"class {_class_name(kind=kind)}(ABC):",
        *(
            _indent(line)
            for line in [
                *init_lines,
                "@property",
                "@abstractmethod",
                f"def {_KEY_PROPERTY_NAME}(self) -> {key_type}: ...",
                "@final",
                "@property",
                f"def {_VALUE_PROPERTY_NAME}(self) -> tt.{kind}:",
                _indent(f"return {parent}.{path}[self.{_KEY_PROPERTY_NAME}]"),
            ]
        ),
    ]


def _generate_column(column_name: str, /, *, table_name: str) -> list[str]:
    return [
        "@final",
        f"class {_class_name(table_name, column_name, kind='Column')}({_class_name(kind='Column')}):",
        *(
            _indent(line)
            for line in [
                "@property",
                "@override",
                "def key(self) -> str:",
                _indent(f'return r"""{column_name}"""'),
            ]
        ),
    ]


def _generate_table(table: Table, /, *, name: str) -> list[str]:
    return [
        *(
            line
            for column_name in table
            for line in _generate_column(column_name, table_name=name)
        ),
        "@final",
        f"class {_class_name(name, kind='Table')}({_class_name(kind='Table')}):",
        *(
            _indent(line)
            for line in [
                "def __init__(self) -> None:",
                *(
                    f"""{_indent(f"self.{_identifier(column_name, kind='attribute')}: Final = {_class_name(name, column_name, kind='Column')}(parent=self)")}"""
                    for column_name in table
                ),
            ]
        ),
        *(
            _indent(line)
            for line in [
                "@property",
                "@override",
                "def key(self) -> str:",
                _indent(f'return r"""{name}"""'),
            ]
        ),
    ]


def _generate_tables(tables: Tables, /) -> list[str]:
    return [
        *(
            line
            for name, table in tables.items()
            for line in _generate_table(table, name=name)
        ),
        "@final",
        f"class {_TABLES_CLASS_NAME}:",
        *(
            _indent(line)
            for line in [
                "def __init__(self) -> None:",
                *(
                    _indent(
                        f"self.{_identifier(name, kind='attribute')}: Final = {_class_name(name, kind='Table')}()"
                    )
                    for name in tables
                ),
            ]
        ),
    ]


def _generate_skeleton(skeleton: Skeleton, /) -> list[str]:
    return [
        *_generate_abstract_class("Table", key_type="str", path="tables"),
        *_generate_abstract_class(
            "Column",
            key_type="str",
            parent_type=_class_name(kind="Table"),
            path=_VALUE_PROPERTY_NAME,
        ),
        *_generate_tables(skeleton["tables"]),
        "@final",
        f"class {_SKELETON_CLASS_NAME}:",
        *(
            _indent(line)
            for line in [
                "def __init__(self) -> None:",
                *(
                    _indent(line)
                    for line in [f"self.tables: Final = {_TABLES_CLASS_NAME}()"]
                ),
                "@contextmanager",
                "def of(self, session: tt.Session, /) -> Generator[None, None, None]:",
                *(
                    _indent(line)
                    for line in [
                        f"{_CONTEXT_VAR_NAME}.set(session)",
                        "yield None",
                    ]
                ),
                "@property",
                "def session(self) -> tt.Session:",
                _indent(f"return {_SESSION_FUNCTION_NAME}()"),
            ]
        ),
    ]


@validate_call
def generate(skeleton: Skeleton, /) -> str:
    lines = [
        "# Generated skeleton, do not edit manually.",
        "from abc import ABC, abstractmethod",
        "from collections.abc import Generator",
        "from contextlib import contextmanager",
        "from contextvars import ContextVar",
        "from typing import Final, final",
        "import atoti as tt",
        "from typing_extensions import override",
        f'{_CONTEXT_VAR_NAME}: ContextVar[tt.Session] = ContextVar("skeleton")',
        f"def {_SESSION_FUNCTION_NAME}() -> tt.Session:",
        *(
            _indent(line)
            for line in [
                "try:",
                _indent(f"return {_CONTEXT_VAR_NAME}.get()"),
                "except LookupError as error:",
                _indent(f"method = {_SKELETON_CLASS_NAME}.{_SKELETON_OF_METHOD_NAME}"),
                _indent(
                    r'raise RuntimeError(f"Call `{method.__qualname__}` before.") from error'
                ),
            ]
        ),
        *_generate_skeleton(skeleton),
        f"SKELETON = {_SKELETON_CLASS_NAME}()",
    ]
    assert not any(linesep in line for line in lines)
    return linesep.join(lines)
