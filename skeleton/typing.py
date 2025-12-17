from collections.abc import Set as AbstractSet
from typing import Annotated, TypeAlias

from typing_extensions import TypedDict

from .node import Node

_ColumnSkeleton: TypeAlias = Annotated[str, Node(key_length=2)]
_TableSkeleton: TypeAlias = Annotated[AbstractSet[_ColumnSkeleton], Node()]
_TablesSkeleton: TypeAlias = dict[str, _TableSkeleton]

_LevelSkeleton: TypeAlias = Annotated[str, Node(key_length=3)]
_HierarchySkeleton: TypeAlias = Annotated[
    AbstractSet[_LevelSkeleton], Node(key_length=2)
]
_DimensionSkeleton: TypeAlias = dict[str, _HierarchySkeleton]
_DimensionsSkeleton: TypeAlias = dict[str, _DimensionSkeleton]

_MeasureSkeleton: TypeAlias = Annotated[str, Node()]
_MeasuresSkeleton: TypeAlias = AbstractSet[_MeasureSkeleton]


class __CubeSkeleton(TypedDict):
    dimensions: _DimensionsSkeleton
    measures: _MeasuresSkeleton


_CubeSkeleton: TypeAlias = Annotated[__CubeSkeleton, Node()]

_CubesSkeleton: TypeAlias = dict[str, _CubeSkeleton]


class Skeleton(TypedDict):
    tables: _TablesSkeleton
    cubes: _CubesSkeleton
