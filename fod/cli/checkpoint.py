import os
import typer
import subprocess
from typing_extensions import Annotated
from rich.table import Table
import rich

from fod._fod.utils import ensure_dir
from fod._fod.data_dir import DataDir
from fod._fod.park.park import Park
from fod._fod.models import environment


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


@checkpoint_command.command()
def push(
    target: Annotated[str, typer.Option(
        "--target", "-t",
        help="namespace/environment:tag to push to"
    )],
    path: str = typer.Option(
        help="prefix to list checkpoints for"
    ),
    rev: str = typer.Option(
        help="uuid of the revision to push"
    ),
):
    """Push a checkpoint to a target"""
    park_url = os.environ.get("PARK_URL")
    api = Park(park_url)

    namespace = target.split("/")[0]
    env_tag = target.split("/")[1]
    environment = env_tag.split(":")[0]
    tag = env_tag.split(":")[1]

    data_dir = DataDir()
    chck = data_dir.get_environment_checkpoint(prefix=path, uuid=rev)
    data = chck.model_dump()

    api.push(namespace, environment, tag, data)
    print("pushed!")


@checkpoint_command.command()
def pull(
    target: Annotated[str, typer.Option(
        "--target", "-t",
        help="namespace/environment:tag to push to"
    )],
):
    """Pull a checkpoint from a target"""
    park_url = os.environ.get("PARK_URL")
    api = Park(park_url)

    namespace = target.split("/")[0]
    env_tag = target.split("/")[1]
    env_name = env_tag.split(":")[0]
    tag = env_tag.split(":")[1]

    checkpoint_data = api.pull(namespace, env_name, tag)

    chck = environment.EnvironmentCheckpoint(
        timestamp = checkpoint_data["timestamp"],
        uuid = checkpoint_data["uuid"],
        tags = checkpoint_data["tags"],
        environment = environment.EnvironmentSpec(
            spec = checkpoint_data["environment"]["spec"],
            lockfile = checkpoint_data["environment"]["lockfile"],
            lockfile_hash = checkpoint_data["environment"]["lockfile_hash"],
        )
    )

    data_dir = DataDir()
    data_dir.save_environment_checkpoint(chck, prefix=f"{namespace}/{env_name}", latest=True)

