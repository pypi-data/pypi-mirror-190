"""
    Dummy conftest.py for postopus.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest


@pytest.fixture
def mock_inp_and_parser_log(tmp_path):
    # mock inp file & parser.log
    tmpinpfile = tmp_path / "inp"
    tmpinpfile.write_text("Mock inp file")
    tmpexec = tmp_path / "exec"
    tmpexec.mkdir()
    tmpparser = tmpexec / "parser.log"
    tmpparser.write_text("UnitsOutput = 1")
