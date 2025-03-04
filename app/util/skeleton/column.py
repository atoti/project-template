import atoti as tt

from .skeleton import Column as Column


def column(session: tt.Session, column: Column, /) -> tt.Column:
    """Atoti has :attr:`atoti.Cube.levels` but no `Tables.columns`, this is the next-best thing."""
    table_name, column_name = column.key
    return session.tables[table_name][column_name]
