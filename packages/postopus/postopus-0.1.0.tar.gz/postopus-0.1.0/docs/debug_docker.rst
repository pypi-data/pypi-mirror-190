How-to: Debug Runs in Docker Container
======================================

When adding new tests, the runs inside the Docker container might fail. E. g. CGAL or NetCDF support might
be missing in the Docker image. Or the archimedeantrial spiral example cannot run with only 1 MPI process.

How can you debug this? Start the container interactively and try running it manually:

.. code-block:: bash

    user@laptop# cd /path/to/failing/inp
    user@laptop# sudo docker run --user `id -u ${SUDO_USER}` --env MPIPROCS=6 -v `pwd`:/io -ti octopus bash
    root@docker:/io$ source ~/spack/share/spack/setup-env.sh
    root@docker:/io$ spack load octopus
    root@docker:/io$ mpirun -np [number of mpi processes here] octopus
..
