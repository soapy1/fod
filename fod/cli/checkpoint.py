import os
import typer

from rich.table import Table
import rich

from fod._fod.data_dir import DataDir


checkpoint_command = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
)


@checkpoint_command.command()
def list(
    ctx: typer.Context,
    path: str = typer.Option(
        help="prefix to list checkpoints for"
    ),
):
    """List all checkpoints for the current environment"""
    data_dir = DataDir()

    checkpoints = data_dir.get_environment_checkpoints(prefix=path)
    checkpoints.sort(key=lambda x: x.timestamp, reverse=True)

    table = Table(title="Checkpoints")
    table.add_column("uuid", justify="left", no_wrap=True)
    table.add_column("tags", justify="left", no_wrap=True)
    table.add_column("timestamp", justify="left", no_wrap=True)

    for point in checkpoints:
        table.add_row(point.uuid, str(point.tags), point.timestamp)

    rich.print(table)

