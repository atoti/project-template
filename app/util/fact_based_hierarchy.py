from collections.abc import Callable
from typing import Protocol, TypeVar

import atoti as tt

from .column import _ColumnSkeleton, column


class _LevelSkeleton(Protocol):
    @property
    def name(self) -> str: ...


class _HierarchySkeleton(Protocol):
    @property
    def key(self) -> tuple[str, str]: ...


_Hierarchy = TypeVar("_Hierarchy", bound=_HierarchySkeleton)


def fact_based_hierarchy(
    session: tt.Session,
    hierarchy: _Hierarchy,
    get_mapping: Callable[[_Hierarchy], dict[_LevelSkeleton, _ColumnSkeleton]],
    /,
) -> tuple[tuple[str, str], dict[str, tt.Column]]:
    return hierarchy.key, {
        level_skeleton.name: column(session, column_skeleton)
        for level_skeleton, column_skeleton in get_mapping(hierarchy).items()
    }
