from collections.abc import Mapping, Sequence, Set as AbstractSet
from typing import Annotated, TypeAlias

import atoti as tt
from typing_extensions import TypedDict

from ._node import Node

_ColumnSkeleton: TypeAlias = Annotated[str, Node(tt.Column)]
_TableSkeleton: TypeAlias = Annotated[
    AbstractSet[_ColumnSkeleton],
    Node(tt.Table, path_from_parent_value=".tables"),
]
_TablesSkeleton: TypeAlias = Mapping[str, _TableSkeleton]

_LevelSkeleton: TypeAlias = Annotated[
    str, Node(tt.Level, key_length=3, path_from_parent_value=".levels")
]
_HierarchySkeleton: TypeAlias = Annotated[
    Sequence[_LevelSkeleton],
    Node(tt.Hierarchy, key_length=2, path_from_parent_value=".hierarchies"),
]
_DimensionSkeleton: TypeAlias = Mapping[str, _HierarchySkeleton]
_DimensionsSkeleton: TypeAlias = Mapping[str, _DimensionSkeleton]

_MeasureSkeleton: TypeAlias = Annotated[
    str, Node(tt.Measure, path_from_parent_value=".measures")
]
_MeasuresSkeleton: TypeAlias = AbstractSet[_MeasureSkeleton]


class __CubeSkeleton(TypedDict):
    dimensions: _DimensionsSkeleton
    measures: _MeasuresSkeleton


_CubeSkeleton: TypeAlias = Annotated[
    __CubeSkeleton, Node(tt.Cube, path_from_parent_value=".cubes")
]

_CubesSkeleton: TypeAlias = Mapping[str, _CubeSkeleton]


class _SessionSkeleton(TypedDict):
    tables: _TablesSkeleton
    cubes: _CubesSkeleton


SessionSkeleton: TypeAlias = Annotated[_SessionSkeleton, Node(tt.Session)]
