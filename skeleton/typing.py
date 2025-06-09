from collections.abc import Mapping, Sequence, Set as AbstractSet
from typing import TypeAlias

from typing_extensions import TypedDict

Table: TypeAlias = AbstractSet[str]
Tables: TypeAlias = Mapping[str, Table]

Hierarchy: TypeAlias = Sequence[str]
Dimension: TypeAlias = Mapping[str, Hierarchy]
Dimensions: TypeAlias = Mapping[str, Dimension]

Measures: TypeAlias = AbstractSet[str]


class Cube(TypedDict):
    dimensions: Dimensions
    measures: Measures


Cubes: TypeAlias = Mapping[str, Cube]


class Skeleton(TypedDict):
    tables: Tables
    cubes: Cubes
