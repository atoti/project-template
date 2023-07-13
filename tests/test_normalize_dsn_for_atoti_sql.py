from __future__ import annotations

import pytest
from pydantic import PostgresDsn, TypeAdapter

from app.util import normalize_postgres_dsn_for_atoti_sql


@pytest.mark.parametrize(
    ("value", "expected_output"),
    [
        (
            "postgres://foo:bar@example.com",
            "postgresql://example.com?user=foo&password=bar",
        ),
        (
            "postgres://foo:bar@example.com/db",
            "postgresql://example.com/db?user=foo&password=bar",
        ),
        (
            "postgres://foo:bar@example.com:5432/db?test=baz",
            "postgresql://example.com:5432/db?test=baz&user=foo&password=bar",
        ),
        (
            "postgres://foo:bar@example.com:5432/db?test1=baz&test2=foo#search",
            "postgresql://example.com:5432/db?test1=baz&test2=foo&user=foo&password=bar#search",
        ),
    ],
)
def test_normalize_dsn_for_atoti_sql(value: str, expected_output: str) -> None:
    validated_value: PostgresDsn = TypeAdapter(PostgresDsn).validate_python(value)
    output = str(normalize_postgres_dsn_for_atoti_sql(validated_value))
    assert output == expected_output
