(python-environment)=
# Setting up a python environment

## Install Mamba (or conda)

If you don't already have it (or conda), install mamba from [mambaforge](https://github.com/conda-forge/miniforge#mambaforge) appropriate for you computer architecture.

If you have conda it should work well, but make sure that your default channel is [conda-forge](https://conda-forge.org/docs/user/introduction.html#how-can-i-install-packages-from-conda-forge). However, note that mamba is usually faster.

Mamba (and conda) provide "environments" or "kernels" to run your python-based programs.  They not only work with python files, but with c- and FORTRAN extensions used in much of scientific computing.  You could use `pip` instead, but you will likely hit roadblocks when dealing with netcdf files.

## Creating your environment

A list of packages is available that should work to create you an environment at [eos431environment.yml](./eos431environment.yml).  To use this file you simply do:

```
mamba env create -f eos431environment.yml
mamba env list
```

should return something like:

```
eos431                 /Users/jklymak/mambaforge/envs/eos431
```

To use this environment, you can do

```
mamba activate eos431
```

## Running jupyter notebooks

You are encouraged to use [jupyter](https://jupyter.org) notebooks for your data analysis and to hand in for your assignments.  You may be used to other ways to do this, but I usually use the command line:

```
mamba activate eos431
jupyter lab &
```

which should open a jupyterlab interface in your browser.

(syzygy)=
## Working on uvic.syzygy.ca

Some folks are used to working on <https://uvic.syzygy.ca>.  My short experience with this is that its pretty slow, and if many folks do it, we are liable to get in trouble.  But if you are really stuck because your computer is too ancient then you can do the install steps above, and then install a kernel to make it available on the syzygy machines.

To do this, I did the following

- uploaded [eos431environment.yml](./eos431environment.yml) to syzygy, as above, and put it in a subdirectory.
- Make an eos431 environment: from a terminal on syzygy, I ran the mamba command above: `mamba env create -f eos431environment.yml`.  At this point everything installed fine for me, so it should work for you as well.
- Run `mamba activate eos431` to activate the new environment.
- Install a kernel for jupyter: `python -m ipykernel install --user --name eos431 --display-name "Python (eos431)"`
- Refresh your kernel window, create a new notebook, but choose `Python (eos431)` as the kernel (instead of `Python3 (ipykernel)`).
- To run veros, just follow the instructions above in the command line (after `mamba activate eos431`.)




