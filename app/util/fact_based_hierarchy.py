from collections.abc import Callable
from typing import Protocol, TypeVar

import atoti as tt


class _GetColumn(Protocol):
    def __call__(self, session: tt.Session, /) -> tt.Column: ...


class _Level(Protocol):
    @property
    def name(self) -> str: ...


class _Hierarchy(Protocol):
    @property
    def key(self) -> tuple[str, str]: ...

    def __getattribute__(self, name: str, /) -> _Level: ...


_T = TypeVar("_T", bound=_Hierarchy)


def fact_based_hierarchy(
    session: tt.Session,
    hierarchy: _T,
    get_mapping: Callable[[_T], dict[_Level, _GetColumn]],
    /,
) -> tuple[tuple[str, str], dict[str, tt.Column]]:
    return hierarchy.key, {
        level.name: get_column(session)
        for level, get_column in get_mapping(hierarchy).items()
    }
