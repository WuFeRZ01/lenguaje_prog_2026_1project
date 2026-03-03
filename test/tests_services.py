import pytest

from src.tool_lending.exceptions import (
    DuplicateLoanError,
    NotFoundError,
    OutOfStockError,
    ValidationError,
)
from src.tool_lending.services import (
    create_loan,
    create_member,
    create_tool,
    delete_tool,
    list_loans,
    list_members,
    list_tools,
    return_loan,
    update_tool,
)


def test_create_tool_ok():
    t = create_tool("Taladro", "Electricas", 2)
    assert t.id == 1
    assert t.stock == 2


def test_create_tool_empty_name_error():
    with pytest.raises(ValidationError):
        create_tool("", "Cat", 1)


def test_create_tool_negative_stock_error():
    with pytest.raises(ValidationError):
        create_tool("Martillo", "Manual", -1)


def test_list_tools_returns_items():
    create_tool("Sierra", "Manual", 1)
    tools = list_tools()
    assert len(tools) == 1
    assert tools[0].name == "Sierra"


def test_update_tool_changes_stock():
    t = create_tool("Pulidora", "Electricas", 3)
    t2 = update_tool(t.id, stock=1)
    assert t2.stock == 1


def test_delete_tool_not_found():
    with pytest.raises(NotFoundError):
        delete_tool(999)


def test_create_member_ok():
    m = create_member("Samu")
    assert m.id == 1
    assert m.name == "Samu"


def test_create_member_empty_name_error():
    with pytest.raises(ValidationError):
        create_member("   ")


def test_loan_member_not_found():
    t = create_tool("Llave", "Manual", 1)
    with pytest.raises(NotFoundError):
        create_loan(member_id=999, tool_id=t.id)


def test_loan_tool_not_found():
    m = create_member("Ana")
    with pytest.raises(NotFoundError):
        create_loan(member_id=m.id, tool_id=999)


def test_loan_out_of_stock():
    m = create_member("Ana")
    t = create_tool("Taladro", "Electricas", 0)
    with pytest.raises(OutOfStockError):
        create_loan(member_id=m.id, tool_id=t.id)


def test_loan_ok_decreases_stock_and_creates_active_loan():
    m = create_member("Ana")
    t = create_tool("Taladro", "Electricas", 1)

    loan = create_loan(member_id=m.id, tool_id=t.id)
    assert loan.active is True

    tools = list_tools()
    assert tools[0].stock == 0

    loans = list_loans(active_only=True)
    assert len(loans) == 1


def test_duplicate_active_loan_error():
    m = create_member("Ana")
    t = create_tool("Taladro", "Electricas", 2)

    create_loan(member_id=m.id, tool_id=t.id)
    with pytest.raises(DuplicateLoanError):
        create_loan(member_id=m.id, tool_id=t.id)


def test_return_loan_ok_increases_stock_and_deactivates():
    m = create_member("Ana")
    t = create_tool("Taladro", "Electricas", 1)
    loan = create_loan(member_id=m.id, tool_id=t.id)

    returned = return_loan(loan.id)
    assert returned.active is False

    tools = list_tools()
    assert tools[0].stock == 1


def test_return_loan_not_found():
    with pytest.raises(NotFoundError):
        return_loan(999)


def test_return_loan_already_inactive_error():
    m = create_member("Ana")
    t = create_tool("Taladro", "Electricas", 1)
    loan = create_loan(member_id=m.id, tool_id=t.id)
    return_loan(loan.id)
    with pytest.raises(ValidationError):
        return_loan(loan.id)