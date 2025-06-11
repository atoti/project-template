from __future__ import annotations

import re
from collections.abc import Mapping, Set as AbstractSet
from os import linesep
from textwrap import dedent
from typing import Annotated, Literal, TypeVar, get_args, get_origin

import atoti as tt
from pydantic import TypeAdapter
from pydantic.alias_generators import to_pascal, to_snake
from typing_extensions import is_typeddict

from .node import Node

_T = TypeVar("_T")


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


_COUNTER = [0]


def _generate_unique_class_name() -> str:
    value = _COUNTER[0]
    _COUNTER[0] += 1
    return _private(f"Generated{value}")


_ATOTI_IMPORT_ALIAS = "tt"
_KEY_PROPERTY_NAME = "key"
_NAME_PROPERTY_NAME = "name"
_PARENT_PARAMETER_NAME = "parent"
_PARENT_PROPERTY_NAME = _private(_PARENT_PARAMETER_NAME)


def _atoti_class_name(type_: type, /) -> str:
    assert getattr(tt, type_.__name__) is type_
    return f"{_ATOTI_IMPORT_ALIAS}.{type_.__name__}"


def _attribute_name(type_: type, /) -> str:
    return to_snake(type_.__name__)


def _unwrap_type(type_: type[_T], /) -> tuple[type[_T], Node | None]:
    match get_origin(type_), get_args(type_):
        case origin, (unwrapped_type, (Node() as node)) if origin is Annotated:
            return unwrapped_type, node
        case _:
            return type_, None


SKELETON_CONSTANT_NAME = "SKELETON"


def _generate_class_name_and_lines(
    skeleton: _T,
    skeleton_type: type[_T],
    /,
    *,
    name: str | None,
    parent_type_name: str,
    parent_value_type: type,
    root_value_type: type,
) -> tuple[str, list[str]]:
    skeleton_type, node = _unwrap_type(skeleton_type)

    class_name = _generate_unique_class_name()

    lines: list[str] = []

    match get_origin(skeleton_type), get_args(skeleton_type):
        case origin, (name_type, value_type) if issubclass(origin, Mapping):
            assert name_type is str
            class_name_and_lines_from_child_name = {
                child_name: _generate_class_name_and_lines(
                    skeleton[child_name],
                    value_type,
                    name=child_name,
                    parent_type_name=parent_type_name if node is None else class_name,
                    parent_value_type=parent_value_type
                    if node is None
                    else node.value_type,
                    root_value_type=root_value_type,
                )
                for child_name in skeleton
            }
            for _, child_lines in class_name_and_lines_from_child_name.values():
                lines.extend(child_lines)
            extra_init_lines = [
                f"self.{_identifier(child_name, kind='attribute')}: Final = {child_class_name}({_PARENT_PARAMETER_NAME if node is None else 'self'})"
                for child_name, (
                    child_class_name,
                    _,
                ) in class_name_and_lines_from_child_name.items()
            ]
        case origin, (element_type,) if issubclass(origin, AbstractSet):
            class_name_and_lines_from_child_name = {
                child_name: _generate_class_name_and_lines(
                    child_name,
                    element_type,
                    name=child_name,
                    parent_type_name=parent_type_name if node is None else class_name,
                    parent_value_type=parent_value_type
                    if node is None
                    else node.value_type,
                    root_value_type=root_value_type,
                )
                for child_name in skeleton
            }
            for _, child_lines in class_name_and_lines_from_child_name.values():
                lines.extend(child_lines)
            extra_init_lines = [
                f"self.{_identifier(child_name, kind='attribute')}: Final = {child_class_name}({_PARENT_PARAMETER_NAME if node is None else 'self'})"
                for child_name, (
                    child_class_name,
                    _,
                ) in class_name_and_lines_from_child_name.items()
            ]
        case _:
            if is_typeddict(skeleton_type):
                class_name_and_lines_from_attribute_name = {
                    attribute_name: _generate_class_name_and_lines(
                        skeleton[attribute_name],
                        annotation,
                        name=None,
                        parent_type_name=parent_type_name
                        if node is None
                        else class_name,
                        parent_value_type=parent_value_type
                        if node is None
                        else node.value_type,
                        root_value_type=root_value_type,
                    )
                    for attribute_name, annotation in skeleton_type.__annotations__.items()
                }
                for _, extra_lines in class_name_and_lines_from_attribute_name.values():
                    lines.extend(extra_lines)
                extra_init_lines = [
                    f"self.{attribute_name}: Final = {class_name}(self)"
                    for attribute_name, (
                        class_name,
                        _,
                    ) in class_name_and_lines_from_attribute_name.items()
                ]
            else:
                extra_init_lines = []

    if name is not None:
        extra_init_lines.append(f'self.{_NAME_PROPERTY_NAME}: Final = r"""{name}"""')

    if node is not None and node.key_length is not None:
        extra_init_lines.append(
            f"""self.{_KEY_PROPERTY_NAME}: Final = {
                ", ".join(
                    [
                        f"self{''.join([f'.{_PARENT_PROPERTY_NAME}'] * (node.key_length - index - 1))}.{_NAME_PROPERTY_NAME}"
                        for index in range(node.key_length)
                    ]
                )
            }"""
        )

    return (
        class_name,
        [
            *lines,
            *[
                "@final",
                f"class {class_name}:",
                *(
                    _indent(line)
                    for line in [
                        f"def __init__(self, {_PARENT_PARAMETER_NAME}: {parent_type_name}, /) -> None:",
                        *(
                            _indent(line)
                            for line in [
                                *(
                                    []
                                    if node is None
                                    else [
                                        f"self.{_PARENT_PROPERTY_NAME}: Final = {_PARENT_PARAMETER_NAME}"
                                    ]
                                ),
                                *extra_init_lines,
                            ]
                        ),
                        *(
                            []
                            if node is None
                            else [
                                f"def __call__(self, {_attribute_name(root_value_type)}: {_atoti_class_name(root_value_type)}, /) -> {_atoti_class_name(node.value_type)}:",
                                _indent(
                                    f"return {_attribute_name(root_value_type)}{node.path_from_parent_value}[self.{_NAME_PROPERTY_NAME}]"
                                    if parent_value_type is root_value_type
                                    else f"return self.{_PARENT_PROPERTY_NAME}({_attribute_name(root_value_type)}){node.path_from_parent_value}[self.{_NAME_PROPERTY_NAME}]"
                                ),
                            ]
                        ),
                    ]
                ),
            ],
        ],
    )


