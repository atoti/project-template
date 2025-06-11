from dataclasses import KW_ONLY
from typing import Annotated

from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    _: KW_ONLY
    key_length: Annotated[int | None, Field(ge=2)] = None
