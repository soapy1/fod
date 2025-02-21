import os
import typer
import subprocess

from rich.table import Table
import rich

from fod._fod.utils import ensure_dir
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


@checkpoint_command.command()
def install(
    ctx: typer.Context,
    target: str = typer.Option(
        help="path to install into"
    ),
    uuid: str = typer.Option(
        help="uuid of the checkpoint to install"
    )
):
    """Install a checkpoint to a target path"""
    data_dir = DataDir()

    # ensure the target dir exists
    target = os.path.abspath(target)
    ensure_dir(target)

    # find the checkpoint the user wants to install
    checkpoints = data_dir.get_all_environment_checkpoints()
    checkpoints_flatten = []
    for chk in checkpoints.values():
        checkpoints_flatten += chk
    target_checkpoint = [chk for chk in checkpoints_flatten if chk.uuid == uuid]
    if len(target_checkpoint) == 0:
        print(f"checkpoint {uuid} not found!")
    else:
        # drop the checkpoint spec + lockfile into the target dir
        target_checkpoint = target_checkpoint[0]
        # lockfile = target_checkpoint.environment.lockfile.replace()
        with open(os.path.join(target, "pixi.lock"), "w") as f:
            f.write(target_checkpoint.environment.lockfile)
        with open(os.path.join(target, "pixi.toml"), "w") as f:
            f.write(target_checkpoint.environment.spec)

        print(f"installing target checkpoint for {uuid}")
        p = subprocess.Popen(["pixi", "install"], cwd=target)
        p.wait()
