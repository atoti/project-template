from typing import Protocol

import atoti as tt


class _ColumnSkeleton(Protocol):
    @property
    def key(self) -> tuple[str, str]: ...


def column(
    session: tt.Session,
    column: _ColumnSkeleton,
    /,
) -> tt.Column:
    table_name, column_name = column.key
    return session.tables[table_name][column_name]
