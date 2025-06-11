from collections.abc import Mapping, Set as AbstractSet
from typing import Annotated, TypeAlias

from typing_extensions import TypedDict

from .node import Node

_ColumnSkeleton: TypeAlias = Annotated[str, Node(key_length=2)]
_TableSkeleton: TypeAlias = Annotated[AbstractSet[_ColumnSkeleton], Node()]
_TablesSkeleton: TypeAlias = Mapping[str, _TableSkeleton]

_LevelSkeleton: TypeAlias = Annotated[str, Node(key_length=3)]
_HierarchySkeleton: TypeAlias = Annotated[
    AbstractSet[_LevelSkeleton], Node(key_length=2)
]
_DimensionSkeleton: TypeAlias = Mapping[str, _HierarchySkeleton]
_DimensionsSkeleton: TypeAlias = Mapping[str, _DimensionSkeleton]

_MeasureSkeleton: TypeAlias = Annotated[str, Node()]
_MeasuresSkeleton: TypeAlias = AbstractSet[_MeasureSkeleton]


class __CubeSkeleton(TypedDict):
    dimensions: _DimensionsSkeleton
    measures: _MeasuresSkeleton


_CubeSkeleton: TypeAlias = Annotated[__CubeSkeleton, Node()]

_CubesSkeleton: TypeAlias = Mapping[str, _CubeSkeleton]


class Skeleton(TypedDict):
    tables: _TablesSkeleton
    cubes: _CubesSkeleton


SKELETON: Skeleton = {
    "tables": {
        "Station details": {
            "ID",
            "Name",
            "Department",
            "City",
            "Postcode",
            "Street",
            "House number",
            "Capacity",
        },
        "Station status": {"Station ID", "Bike type", "Bikes"},
    },
    "cubes": {
        "Station": {
            "dimensions": {
                "Station details": {
                    "Location": {
                        "Department",
                        "City",
                        "Postcode",
                        "Street",
                        "House number",
                    },
                    "Station": {"Name", "ID"},
                },
                "Station status": {"Bike type": {"Bike type"}},
            },
            "measures": {"Bikes", "Capacity", "contributors.COUNT"},
        }
    },
}
