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

Make sure to also install [pixi](https://pixi.sh/)

## Try it out

Use the pixi environment provided in the `demo-assets/pixi-py` directory.

```
$ cd demo-assets/pixi-py

# install the env
$ fod install

# try installing some new packages
$ fod add filelock
$ fod add scipy

# list available checkpoints
$ fod checkpoint list
$ fod checkpoint list   
                         Checkpoints                          
┏━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ uuid     ┃ tags         ┃ timestamp                        ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 401a162b │ ['401a162b'] │ 2025-02-21 18:13:27.011398+00:00 │
│ 306aebf1 │ ['306aebf1'] │ 2025-02-21 18:02:59.879622+00:00 │
│ 6d7455ad │ ['6d7455ad'] │ 2025-02-21 18:01:30.833781+00:00 │
└──────────┴──────────────┴──────────────────────────────────┘

# try installing a checkpoint to another dir
$ cd ..
$ fod checkpoint install --target ./new-env --uuid 401a162b
```
