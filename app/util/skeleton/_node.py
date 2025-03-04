from abc import abstractmethod
from collections.abc import Set as AbstractSet
from inspect import getmembers
from typing import (
    ClassVar,
    Final,
    Generic,
    TypeVar,
    final,
    get_args,
    get_origin,
)

from typing_extensions import override


def _camel_from_pascal(name: str, /) -> str:
    return f"{name[0].lower()}{name[1:]}"


def _is_private(name: str, /) -> bool:
    return name.startswith("_")


_KeyT = TypeVar("_KeyT", bound=str | tuple[str, ...])


class HeterogeneousNode(Generic[_KeyT]):
    _key_length: ClassVar[int]
    _path: tuple[str, ...] | None = None

    @override
    def __init_subclass__(cls, *args: object, **kwargs: object) -> None:
        super().__init_subclass__(*args, **kwargs)

        if cls.__name__ == "LeafNode":
            return

        cls._key_length = cls._get_key_length()

    @classmethod
    @abstractmethod
    def _children(cls) -> AbstractSet[type]: ...

    @final
    @classmethod
    def _get_key_length(cls) -> int:
        orig_base, *_ = cls.__orig_bases__  # type: ignore[attr-defined]
        key_type, *_ = get_args(orig_base)
        if key_type is str:
            return 1
        assert get_origin(key_type) is tuple
        key_length = len(get_args(key_type))
        degenerated_tuple_length = 1
        assert key_length > degenerated_tuple_length, (
            "Use `str` instead of `tuple[str]`."
        )
        return key_length

    @final
    @property
    def key(self) -> _KeyT:
        assert self._path is not None
        match self._key_length:
            case 1:
                return self._path[-1]  # type: ignore[return-value]
            case key_length:
                return self._path[-key_length:]  # type: ignore[return-value]

    @final
    def _set_path(self, *, parent_path: tuple[str, ...]) -> None:
        self._path = (*parent_path, *(() if self.name is None else (self.name,)))  # type: ignore[attr-defined]

        child_from_attribute_name = {
            _camel_from_pascal(child.__name__): child for child in self._children()
        }
        attribute_names = {
            name
            for name in dir(type(self))
            if not _is_private(name) and name not in {"key", "name"}
        }
        assert attribute_names == set(child_from_attribute_name), (
            f"Expected `{type(self).__name__}` to have attributes {set(child_from_attribute_name)} but got {attribute_names}."
        )

        for attribute_name, child in child_from_attribute_name.items():
            value = getattr(self, attribute_name)
            assert isinstance(value, child)
            assert isinstance(value, HomogeneousNode)
            value._set_path(parent_path=self._path)  # noqa: SLF001


class LeafNode(HeterogeneousNode[_KeyT]):
    @final
    @override
    @classmethod
    def _children(cls) -> AbstractSet[type]:
        return set()

    @final
    def __init__(self, name: str, /) -> None:
        super().__init__()
        self.name: Final = name


class HomogeneousNode:
    @classmethod
    @abstractmethod
    def _child(cls) -> type: ...

    @final
    def _set_path(self, *, parent_path: tuple[str, ...]) -> None:
        for name, value in getmembers(type(self)):
            if _is_private(name):
                continue
            assert isinstance(value, self._child()), (
                f"Expected `{type(self).__name__}.{name}` to be a `{self._child().__name__}` but got `{type(value).__name__}`."
            )
            assert isinstance(value, HeterogeneousNode)
            value._set_path(parent_path=parent_path)  # noqa: SLF001
