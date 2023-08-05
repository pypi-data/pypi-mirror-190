import os
import pathlib

import pytest


@pytest.mark.order(1)
def test_testdata_is_available():
    """Check if the testdata is available locally. We do this by checking if at
    least 1GB of data is in the tests subdirectory, and complain if not.

    [Possible improvement: ]It would be nicer to run this as a prerequisite for
    each test that relies on data. ]
    """
    testdatadir = pathlib.Path(__file__).parent
    # size of data in tests/data dir in bytes
    testdata_size = 0
    for path, dirs, files in os.walk(testdatadir):
        for f in files:
            filpath = pathlib.Path(os.path.join(path, f))
            if not filpath.is_symlink():
                testdata_size += filpath.stat().st_size

            # Early abort if some data is in the testdata dir (more than 50K, usually
            # expect around 10K
            if testdata_size > 50000:
                return

    if int(testdata_size) <= 50000:
        msg = "Test data not available\n"
        msg += "run `cd tests/data && python download_testdata.py`."
        raise ValueError(msg)
