import atoti as tt

from .column import column
from .skeleton import Column, Hierarchy, Level, Levels


def _column(level: Level, /) -> Column:
    column = level._column  # noqa: SLF001
    assert column is not None, (
        f"Cannot use `{fact_based_hierarchy.__name__}()` with a hierarchy with level `{level.name}` not based on a column."
    )
    return column


def fact_based_hierarchy(
    session: tt.Session, hierarchy: Hierarchy, /
) -> tuple[tuple[str, str], dict[str, tt.Column]]:
    """Return the definition of a hierarchy for which all levels are based on columns."""
    levels = hierarchy._child(Levels)  # noqa: SLF001
    assert levels is not None
    return hierarchy.key, {
        level.name: column(session, _column(level))
        for level in levels._children().values()  # noqa: SLF001
    }
