from typing import Final, final

from typing_extensions import override

from ._node import HeterogeneousNode, HomogeneousNode, LeafNode


@final
class Column(LeafNode[tuple[str, str]]): ...


class Columns(HomogeneousNode[Column]): ...


class Table(HeterogeneousNode[str, Columns]): ...


class Tables(HomogeneousNode[Table]): ...


@final
class Level(LeafNode[tuple[str, str, str]]):
    _column: Column | None = None

    def __init__(self, column_or_name: Column | str, /) -> None:
        match column_or_name:
            case Column() as column:
                super().__init__("__pending__")
                self._column = column
            case str() as name:
                super().__init__(name)

    @override  # type: ignore[misc]
    def _set_path(self, *, parent_path: tuple[str, ...]) -> None:
        if self._column is not None:
            assert self._column.key is not None, (
                "The column key should have been set by now."
            )
            self.name = self._column.name  # type: ignore[misc]

        super()._set_path(parent_path=parent_path)


class Levels(HomogeneousNode[Level]): ...


class Hierarchy(HeterogeneousNode[tuple[str, str], Levels]): ...


class Hierarchies(HomogeneousNode[Hierarchy]): ...


class Dimension(HeterogeneousNode[str, Hierarchies]): ...


class Dimensions(HomogeneousNode[Dimension]): ...


@final
class Measure(LeafNode[str]): ...


class Measures(HomogeneousNode[Measure]): ...


class Cube(HeterogeneousNode[str, Dimensions, Measures]): ...


class Cubes(HomogeneousNode[Cube]): ...


class Skeleton(
    HeterogeneousNode[
        tuple[()],
        # Before `Cubes` so that a `Level` referencing a `Column` can access the column's `_path`.
        Tables,
        Cubes,
    ]
):
    """The skeleton of a data model.

    It mirrors the structure of the data model but only declares the parent/child relationship between nodes and the name of each node.

    Note:
        Attaching other information to the skeleton is discouraged because this will end up duplicating the data model API already provided by Atoti.
        For instance, it is discouraged to add a ``data_type`` attribute to ``Column``, or a ``keys`` attribute to ``Table``.

    Skeletons scale well to large data models because IDEs can inspect them statically and thus offer:

    * Autocompletion
    * "Find all references"
    * "Go to definition"
    * Type checking
    * Dead code detection

    When instantiated, the skeleton will propagate the path from the root (i.e. this class) to all the nodes, providing easy access to unambiguous keys:

    >>> class _MyCubeFooDimensionBarHierarchyLevels(Levels):
    ...     BAZ = Level("baz")
    >>> class _MyCubeFooDimensionBarHierarchy(Hierarchy):
    ...     name = "bar"
    ...     levels = _MyCubeFooDimensionBarHierarchyLevels()
    >>> class _MyCubeFooDimensionHierarchies(Hierarchies):
    ...     BAR = _MyCubeFooDimensionBarHierarchy()
    >>> class _MyCubeFooDimension(Dimension):
    ...     name = "foo"
    ...     hierarchies = _MyCubeFooDimensionHierarchies()
    >>> class _MyCubeDimensions(Dimensions):
    ...     FOO = _MyCubeFooDimension()
    >>> class _MyCube(Cube):
    ...     name = "my cube"
    ...     dimensions = _MyCubeDimensions()
    >>> class _Cubes(Cubes):
    ...     MY_CUBE = _MyCube()
    >>> class _Skeleton(Skeleton):
    ...     cubes = _Cubes()
    >>> SKELETON = _Skeleton()
    >>> SKELETON.cubes.MY_CUBE.dimensions.FOO.key
    'foo'
    >>> SKELETON.cubes.MY_CUBE.dimensions.FOO.hierarchies.BAR.key
    ('foo', 'bar')
    >>> SKELETON.cubes.MY_CUBE.dimensions.FOO.hierarchies.BAR.levels.BAZ.key
    ('foo', 'bar', 'baz')

    This works well with :func:`atoti.mapping_lookup` when ``check=False`` since that mode requires unambiguous keys.

    """

    name: Final = "__root__"

    def __init__(self) -> None:
        self._set_path(parent_path=())
