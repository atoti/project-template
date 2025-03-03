from collections.abc import Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from ._node import HeterogeneousNode, HomogeneousNode, LeafNode


@final
class Column(LeafNode[tuple[str, str]]): ...


class Columns(HomogeneousNode):
    @final
    @override
    @classmethod
    def _child(cls) -> type:
        return Column


class Cube(HeterogeneousNode[str]):
    @final
    @override
    @classmethod
    def _children(cls) -> AbstractSet[type]:
        return {Dimensions, Measures}


class Cubes(HomogeneousNode):
    @final
    @override
    @classmethod
    def _child(cls) -> type:
        return Cube


class Dimension(HeterogeneousNode[str]):
    @final
    @override
    @classmethod
    def _children(cls) -> AbstractSet[type]:
        return {Hierarchies}


class Dimensions(HomogeneousNode):
    @final
    @override
    @classmethod
    def _child(cls) -> type:
        return Dimension


class Hierarchy(HeterogeneousNode[tuple[str, str]]):
    @final
    @override
    @classmethod
    def _children(cls) -> AbstractSet[type]:
        return {Levels}


class Hierarchies(HomogeneousNode):
    @final
    @override
    @classmethod
    def _child(cls) -> type:
        return Hierarchy


@final
class Level(LeafNode[tuple[str, str, str]]): ...


class Levels(HomogeneousNode):
    @final
    @override
    @classmethod
    def _child(cls) -> type:
        return Level


@final
class Measure(LeafNode[str]): ...


class Measures(HomogeneousNode):
    @final
    @override
    @classmethod
    def _child(cls) -> type:
        return Measure


class Skeleton(HeterogeneousNode[str]):
    name: Final = None

    def __init__(self) -> None:
        self._set_path(parent_path=())

    @final
    @override
    @classmethod
    def _children(cls) -> AbstractSet[type]:
        return {Cubes, Tables}


class Table(HeterogeneousNode[str]):
    @final
    @override
    @classmethod
    def _children(cls) -> AbstractSet[type]:
        return {Columns}


class Tables(HomogeneousNode):
    @final
    @override
    @classmethod
    def _child(cls) -> type:
        return Table
