from pathlib import Path
import os
import yaml

from fod._fod.utils import ensure_dir
from fod._fod.models import environment

def default_data_dir() -> Path:
    dof_dir = os.environ.get("FOD_DIR", None)
    if dof_dir is None:
        dof_dir = Path.home() / ".fod"
    else:
        dof_dir = Path(dof_dir)
    
    return dof_dir / "data"


class DataDir:
    def __init__(self, data_dir: str | None = None):
        self.data_dir = data_dir
        if self.data_dir is None:
            self.data_dir = str(default_data_dir())
        
        ensure_dir(self.data_dir)

    def _get_env_dir(self, prefix: str):
        # Not stoked on this approach. But provides a mapping
        # between a prefix path and folder in a way that doesn't
        # get too long and remains unique
        name = prefix.replace("/", "+")
        return f"{self.data_dir}/{name}"

    def delete_environment_checkpoint(self, prefix: str, uuid: str):
        target_dir = self._get_env_dir(prefix)
        target_file = f"{target_dir}/{uuid}"
        if os.path.exists(target_file):
            os.remove(target_file)

    def save_environment_checkpoint(self, checkpoint: environment.EnvironmentCheckpoint, prefix: str, latest: bool = False):
        """Save an environment checkpoint to a prefix. By default the environment will be saved
        to <data_dir>/<prefix checkpoint dir>/<uuid>
        
        Parameters
        ----------
        checkpoint : environment.EnvironmentCheckpoint
            checkpoint to save
        
        prefix : str
            prefix that the environment belongs to

        latest : bool
            if set to true, will additionally save a version of the checkpoint to 
            the name 'latest'
        """
        target_dir = self._get_env_dir(prefix)
        ensure_dir(target_dir)
        
        target_file = f"{target_dir}/{checkpoint.uuid}"
        with open(target_file, "w+") as file:
            yaml.dump(checkpoint.model_dump(), file)

        if latest:
            target_file = f"{target_dir}/latest"
            with open(target_file, "w+") as file:
                yaml.dump(checkpoint.model_dump(), file)

    def get_environment_checkpoint(self, prefix: str, uuid: str) -> environment.EnvironmentCheckpoint:
        target_dir = self._get_env_dir(prefix)
        target_file = f"{target_dir}/{uuid}"
        if not os.path.exists(target_file):
            return None
        
        with open(target_file, 'r') as file:
            contents = yaml.safe_load(file)
            return environment.EnvironmentCheckpoint.parse_obj(contents)
    
    def get_environment_checkpoints(self, prefix: str) -> list[environment.EnvironmentCheckpoint]:
        target_dir = self._get_env_dir(prefix)
        if not os.path.isdir(target_dir):
            return []
        files = os.listdir(target_dir)

        checkpoints = []
        for file in files:
            # the latest file is a duplicate, skip 
            if file == "latest":
                continue
            with open(os.path.join(target_dir, file), 'r') as file:
                contents = yaml.safe_load(file)
            
            checkpoints.append(environment.EnvironmentCheckpoint.parse_obj(contents))
        
        checkpoints.sort(key=lambda x: x.timestamp, reverse=True)
        return checkpoints
    
    def get_all_environment_checkpoints(self) -> dict[str, list[environment.EnvironmentCheckpoint]]:
        """Get a dict of all the saved checkpoints for all environments. The return value 
        takes the form:

        {
            <prefix path>: [
                <environment checkpoints>
            ],
            "/home/my/env/location": [
               environment.EnvironmentCheckpoint("checkpoint1"),
               environment.EnvironmentCheckpoint("checkpoint1")  
            ]
        }

        Returns
        -------
        env_checkpoints : dict[str, list[environment.EnvironmentCheckpoint]]
            Dict of environment path to list of checkpoints for the environment
        
        """
        checkpoint_dirs = [path for path in os.listdir(self.data_dir) if os.path.isdir(os.path.join(self.data_dir, path))]
        
        env_checkpoints = {}
        for prefix in checkpoint_dirs:
            checkpoints = self.get_environment_checkpoints(prefix=prefix)
            env_checkpoints[prefix] = checkpoints

        return env_checkpoints
        
    def get_latest(self, prefix: str) -> environment.EnvironmentCheckpoint:
        target_dir = self._get_env_dir(prefix)
        target_file = f"{target_dir}/latest"
        if not os.path.exists(target_file):
            # TODO: it would be nice if this searched all the checkpoints
            # to determine the latest one, opposed to giving up like this
            return None
        
        with open(target_file, 'r') as file:
            contents = yaml.safe_load(file)
            return environment.EnvironmentCheckpoint.parse_obj(contents)
