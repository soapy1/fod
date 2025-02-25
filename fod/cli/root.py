import typer

from fod._fod.models import environment
from fod._fod.data_dir import DataDir
from fod.cli.checkpoint import checkpoint_command

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
)


app.add_typer(
    checkpoint_command,
    name="checkpoint",
    help="create and manage checkpoints",
    rich_help_panel="Checkpoint",
)


@app.command()
def maybe_checkpoint(
    path: str = typer.Option(
        help="path to the root pixi env"
    ),
):
    """make a checkpoint if there is a change from the last checkpoint"""
    env_checkpoint = environment.EnvironmentCheckpoint.from_path(path)
    
    data_dir = DataDir()

    # check to see what the latest checkpoint is. Will save this checkpoint
    # if there has been a change
    latest_checkpoint = data_dir.get_latest(path)
    if latest_checkpoint is None or latest_checkpoint.environment.lockfile_hash != env_checkpoint.environment.lockfile_hash:
        data_dir.save_environment_checkpoint(env_checkpoint, path, latest=True)
