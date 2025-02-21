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
        None,
        help="prefix to list checkpoints for"
    ),
    all: bool = typer.Option(
        False,
        help="show all checkpoints for all environments"
    )
):
    """List all checkpoints for the current environment"""
    data_dir = DataDir()

    if all:
        checkpoints = data_dir.get_all_environment_checkpoints()
    else:
        checkpoints = {path: data_dir.get_environment_checkpoints(prefix=path)}

    for chck_path, chks in checkpoints.items():
        table = Table(title=f"Checkpoints for {chck_path}")
        table.add_column("uuid", justify="left", no_wrap=True)
        table.add_column("tags", justify="left", no_wrap=True)
        table.add_column("timestamp", justify="left", no_wrap=True)

        for point in chks:
            table.add_row(point.uuid, str(point.tags), point.timestamp)

        rich.print(table)

