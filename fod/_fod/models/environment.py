import os
import datetime
from pydantic import BaseModel
import hashlib

from fod._fod.utils import short_uuid

class EnvironmentSpec(BaseModel):
    """Specifies a locked environment from pixi

    spec : str
      The pyproject.toml for the environemnt
    
    lockifle : str
      The pixi.lock for the environment

    lockfile_hash : str
      Hash for the content of the lockfile. If the lockfile hash has
      changed, then the environment has been updated. If the spec
      file has changed, it will cause a change in the lockfile as
      well.
    """
    spec: str
    lockfile: str
    lockfile_hash: str


class EnvironmentCheckpoint(BaseModel):
    """An environment at a point in time
    
    Only applys to a particular environment spec
    """
    environment: EnvironmentSpec
    timestamp: str
    uuid: str
    tags: list[str]

    @classmethod
    def from_path(cls, path: str):
        pixi_lock_path = f"{path}/pixi.lock"
        pyproject_toml_path = f"{path}/pyproject.toml" 
        if not os.stat(pixi_lock_path):
          raise Exception("did not find pixi lock")
        if not os.stat(pyproject_toml_path):
            raise Exception("did not find pyproject toml")

        pixi_lock = ""
        with open(pixi_lock_path, 'rb') as file:
            pixi_lock = file.read()

        pyproject_toml = ""
        with open(pyproject_toml_path, 'rb') as file:
            pyproject_toml = file.read()

        spec = EnvironmentSpec(
            spec = pyproject_toml,
            lockfile = pixi_lock,
            lockfile_hash = hashlib.sha256(pyproject_toml).hexdigest()
        )
        uuid = short_uuid()

        return cls(
            environment=spec,
            timestamp=str(datetime.datetime.now(datetime.UTC)),
            uuid=uuid,
            tags=[uuid]
        )
