from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Tool:
    """Represents a tool that can be borrowed."""

    id: int
    name: str
    category: str
    stock: int


@dataclass(frozen=True)
class Member:
    """Represents a member who can borrow tools."""

    id: int
    name: str


@dataclass(frozen=True)
class Loan:
    """Represents a loan of a tool to a member."""

    id: int
    member_id: int
    tool_id: int
    active: bool

