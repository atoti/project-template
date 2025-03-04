"""Module containing the node classes required to build a skeleton.

The code is dense and makes heavy use of reflection but expected invariants are enforced by many assertions.

This module does not need to be modified to add new nodes to the skeleton.
"""

from abc import ABC
from typing import (
    ClassVar,
    Final,
    Generic,
    TypeVar,
    cast,
    final,
    get_args,
    get_origin,
)

from typing_extensions import TypeVarTuple, Unpack, get_original_bases, override


def _camel_from_pascal(name: str, /) -> str:
    match len(name):
        case 0:
            return ""
        case 1:
            return name.lower()
        case _:
            return f"{name[0].lower()}{name[1:]}"


def _is_private(name: str, /) -> bool:
    return name.startswith("_")


_KeyT_co = TypeVar("_KeyT_co", bound=str | tuple[str, ...], covariant=True)

_ChildT = TypeVar("_ChildT")
_HeterogeneousChildT = TypeVarTuple("_HeterogeneousChildT")

_LEAF_NODE_CLASS_NAME = "LeafNode"


class HeterogeneousNode(Generic[_KeyT_co, Unpack[_HeterogeneousChildT]], ABC):
    _child_types: tuple[Unpack[_HeterogeneousChildT]]
    _key_length: ClassVar[int]
    _path: tuple[str, ...] | None = None
    name: str

    @override
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        # Cannot directly reference `LeafNode` at this time.
        if cls.__name__ == _LEAF_NODE_CLASS_NAME:
            return

        (orig_base,) = cls.__orig_bases__  # type: ignore[attr-defined]
        key_type, *child_types = get_args(orig_base)

        if get_origin(orig_base).__name__ == _LEAF_NODE_CLASS_NAME:
            assert not child_types, (
                f"Expected leaf {cls.__name__} to not have children but got {child_types}."
            )
            cls._child_types = ()
        else:
            assert child_types, (
                f"Expected non-leaf {cls.__name__} to have children but got none."
            )
            cls._child_types = tuple(child_types)

            if HeterogeneousNode not in cls.__bases__:
                for child_type in cls._child_types:
                    child = cls._child(child_type)
                    assert isinstance(child, HomogeneousNode | None), (
                        f"Expected {cls.__name__}'s {child_type.__name__} to be an {HomogeneousNode.__name__} but got {type(child).__name__}."
                    )

        attribute_names = {
            name
            for name in dir(cls)
            if not _is_private(name) and name not in {"key", "name"}
        }
        if (
            _LEAF_NODE_CLASS_NAME in {base.__name__ for base in cls.__bases__}
        ) or HeterogeneousNode in cls.__bases__:
            assert not attribute_names, (
                f"Expected {cls.__name__} to have no attributes but got {attribute_names}."
            )
        else:
            unexpected_attribute_names = attribute_names - {
                _camel_from_pascal(child_type.__name__)
                for child_type in cls._child_types
            }
            assert not unexpected_attribute_names, (
                f"{cls.__name__} has some unexpected attributes: {attribute_names}."
            )

        if key_type is str:
            cls._key_length = 1
        else:
            assert get_origin(key_type) is tuple
            key_length = len(get_args(key_type))
            degenerated_tuple_length = 1
            assert key_length == 0 or key_length > degenerated_tuple_length, (
                "Use `str` instead of `tuple[str]`."
            )
            cls._key_length = key_length

    @final
    @classmethod
    def _child(cls, child_type: type[_ChildT], /) -> _ChildT | None:
        attribute_name = _camel_from_pascal(child_type.__name__)
        child = getattr(cls, attribute_name, None)
        assert isinstance(child, child_type | None), (
            f"Expected {cls.__name__}.{attribute_name} to be a {child_type.__name__} but got {type(child).__name__}."
        )
        return child

    @final
    @property
    def key(self) -> _KeyT_co:
        assert self._path is not None, (
            f"The `_path` of the {type(self).__name__} named `{self.name}` should have been set by now."
        )
        match self._key_length:
            case 0:
                return cast(_KeyT_co, ())
            case 1:
                return cast(_KeyT_co, self._path[-1])
            case key_length:
                return cast(_KeyT_co, self._path[-key_length:])

    @final
    def _set_path(self, *, parent_path: tuple[str, ...]) -> None:
        self_part = () if self.name is None else (self.name,)
        self._path = (*parent_path, *self_part)
        for child_type in self._child_types:
            assert isinstance(child_type, type)
            assert issubclass(child_type, HomogeneousNode)
            child = self._child(child_type)
            if child is not None:
                child._set_path(parent_path=self._path)  # noqa: SLF001


class LeafNode(HeterogeneousNode[_KeyT_co]):
    def __init__(self, name: str, /) -> None:
        super().__init__()
        self.name: Final = name


assert LeafNode.__name__ == _LEAF_NODE_CLASS_NAME

_HomogenousChildT = TypeVar("_HomogenousChildT")


class HomogeneousNode(Generic[_HomogenousChildT], ABC):
    _child_type: type[_HomogenousChildT]

    @override
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if HomogeneousNode not in cls.__bases__:
            return

        (original_base,) = get_original_bases(cls)
        assert get_origin(original_base) is HomogeneousNode
        (child_type,) = get_args(original_base)
        assert issubclass(child_type, HeterogeneousNode)
        cls._child_type = child_type

    @final
    @classmethod
    def _children(cls) -> dict[str, _HomogenousChildT]:
        children: dict[str, _HomogenousChildT] = {}
        for name, value in vars(cls).items():
            if _is_private(name):
                continue
            assert isinstance(value, cls._child_type), (
                f"Expected {cls.__name__}.{name} to be a {cls._child_type.__name__} but got {type(value).__name__}."
            )
            children[name] = value
        return children

    @final
    def _set_path(self, *, parent_path: tuple[str, ...]) -> None:
        for value in self._children().values():
            assert isinstance(value, HeterogeneousNode), (
                f"Expected {type(value).__name__} to be an {HeterogeneousNode.__name__}."
            )
            value._set_path(parent_path=parent_path)  # noqa: SLF001
