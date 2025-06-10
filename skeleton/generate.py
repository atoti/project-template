from __future__ import annotations

import re
from collections.abc import Mapping
from os import linesep
from typing import (
    Annotated,
    Literal,
    TypeVar,
    get_args,
    get_origin,
    overload,
)

import atoti as tt
from pydantic import validate_call
from pydantic.alias_generators import to_pascal
from typing_extensions import is_typeddict

from ._node import Node
from .typing import SessionSkeleton

_T = TypeVar("_T", bound=type)


def _identifier(name: str, /, *, kind: Literal["attribute", "class"]) -> str:
    identifier = re.sub(r"\W|^(?=\d)", "_", name)
    match kind:
        case "attribute":
            return identifier.upper()
        case "class":
            return to_pascal(identifier)


def _indent(code: str, /) -> str:
    return f"{' ' * 4}{code}"


def _private(identifier: str, /) -> str:
    return f"_{identifier}"


def _class_name(type_: type) -> str:
    return _private(type_.__name__)


_COUNTER = [0]


def _generate_unique_class_name() -> str:
    value = _COUNTER[0]
    _COUNTER[0] += 1
    return _private(f"Generated{value}")


_CONTEXT_VAR_NAME = _private("CONTEXT_VAR")
_KEY_PROPERTY_NAME = "key"
_NAME_PROPERTY_NAME = "name"
_PATH_PROPERTY_NAME = _private("path")
_SESSION_CONSTANT_NAME = tt.Session.__name__.upper()
_SESSION_SET_METHOD_NAME = "set"
_TABLES_CLASS_NAME = _private("Tables")
_VALUE_PROPERTY_NAME = "value"


def _generate_abstract_class(
    type_: type,
    /,
    *,
    #  key_length: int,
    parent_type: type,
    path: str = "",
) -> list[str]:
    parent_attribute_name = _private(_private("parent"))
    return [
        f"class {_class_name(type_)}(ABC):",
        *(
            _indent(line)
            for line in [
                f"def __init__(self, *, parent: {_class_name(parent_type)}) -> None:",
                _indent(f"self.{parent_attribute_name}: Final = parent"),
                "@property",
                "@abstractmethod",
                f"def {_KEY_PROPERTY_NAME}(self) -> str: ...",
                "@property",
                "@abstractmethod",
                f"def {_NAME_PROPERTY_NAME}(self) -> str: ...",
                "@final",
                "@property",
                f"def {_VALUE_PROPERTY_NAME}(self) -> tt.{type_.__name__}:",
                _indent(
                    f"return self.{parent_attribute_name}.value{path}[self.{_KEY_PROPERTY_NAME}]"
                ),
            ]
        ),
    ]


@overload
def _generate_homogeneous_node_class_name_and_lines(
    type_: type, name: str, /
) -> tuple[str, list[str]]: ...
@overload
def _generate_homogeneous_node_class_name_and_lines(
    type_: type,
    name: str,
    /,
    *,
    class_name_from_child_name: Mapping[str, str],
    parent_type: type,
) -> tuple[str, list[str]]: ...
def _generate_homogeneous_node_class_name_and_lines(
    type_: type,
    name: str,
    /,
    *,
    class_name_from_child_name: Mapping[str, str] | None = None,
    parent_type: type | None = None,
) -> tuple[str, list[str]]:
    return (
        class_name := _generate_unique_class_name(),
        [
            "@final",
            f"class {class_name}({_class_name(type_)}):",
            *(
                []
                if not class_name_from_child_name or parent_type is None
                else [
                    *(
                        _indent(line)
                        for line in [
                            f"def __init__(self, *, parent: {_class_name(parent_type)}) -> None:",
                            *(
                                _indent(line)
                                for line in [
                                    "super().__init__(parent=parent)",
                                    *(
                                        f"self.{_identifier(child_name, kind='attribute')}: Final = {class_name}(parent=self)"
                                        for child_name, class_name in class_name_from_child_name.items()
                                    ),
                                ]
                            ),
                        ]
                    )
                ]
            ),
            *(
                _indent(line)
                for line in [
                    "@property",
                    "@override",
                    f"def {_NAME_PROPERTY_NAME}(self) -> str:",
                    _indent(f'return r"""{name}"""'),
                ]
            ),
        ],
    )


