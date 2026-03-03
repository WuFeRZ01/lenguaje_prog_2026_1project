from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from src.tool_lending.exceptions import AppError
from src.tool_lending.services import (
    create_loan,
    create_member,
    create_tool,
    list_loans,
    list_members,
    list_tools,
    return_loan,
)

app = typer.Typer(help="Tool Lending CLI - Manage tools, members and loans.")
console = Console()


def _print_tools() -> None:
    tools = list_tools()
    table = Table(title="Tools")
    table.add_column("ID", justify="right")
    table.add_column("Name")
    table.add_column("Category")
    table.add_column("Stock", justify="right")
    for t in tools:
        table.add_row(str(t.id), t.name, t.category, str(t.stock))
    console.print(table)


def _print_members() -> None:
    members = list_members()
    table = Table(title="Members")
    table.add_column("ID", justify="right")
    table.add_column("Name")
    for m in members:
        table.add_row(str(m.id), m.name)
    console.print(table)


def _print_loans(active_only: bool) -> None:
    loans = list_loans(active_only=active_only)
    table = Table(title="Loans" + (" (active only)" if active_only else ""))
    table.add_column("ID", justify="right")
    table.add_column("Member ID", justify="right")
    table.add_column("Tool ID", justify="right")
    table.add_column("Active")
    for l in loans:
        table.add_row(str(l.id), str(l.member_id), str(l.tool_id), str(l.active))
    console.print(table)


@app.command("add-tool")
def add_tool(name: str = typer.Option(...), category: str = typer.Option(...), stock: int = typer.Option(...)):
    """Create a new tool."""
    try:
        tool = create_tool(name=name, category=category, stock=stock)
        console.print(f"[bold green]Created tool[/] ID={tool.id}")
    except AppError as e:
        console.print(f"[bold red]Error:[/] {e}")


@app.command("list-tools")
def cmd_list_tools():
    """List tools."""
    try:
        _print_tools()
    except AppError as e:
        console.print(f"[bold red]Error:[/] {e}")


@app.command("add-member")
def add_member(name: str = typer.Option(...)):
    """Create a member."""
    try:
        member = create_member(name=name)
        console.print(f"[bold green]Created member[/] ID={member.id}")
    except AppError as e:
        console.print(f"[bold red]Error:[/] {e}")


@app.command("list-members")
def cmd_list_members():
    """List members."""
    try:
        _print_members()
    except AppError as e:
        console.print(f"[bold red]Error:[/] {e}")


@app.command("loan")
def cmd_loan(member_id: int = typer.Option(...), tool_id: int = typer.Option(...)):
    """Create a loan (borrow a tool)."""
    try:
        loan = create_loan(member_id=member_id, tool_id=tool_id)
        console.print(f"[bold green]Loan created[/] ID={loan.id}")
    except AppError as e:
        console.print(f"[bold red]Error:[/] {e}")


@app.command("return-loan")
def cmd_return_loan(loan_id: int = typer.Option(...)):
    """Return a loan (close it)."""
    try:
        loan = return_loan(loan_id=loan_id)
        console.print(f"[bold green]Loan returned[/] ID={loan.id}")
    except AppError as e:
        console.print(f"[bold red]Error:[/] {e}")


@app.command("list-loans")
def cmd_list_loans(active_only: bool = typer.Option(False, help="Show only active loans.")):
    """List loans."""
    try:
        _print_loans(active_only=active_only)
    except AppError as e:
        console.print(f"[bold red]Error:[/] {e}")


if __name__ == "__main__":
    app()