"""
Contains the bulk of top-level execution code.
However execution occurs in `__main__.py`
"""

from importlib import metadata
from typing import Optional

import typer
from rich import print as rprint
from rich.prompt import Prompt

app = typer.Typer(
    help="--Pre-Release--\nPagerDuty Public Support Scripts CLI Tool\n--Pre-Release--",
    add_completion=False,
)

__version__ = metadata.version(__package__)


def version_callback(version: bool = typer.Option(None, "--version")):
    """Callback that returns app version"""
    if version:
        print(f"Awesome CLI Version: {__version__}")
        raise typer.Exit()


@app.callback()
def app_callback(
    _: bool = typer.Option(None, "--version", callback=version_callback),
):
    """..."""


@app.command(help="""Share your name -- get a fun fact.""")
def what_am_i(name: Optional[str] = typer.Argument(None)) -> None:
    """
    Says "hello" to an input name.\n
    Uses a callback to ensure only "Camila" is allowed.
    """
    if name is None:
        name_out: str = Prompt.ask("Enter your name, plz :sunglasses:")
    else:
        name_out: str = name

    rprint(f"\nWhat, {name_out}, are you?")
    # example of using rich-print's MarkUp
    rprint(
        f"[green]Why you are [bold red]loved[/bold red][/green] \
[blue]{name_out}[/blue][green]![/green] :heart:"
    )


@app.command()
def pword(
    name: str = "user",
    _: str = typer.Option(
        ...,
        "--hidden-input-string",
        prompt=True,
        confirmation_prompt=True,
        hide_input=True,
    ),
    # NOTE: we would NOT want this as it allows explicit flag calling and regular
    #       code inputing
):
    """Example use of \"hide_input\" true."""

    rprint(
        f"Hello [blue]{name}[/blue]. Doing something very secure :lock: with password."
    )

    #######################


@app.command(rich_help_panel="Yet To Be Implemented")
def adding_tags() -> None:
    """Example of using rich's prompt to add tags to a ticket"""
    tags = []
    while True:
        tag = Prompt.ask("Enter a tag, or [bold red]q[/bold red] to quit")
        if tag == "q":
            break
        tags.append(tag)
    rprint(f"Tags: {tags}")


@app.command(rich_help_panel="Yet To Be Implemented")
def enable_all_extensions() -> None:
    """Enable all extensions"""
    rprint("[bold red]Not Implemented[/bold red]")


@app.command(rich_help_panel="Yet To Be Implemented")
def get_info_on_all_users() -> None:
    """Get info on users"""
    rprint("[bold red]Not Implemented[/bold red]")


@app.command(rich_help_panel="Yet To Be Implemented")
def import_users() -> None:
    """Bulk import users"""
    rprint("[bold red]Not Implemented[/bold red]")


@app.command(rich_help_panel="Yet To Be Implemented")
def maintenance_windows_bulk() -> None:
    """Maintenance windows bulk operations"""
    rprint("[bold red]Not Implemented[/bold red]")


@app.command(rich_help_panel="Yet To Be Implemented")
def mass_update_incidents() -> None:
    """Mass update incidents"""
    rprint("[bold red]Not Implemented[/bold red]")


@app.command("...", rich_help_panel="Yet To Be Implemented")
def dotdotdot() -> None:
    """etc..."""
    rprint("[bold red]Not Implemented[/bold red]")