def _generate_table_class_name_and_lines(
    table: _TableSkeleton, /, *, name: str
) -> tuple[str, list[str]]:
    column_class_name_and_lines_from_column_name = {
        column_name: _generate_homogeneous_node_class_name_and_lines(
            tt.Column, column_name
        )
        for column_name in table
    }
    class_name, lines = _generate_homogeneous_node_class_name_and_lines(
        tt.Table,
        name,
        class_name_from_child_name={
            child_name: class_name
            for child_name, (
                class_name,
                _,
            ) in column_class_name_and_lines_from_column_name.items()
        },
        parent_type=tt.Session,
    )
    return class_name, [
        *(
            line
            for _, lines in column_class_name_and_lines_from_column_name.values()
            for line in lines
        ),
        *lines,
    ]


def _generate_tables(tables: TablesSkeleton, /) -> list[str]:
    table_class_name_and_lines_from_table_name = {
        table_name: _generate_table_class_name_and_lines(table, name=table_name)
        for table_name, table in tables.items()
    }
    return [
        *(
            line
            for _, lines in table_class_name_and_lines_from_table_name.values()
            for line in lines
        ),
        "@final",
        f"class {_TABLES_CLASS_NAME}:",
        *(
            _indent(line)
            for line in [
                f"def __init__(self, *, parent: {_class_name(tt.Session)}) -> None:",
                *(
                    _indent(
                        f"self.{_identifier(name, kind='attribute')}: Final = {table_class_name_and_lines_from_table_name[name][0]}(parent=parent)"
                    )
                    for name in tables
                ),
            ]
        ),
    ]


def _generate_skeleton(
    session_skeleton: _T,
    /,
    *,
    session_skeleton_type: type[_T],
    session_type: type,
) -> list[str]:
    print(
        session_skeleton_type,
        is_typeddict(session_skeleton_type),
        session_skeleton_type.__annotations__,
    )
    return [
        # *_generate_abstract_class(
        #     tt.Column,
        #     # key_len="str",
        #     parent_type=tt.Table,
        # ),
        # *_generate_abstract_class(
        #     tt.Table,
        #     # key_type="str",
        #     parent_type=tt.Session,
        #     path=".tables",
        # ),
        # *_generate_tables(skeleton["tables"]),
        "@final",
        f"class {_class_name(session_type)}:",
        *(
            _indent(line)
            for line in [
                "def __init__(self) -> None:",
                *(
                    _indent(line)
                    for line in [
                        f"self.tables: Final = {_TABLES_CLASS_NAME}(parent=self)"
                    ]
                ),
                "@contextmanager",
                f"def {_SESSION_SET_METHOD_NAME}(self, session: tt.{session_type.__name__}, /) -> Generator[None, None, None]:",
                *(
                    _indent(line)
                    for line in [
                        f"{_CONTEXT_VAR_NAME}.set(session)",
                        "yield None",
                    ]
                ),
                "@property",
                f"def {_VALUE_PROPERTY_NAME}(self) -> tt.{session_type.__name__}:",
                *(
                    _indent(line)
                    for line in [
                        "try:",
                        _indent(f"return {_CONTEXT_VAR_NAME}.get()"),
                        "except LookupError as error:",
                        _indent(
                            f'message = "Call `{_class_name(session_type)}.{_SESSION_SET_METHOD_NAME}` before."'
                        ),
                        _indent("raise RuntimeError(message) from error"),
                    ]
                ),
            ]
        ),
    ]


@validate_call
def generate(session_skeleton: SessionSkeleton, /) -> str:
    assert get_origin(SessionSkeleton) is Annotated
    session_skeleton_type, session_skeleton_node = get_args(SessionSkeleton)
    assert isinstance(session_skeleton_node, Node)
    assert session_skeleton_node.key_length is None
    assert session_skeleton_node.path_from_parent_value == ""
    lines = [
        "from __future__ import annotations",
        "from abc import ABC, abstractmethod",
        "from collections.abc import Generator",
        "from contextlib import contextmanager",
        "from contextvars import ContextVar",
        "from typing import Final, final",
        "import atoti as tt",
        "from typing_extensions import override",
        f'{_CONTEXT_VAR_NAME}: ContextVar[tt.Session] = ContextVar("skeleton")',
        *_generate_skeleton(
            session_skeleton,
            session_skeleton_type=session_skeleton_type,
            session_type=session_skeleton_node.value_type,
        ),
        f"{_SESSION_CONSTANT_NAME} = {_class_name(session_skeleton_node.value_type)}()",
    ]
    assert not any(linesep in line for line in lines)
    return linesep.join(lines)
