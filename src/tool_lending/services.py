from __future__ import annotations

from typing import Any

from .exceptions import (
    DuplicateLoanError,
    NotFoundError,
    OutOfStockError,
    ValidationError,
)
from .models import Loan, Member, Tool
from .storage import load_db, save_db


def _next_id(records: list[dict[str, Any]]) -> int:
    """Compute next integer ID for a list of dict records."""
    if not records:
        return 1
    return max(r["id"] for r in records) + 1


# -----------------------
# Tools CRUD
# -----------------------
def create_tool(name: str, category: str, stock: int) -> Tool:
    """Create a tool.

    Raises:
        ValidationError: if inputs are invalid.
    """
    if not name.strip():
        raise ValidationError("Tool name cannot be empty.")
    if not category.strip():
        raise ValidationError("Tool category cannot be empty.")
    if stock < 0:
        raise ValidationError("Tool stock cannot be negative.")

    db = load_db()
    tool_id = _next_id(db["tools"])
    record = {"id": tool_id, "name": name.strip(), "category": category.strip(), "stock": stock}
    db["tools"].append(record)
    save_db(db)
    return Tool(**record)


def list_tools() -> list[Tool]:
    """Return all tools."""
    db = load_db()
    return [Tool(**t) for t in db["tools"]]


def get_tool(tool_id: int) -> Tool:
    """Get a tool by ID."""
    db = load_db()
    found = next((t for t in db["tools"] if t["id"] == tool_id), None)
    if found is None:
        raise NotFoundError("Tool not found.")
    return Tool(**found)


def update_tool(tool_id: int, *, name: str | None = None, category: str | None = None, stock: int | None = None) -> Tool:
    """Update tool fields."""
    db = load_db()
    tool = next((t for t in db["tools"] if t["id"] == tool_id), None)
    if tool is None:
        raise NotFoundError("Tool not found.")

    if name is not None:
        if not name.strip():
            raise ValidationError("Tool name cannot be empty.")
        tool["name"] = name.strip()

    if category is not None:
        if not category.strip():
            raise ValidationError("Tool category cannot be empty.")
        tool["category"] = category.strip()

    if stock is not None:
        if stock < 0:
            raise ValidationError("Tool stock cannot be negative.")
        tool["stock"] = stock

    save_db(db)
    return Tool(**tool)


def delete_tool(tool_id: int) -> None:
    """Delete a tool by ID.

    Note: For simplicity, we allow deleting even if loans exist (rule not specified).
    """
    db = load_db()
    before = len(db["tools"])
    db["tools"] = [t for t in db["tools"] if t["id"] != tool_id]
    if len(db["tools"]) == before:
        raise NotFoundError("Tool not found.")
    save_db(db)


# -----------------------
# Members CRUD
# -----------------------
def create_member(name: str) -> Member:
    """Create a member."""
    if not name.strip():
        raise ValidationError("Member name cannot be empty.")

    db = load_db()
    member_id = _next_id(db["members"])
    record = {"id": member_id, "name": name.strip()}
    db["members"].append(record)
    save_db(db)
    return Member(**record)


def list_members() -> list[Member]:
    """Return all members."""
    db = load_db()
    return [Member(**m) for m in db["members"]]


def get_member(member_id: int) -> Member:
    """Get member by ID."""
    db = load_db()
    found = next((m for m in db["members"] if m["id"] == member_id), None)
    if found is None:
        raise NotFoundError("Member not found.")
    return Member(**found)


# -----------------------
# Loans (business rules)
# -----------------------
def create_loan(member_id: int, tool_id: int) -> Loan:
    """Create a loan if rules allow it.

    Rules:
    - Member must exist
    - Tool must exist
    - Tool stock must be > 0
    - Member cannot have an active loan for same tool
    """
    db = load_db()

    member = next((m for m in db["members"] if m["id"] == member_id), None)
    if member is None:
        raise NotFoundError("Member not found.")

    tool = next((t for t in db["tools"] if t["id"] == tool_id), None)
    if tool is None:
        raise NotFoundError("Tool not found.")

    if tool["stock"] <= 0:
        raise OutOfStockError("Tool out of stock.")

    duplicate = next(
        (l for l in db["loans"] if l["member_id"] == member_id and l["tool_id"] == tool_id and l["active"] is True),
        None,
    )
    if duplicate is not None:
        raise DuplicateLoanError("Member already has an active loan for this tool.")

    tool["stock"] -= 1

    loan_id = _next_id(db["loans"])
    record = {"id": loan_id, "member_id": member_id, "tool_id": tool_id, "active": True}
    db["loans"].append(record)
    save_db(db)
    return Loan(**record)


def list_loans(active_only: bool = False) -> list[Loan]:
    """List loans, optionally only active loans."""
    db = load_db()
    loans = db["loans"]
    if active_only:
        loans = [l for l in loans if l["active"] is True]
    return [Loan(**l) for l in loans]


def return_loan(loan_id: int) -> Loan:
    """Return (close) a loan.

    Rules:
    - Loan must exist
    - Loan must be active
    - Stock is increased back
    """
    db = load_db()

    loan = next((l for l in db["loans"] if l["id"] == loan_id), None)
    if loan is None:
        raise NotFoundError("Loan not found.")

    if loan["active"] is not True:
        raise ValidationError("Loan is already inactive.")

    tool = next((t for t in db["tools"] if t["id"] == loan["tool_id"]), None)
    if tool is None:
        # Should not happen if DB consistent, but handle anyway
        raise NotFoundError("Tool for this loan not found.")

    loan["active"] = False
    tool["stock"] += 1

    save_db(db)
    return Loan(**loan)