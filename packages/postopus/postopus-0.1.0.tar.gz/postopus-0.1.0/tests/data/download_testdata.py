#!/usr/bin/env python

import os
import platform
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from typing import List

import requests

POSTOPUS_TESTDATA_PROJECT_ID = "31045608"
POSTOPUS_TESTDATA_URL = "https://gitlab.com/dremerb/postopus-testdata"


def duplicate_with_missing_to_symlink(base: str, target: str, missing: List[str]):
    """
    Creates a new "example" in Postopus' tests/data directory from an existing one.
    New example may have missing files/folders. Data is not copied, but symlinked.

    Parameters
    ----------
    base: str
        Name of the example that shall be "duplicated"
    target: str
        Name of the "duplicated" example (result folder)
    missing: List[str]
        List of files or folders that shall be missing from the original data. Path
        shall be relative to base. E. g. for example output "methane", not copying
        "scf.0003" and "inp" must be ["output_iter/scf.0001", "inp"]

    """
    testdatadir = Path(__file__).parent
    # Check if there exists some example to duplicate
    basepath = testdatadir / base
    if not basepath.is_dir():
        raise FileNotFoundError(f"No folder '{base}' in path {testdatadir}!")

    # Check to not override stuff
    targetpath = testdatadir / target
    if targetpath.exists():
        raise FileExistsError(
            f"A file/folder named '{target}' already exists in" f"{testdatadir}!"
        )

    os.mkdir(targetpath)
    # Command for link depends on the operating system. Unix can hardlink folders, in
    # Windows we need a hardlink for every file.
    if platform.system() == "Linux":
        subprocess.run(["cp", "-alT", base, target])
    elif platform.system() == "Darwin":
        subprocess.run(f"cp -R -L {base} {target}", shell=True)
    elif platform.system() == "Windows":
        # Windows is a little more complicated.
        # Now create the directory structure and link every file.
        # Directories are "real", data/files only are hard-linked.
        # For now we ignore `missing` list, as removing those afterwards is much easier
        for path, folders, files in os.walk(basepath):
            levelpath = Path(path)
            # Create folders for this level
            for fol in folders:
                # This might not be pretty, because we add a string with directory
                # structure to a pathlib.Path - but it works
                os.mkdir(targetpath / os.path.relpath(levelpath / fol, basepath))

            # Create symlinks to files
            for fil in files:
                os.symlink(
                    levelpath / fil,
                    targetpath / os.path.relpath(levelpath, basepath) / fil,
                )
                subprocess.run(
                    f"powershell -Command New-Item -ItemType HardLink -Path "
                    f"{targetpath / os.path.relpath(levelpath, basepath) / fil} "
                    f"-Value {levelpath / fil}"
                )
    else:
        # Don't know what we're running on, abort mission!
        print("Don't know how to handle this operating system!", file=sys.stderr)
        exit(-1)

    # Remove data that's supposed to be missing. Do this after building the whole
    # structure in the previous loop, as this removes the need for checking whether
    # things are folders or files.
    for misfil in missing:
        if Path(targetpath / misfil).is_dir():
            # Do manual recursive remove
            for path, folders, files in os.walk(targetpath / misfil):
                # Unlink all files (they are symlinks anyways)
                for fil in files:
                    (Path(path) / fil).unlink()
                # Remove all folders (should be empty now)
                for fol in folders:
                    (Path(path) / fol).rmdir()
            # Remove actual folder
            (targetpath / misfil).rmdir()
        else:
            Path(targetpath / misfil).unlink()


site = requests.get(
    url=f"https://gitlab.com/api/v4/projects/"
    f"{POSTOPUS_TESTDATA_PROJECT_ID}/repository/tags"
)
versions = site.json()
most_recent_v = versions[0]["name"]

archive_url = (
    f"{POSTOPUS_TESTDATA_URL}/-/archive/{most_recent_v}/"
    f"postopus-testdata-{most_recent_v}.tar.gz"
)

tar_filename = "testdata_download_tmp.tar.gz"

print(
    f"Downloading testdata with version '{most_recent_v}' "
    f"from {archive_url}.\nMight take a minute or two, go get a coffee :)"
)

response = requests.get(archive_url, stream=True)

if response.status_code == 200:
    with open(tar_filename, "wb") as f:
        f.write(response.raw.read())

try:
    tar = tarfile.open(tar_filename, "r:gz")
    tar.extractall(path="./unpack_tmp")
    tar.close()
    exit_code = 0
except EOFError as e:
    print("It failed extracting the tar")
    print(e)


# Data now is in './unpack_tmp/postopus-testdata-{most_recent_v}/'
# need to move this data now to '.'
for src_file in Path(f"./unpack_tmp/postopus-testdata-{most_recent_v}/").glob("*"):
    try:
        shutil.move(str(src_file), ".")
    except shutil.Error:
        # Folder/File already exists in '.'
        print(
            f"Please remove '{src_file.name}' from the tests/data folder!",
            file=sys.stderr,
        )
        exit_code = -1

# Create extra test cases
duplicate_with_missing_to_symlink("methane", "methane_min_no_static", ["static"])

duplicate_with_missing_to_symlink(
    "methane", "methane_missing_scf_iter", ["output_iter/scf.0004"]
)
duplicate_with_missing_to_symlink(
    "methane", "methane_missing_td_iter", ["output_iter/td.0000003"]
)
duplicate_with_missing_to_symlink(
    "archimedean_spiral",
    "archimedean_spiral_missing_vector_dimensions",
    [
        "Maxwell/output_iter/td.0000000/e_field-z.z=0",
        "Maxwell/output_iter/td.0000000/e_field-z.x=0,y=0",
    ],
)
if exit_code == 0:
    # Cleanup
    shutil.rmtree("./unpack_tmp")
    pass
else:
    print("Downloaded data is in ./unpack_tmp")
    print("You can attempt to copy it manually using")
    print(f"rsync -auv ./unpack_tmp/postopus-testdata-{most_recent_v}/* .")

os.remove(tar_filename)
exit(exit_code)
