# Postopus

[Postopus](https://gitlab.com/octopus-code/postopus/) (the POST-processing of OctoPUS data) is an environment that
can help with the analysis of data that was computed using the [Octopus](https://octopus-code.org) TDDFT package.

## Documentation

The documentation of postopus is hosted [here](https://octopus-code.gitlab.io/postopus/index.html).
To build the documentation locally: `cd docs && make html`. It will be built into: `docs/_build/html`. Open then the `index.html`

## Setup

Python versions supported: 3.8, 3.9. Python 3.10 is supported.
Release 0.1.0 will support octopus@12.1.

### User Setup

Using a virtual environment is recommended.
To install the project's dependencies, navigate (`cd`) into the project directory and run `pip install .`. The `docs` dependencies are highly recommended for all users (see below).

Note: ase is not listed as a dependency, but it will be needed, so please execute: `pip install git+https://gitlab.com/ase/ase.git@master`.
Context, for those who are interested: `ase` has already merged some of our feature requests that are needed for postopus, but they are not yet tag-released.
### Developer Setup

This section is for developers wanting to contribute to Postopus.
To setup your development environment, you not only need to install the dependencies of the project's code itself but also some modules for testing and keeping the repo clean through pre-commit hooks:

- Installing Postopus with development dependencies in editable mode can be done with `pip install -e .[dev]` (`pip >21.3` required)
  (or `pip install -e '.[dev]'` if you are using mac default's `zsh`) in the project's main directory. If you also want the `docs` requirements you would need to execute `pip install -e .[dev,docs]`
- After installing, you'll need to set up the pre-commit module. Do this with `pre-commit install` in the project's root.
- Tests might require output data from Octopus, for this refer to the section below (Downloading example and test data).

#### Invoke tasks

Currently, the following invoke tasks are available:

- **release**:   Run the release steps, which include syncing the git repo, building the package and pushing it to PyPI and finally tagging the release commit. By default, the task uploads to the test server; use the flag `--test=False` to upload to the real PyPI server. Release to the main PyPI can only be done from the main branch (use `--test=False` or `--no-test`) Example run:

```bash
$ invoke release --no-test
```

## Usage

Example codes in `src/postopus/examples`. The scripts in that folder can be used to easily debug the code.
`example_data_reading.py` shows how to instantiate a `Run` object that allows access to the data from a run with a single System.
`example_achimedeantrial_spiral.py` uses data from a run with multiple systems, providing an example with more complex Octopus output.

To execute these examples, you need to download the test data. (Or compute it, which is harder.)

## Downloading example and test data

A prepared set of output files can be downloaded by running ``cd tests/data && python download_testdata.py``.

### Jupyter Notebook

Check out the Jupyter Notebooks in `docs/notebooks`.

---

### Advanced: Build Example Data for Testing

Most users and developers can ignore this section.

On this version of postopus, one can download the test data as described above, so there is no need to build it. However, if you want to build the test data yourself, you can do so by following the instructions below.

Once you have downloaded the test data (and thus the `inp` files of the example data sets, you can in principle run octopus to compute the output data. We plan to use this later for more complete continuous integration. Here are the instructions for that procedure:

Several input files for smaller Octopus runs can be found in `tests/data`.
The script `tests/data/build_testdata.py` helps to run these examples and generates outputs.
An Octopus binary is required for execution. You can either provide one yourself by
providing the path to a binary with `-o` or you let the script build a Docker image and
run Octopus from inside a container with `-d`, or load octopus with spack. The latter option might require root on
Linux, because Docker - if you need to use `sudo`, make sure to use
`/path/to/virtualenv/bin/python` as the Python Interpreter if you use Virtual
Environments or similar.
Parameters for `build_testdata.py`:

- `--octopus /path/to/octopus/binary`, `--o /path/to/octopus/binary` use a custom Octopus binary
- `--docker`, `-d` build an image with Docker and use it to execute Octopus
- `--parallel mpi_tasks`, `-p mpi_tasks` run Octopus with `#processes` MPI processes
- `--verbose`, `-v` show output of Octopus on your STDOUT
- `--force`, `-f` overwrite existing results
- `--help`, `-h` show help on usage
