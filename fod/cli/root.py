import typer


app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command()
def hello():
    """Hello?"""
    print("why, hellooooooo")


@app.command()
def goodbye():
    """bye?"""
    print("why good byyyyyee?")


# @app.command()
# def push(
#     target: Annotated[str, typer.Option(
#         "--target", "-t",
#         help="namespace/environment:tag to push to"
#     )],
#     rev: str = typer.Option(
#         help="uuid of the revision to push"
#     ),
#     prefix: str = typer.Option(
#         None,
#         help="prefix to save"
#     ),
# ):
#     """Push a checkpoint to a target"""
#     park_url = os.environ.get("PARK_URL")
#     api = Park(park_url)

#     namespace = target.split("/")[0]
#     env_tag = target.split("/")[1]
#     environment = env_tag.split(":")[0]
#     tag = env_tag.split(":")[1]

#     if prefix is None:
#         prefix = os.environ.get("CONDA_PREFIX")
#     else:
#         prefix = os.path.abspath(prefix)

#     chck = Checkpoint.from_uuid(prefix=prefix, uuid=rev)
#     data = chck.env_checkpoint.model_dump()

#     api.push(namespace, environment, tag, data)


# @app.command()
# def pull(
#     target: Annotated[str, typer.Option(
#         "--target", "-t",
#         help="namespace/environment:tag to push to"
#     )],
#     prefix: str = typer.Option(
#         None,
#         help="prefix to save"
#     ),
# ):
#     """Push a checkpoint to a target"""
#     park_url = os.environ.get("PARK_URL")
#     api = Park(park_url)

#     namespace = target.split("/")[0]
#     env_tag = target.split("/")[1]
#     environment = env_tag.split(":")[0]
#     tag = env_tag.split(":")[1]

#     checkpoint_data = api.pull(namespace, environment, tag)

#     if prefix is None:
#         prefix = os.environ.get("CONDA_PREFIX")
#     else:
#         prefix = os.path.abspath(prefix)

#     chck = Checkpoint.from_checkpoint_dict(checkpoint_data=checkpoint_data, prefix=prefix)
#     chck.save()
