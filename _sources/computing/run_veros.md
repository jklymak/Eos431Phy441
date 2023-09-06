(run_veros)=

# Running Veros

![](https://veros.readthedocs.io/en/latest/_static/veros-logo-400px.png)

[Veros](https://veros.readthedocs.io/en/latest/) is a general ocean circulation model (GCM) that is written in python.  That makes it a bit slower than models written in C or FORTRAN, but we can learn a lot with relatively coarse simple simulations, using the model as a numerical laboratory to see the basic physics governing the ocean.

Despite our basic usage, Veros is pretty full-featured.  It has forcing from both wind stress and buoyancy forcing, and it has a relatively full-featured set of turbulence closure schemes to represent un-resolved turbulence.

## Installation

Veros should have been installed as part of your `eos431` environment (see {ref}`python-environment`).  After doing `mamba activate eos431` you should be able to use the `veros` command line tool:

```
veros --help
```

should echo to the command prompt:

```
Usage: veros [OPTIONS] COMMAND [ARGS]...

  Veros command-line tools
```

## The setup file

Each model run can be setup from a single python file that is called from the veros command-line tool, eg:

```
veros run --force-overwrite example.py
```

Where here we have named the setup file [example.py](./example.py).  Depending on what information is in this file, the program will run, sometimes for quite a while, and create netcdf files of the output.  For instance, this file might create a netcdf file named `example.snapshot.nc`.

For your assignments, I have already created these files for you.  However, you may wish to consult them to see how the models are set up.

Most of you should have `mpi` installed with `eos431` environment as well.  If you do, this can be used to speed up `veros` runs by using multiple processors on your machines.  You of course shouldn't use more processes than you have cores in your computer, and it actually can be counter-productive to use too many cores.  But some of the processes here can be sped up using 4 cores.  For instance, if we wanted to divide the x-y domain into 4 subdomains in x and 1 subdomain in y, we can do:

```
mpirun -np 4 veros run --force-overwrite example.py -n 4 1
```

A good rule of thumb is that its not worthwhile making either x or y less than 40 tiles wide.  So `example.py`, we have `settings.nx = 200`, so this is worth dividing into 4 cores, whereas `settings.ny = 4` is definitely not worth dividing.

## Output files

As noted, veros will output `example.snapshot.nc`.  It may also make `*.h5` restart files, which can be used to restart the model from part way through a run.