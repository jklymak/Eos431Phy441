# Setting up a python environment

## Install Mamba (or conda)

If you don't already have it (or conda), install mamba from [mambaforge](https://github.com/conda-forge/miniforge#mambaforge) appropriate for you computer architecture.

If you have conda it should work well, but make sure that your default channel is [conda-forge](https://conda-forge.org/docs/user/introduction.html#how-can-i-install-packages-from-conda-forge). However, note that mamba usually faster.

Mamba (and conda) provide "environments" or "kernels" to run your python-based programs.  They not only work with python files, but with c- and FORTRAN extensions used in much of scientific computing.  You could use `pip` instead, but you will likely hit roadblocks when dealing with netcdf files.

## Creating your environment

A list of packages is available that should work to create you an environment at <https://jklymak.github.io/Eos431Phy441/eos431environment.yml>.





