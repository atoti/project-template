from collections.abc import Mapping, Sequence, Set as AbstractSet
from typing import Annotated, TypeAlias

import atoti as tt
from typing_extensions import TypedDict

from .node import Node

_ColumnSkeleton: TypeAlias = Annotated[str, Node(tt.Column)]
_TableSkeleton: TypeAlias = Annotated[
    AbstractSet[_ColumnSkeleton],
    Node(tt.Table, path_from_parent_value=".tables"),
]
_TablesSkeleton: TypeAlias = Mapping[str, _TableSkeleton]

_LevelSkeleton: TypeAlias = Annotated[str, Node(tt.Level, key_length=3)]
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


class _Skeleton(TypedDict):
    tables: _TablesSkeleton
    cubes: _CubesSkeleton


Skeleton: TypeAlias = Annotated[_Skeleton, Node(tt.Session)]


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
                    "Location": [
                        "Department",
                        "City",
                        "Postcode",
                        "Street",
                        "House number",
                    ],
                    "Station": ["Name", "ID"],
                },
                "Station status": {"Bike type": ["Bike type"]},
            },
            "measures": {"Bikes", "Capacity", "contributors.COUNT"},
        }
    },
}
