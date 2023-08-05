import argparse
import os
import pathlib
import subprocess
from pwd import getpwnam
from sys import stderr


def eprint(msg):
    """
    Print to STDERR
    """
    print(f"ERROR: {msg}", file=stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate example data from all input " "files in tests/data."
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force recalculation of data, even if it already exists.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print Octopus' output to STDOUT."
    )
    parser.add_argument(
        "-p",
        "--parallel",
        metavar="mpi_tasks",
        help="Run Octopus in parallel. Provide number of " "MPI processes to use.",
    )
    octobinary = parser.add_mutually_exclusive_group(required=True)
    octobinary.add_argument(
        "-o", "--octopus", metavar="octopus_binary", help="Path to Octopus executable."
    )
    octobinary.add_argument(
        "-d",
        "--docker",
        action="store_true",
        help="Use docker to build and execute Octopus.",
    )
    args = parser.parse_args()

    # Check if parameter 'octopus' is set and legal
    if args.octopus is not None:
        if not os.path.isfile(args.octopus):
            eprint("Bad path to Octopus executable!")
            exit(-1)
        if not os.access(args.octopus, os.X_OK):
            eprint("Provided Octopus is not executable!")
            exit(-1)

    if args.parallel is not None:
        try:
            mpiprocs = int(args.parallel)
            if mpiprocs < 1:
                raise TypeError
        except TypeError:
            eprint("Argument to 'parallel'/'p' is not an int or smaller than 1!")
            exit(-1)
    else:
        mpiprocs = 1

    """
    Actual process that starts data generation
    """
    if args.docker is not None:
        import docker

    basepath = pathlib.Path.cwd().parent.parent
    octopus_run_cmd = ""
    if args.octopus is not None:
        if args.parallel is not None:
            octopus_run_cmd = "mpirun -np " + str(mpiprocs) + " " + args.octopus
        else:
            octopus_run_cmd = args.octopus
    elif args.docker is not None:
        # We need to make sure there is a image in docker
        client = docker.from_env()
        client.images.build(path=str(basepath / "dev" / "docker"), tag="octopus")
        # Set octopus_run_cmd to a dummy value
        octopus_run_cmd = "docker"
    else:  # Try if octopus binary is in $PATH
        import shutil

        # Check if octopus binary is in $PATH
        if shutil.which("octopus") is None:
            raise EnvironmentError(
                "No Octopus binary in $PATH! Please alter $PATH "
                "or use --octopus or --docker!"
            )

        # Check if mpirun exists
        if shutil.which("mpirun") is None:
            eprint("MPI not found on system! Will continue with serial octopus.")
            octopus_run_cmd = args.octopus
        else:
            octopus_run_cmd = (
                "mpirun -np " + str(mpiprocs) + " " + shutil.which("octopus")
            )

    output_dirs = ["exec", "output_iter", "restart", "static", "td.general"]
    # Path, where example 'inp's are expected
    expath = os.path.join(basepath, "tests", "data")
    # Iterate over all directories
    for root, dirs, files in os.walk(expath):
        # if it does not contain a 'inp' file, skip
        if "inp" not in files:
            continue

        # DBG
        print(f"Working on example {root}")

        exists = False
        for o in output_dirs:
            if o in dirs:
                exists = True
                break

        if exists and args.force is None:
            eprint(f"Data exists in {root}")
            continue
        elif exists and args.force is None:
            print(f"Data exists in {root} - overwriting!")

        # Executing Octopus for the current 'inp'
        if octopus_run_cmd == "docker":
            # start Docker container
            pass
            # image: image name of octopus container
            # $USER would contain "root", if setup.py is executed with 'sudo'
            if os.getenv("USER") == "root":
                user = getpwnam(os.getenv("SUDO_USER")).pw_uid
            else:
                user = getpwnam(os.getenv("USER")).pw_uid
            # set verbosity
            if args.verbose is not None:
                tty = True
                detach = False
            else:
                tty = False
                detach = True

            cont = client.containers.run(
                image="octopus",
                command="octopus",
                user=user,
                volumes={root: {"bind": "/io", "mode": "rw"}},
                tty=tty,
                detach=detach,
                environment={"MPIPROCS": mpiprocs},
            )

            if args.verbose and detach:
                cont.logs()
            elif args.verbose and not detach:
                print(cont.decode())

        else:
            # Run provided Octopus binary
            octoproc = subprocess.Popen(
                octopus_run_cmd, cwd=root, stdout=subprocess.PIPE
            )
            if args.verbose:
                # Grab STDOUT line by line and print it
                while octoproc.poll() is None:
                    print(octoproc.stdout.readline().decode())
                # Catch remaining lines, after process exited
                print(octoproc.stdout.read().decode())