def generate(skeleton: _T, skeleton_type: type[_T], /) -> str:
    skeleton_type, node = _unwrap_type(skeleton_type)
    assert node is not None
    assert node.key_length is None
    assert node.path_from_parent_value == ""

    skeleton = TypeAdapter(skeleton_type).validate_python(skeleton)

    import_lines = [
        "from __future__ import annotations",
        "from typing import Final, final",
        f"import atoti as {_ATOTI_IMPORT_ALIAS}",
    ]

    skeleton_class_name = _generate_unique_class_name()

    match skeleton_type:
        case typed_dict_type if is_typeddict(skeleton_type):
            class_name_and_lines_from_attribute_name = {
                attribute_name: _generate_class_name_and_lines(
                    skeleton[attribute_name],
                    annotation,
                    name=None,
                    parent_type_name=skeleton_class_name,
                    parent_value_type=node.value_type,
                    root_value_type=node.value_type,
                )
                for attribute_name, annotation in typed_dict_type.__annotations__.items()
            }
            extra_lines = []
            for _, lines in class_name_and_lines_from_attribute_name.values():
                extra_lines.extend(lines)
            extra_init_lines = [
                f"self.{attribute_name}: Final = {class_name}(self)"
                for attribute_name, (
                    class_name,
                    _,
                ) in class_name_and_lines_from_attribute_name.items()
            ]
        case _:
            extra_lines = []
            extra_init_lines = []

    skeleton_class_lines = [
        "@final",
        f"class {skeleton_class_name}:",
        *(
            _indent(line)
            for line in [
                *dedent(
                    '''\
                    """The skeleton of the application.

                    It mirrors the structure of the data model but only declares the parent/child relationship between nodes.

                    Note:
                        Attaching other information to the skeleton is discouraged because this will end up duplicating the data model API already provided by Atoti.
                        For instance, it is discouraged to add a ``data_type`` attribute to ``Column``, or a ``keys`` attribute to ``Table``.

                    Skeletons scale well to large data models because IDEs can inspect them statically and thus offer:

                    * Autocompletion
                    * "Find all references"
                    * "Go to definition"
                    * Type checking
                    """
                    '''
                ).splitlines(),
                "def __init__(self) -> None:",
                *(_indent(line) for line in extra_init_lines),
            ]
        ),
    ]

    lines = [
        "# Generated skeleton, do not edit.",
        *import_lines,
        *extra_lines,
        *skeleton_class_lines,
        f"{SKELETON_CONSTANT_NAME} = {skeleton_class_name}()",
    ]
    assert not any(linesep in line for line in lines)
    return linesep.join(lines)
