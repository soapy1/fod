# FOD

The purpose of fod is to experiment with automatic environment
checkpointing. It will sit on top of pixi, using it as a backend
to manage environments.

## Dev env

To setup your dev env, create a conda env

```
$ conda env create -f environment.yml 

$ conda activate fod-dev
```

Add the `fod` bin directory to path
```
$ export PATH="$pwd/fod/bin:$PATH"
```
