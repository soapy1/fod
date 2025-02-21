from pydantic import BaseModel


class EnvironmentSpec(BaseModel):
    """Specifies a locked environment from pixi

    spec : str
      The pyproject.toml for the environemnt
    
    lockifle : str
      The pixi.lock for the environment
    """
    spec: str
    lockfile: str


class EnvironmentCheckpoint(BaseModel):
    """An environment at a point in time
    
    Only applys to a particular environment spec
    """
    environment: EnvironmentSpec
    timestamp: str
    uuid: str
    tags: list[str]
