import pathlib

import pandas

from postopus.files.pandas_text import PandasTextFile
from postopus.octopus_run import Run

testdata_dir = pathlib.Path(__file__).parent / "data"


def test_finding_static_data():
    run = Run(testdata_dir / "methane")
    assert sorted(run.default.td.fields.keys()) == sorted(
        [
            "current",
            "density",
            "energy",
            "laser",
            "multipoles",
        ]
    )


def test_loading_static_data():
    run = Run(testdata_dir / "methane")
    # convergence and forces are DataFrames
    assert type(run.default.td.energy) == pandas.DataFrame
    assert type(run.default.td.laser) == pandas.DataFrame
    assert type(run.default.td.multipoles) == pandas.DataFrame
    assert type(run.default.td.multipoles.attrs) == dict


def test_coordinates_attrs_reading():
    run = Run(testdata_dir / "celestial_bodies")
    exp_unit_dict = {
        "Iter": "[Iter n.]",
        "t": "[hbar/H]",
        "x(  1)": "[b]",
        "x(  2)": "[b]",
        "x(  3)": "[b]",
        "v(  1)": "[bH(2pi/h)]",
        "v(  2)": "[bH(2pi/h)]",
        "v(  3)": "[bH(2pi/h)]",
        "f(  1)": "[H/b]",
        "f(  2)": "[H/b]",
        "f(  3)": "[H/b]",
    }
    act_unit_dict = run.SolarSystem.Sun.td.coordinates.attrs["units"]

    assert exp_unit_dict == act_unit_dict


def test_standard_attrs_reading():
    """
    Test expected standard reading routine for attrs in tdgeneral files

    """
    run = Run(testdata_dir / "methane")
    exp_unit_dict = {
        "Iter": "[Iter n.]",
        "t": "[hbar/H]",
        "E(1)": "[H/b]",
        "E(2)": "[H/b]",
        "E(3)": "[H/b]",
    }
    exp_metadata_dict = {"dt": ["0.500000000000E-01 [hbar/H]"], "filename": "laser"}

    act_unit_dict = run.default.td.laser.attrs["units"]
    act_metadata_dict = run.default.td.laser.attrs["metadata"]

    assert exp_unit_dict == act_unit_dict
    assert exp_metadata_dict == act_metadata_dict


def test_total_curr_attrs_reading():
    """ """
    run = Run(
        testdata_dir
        / "octopus-tutorials"
        / "3-periodic_systems"
        / "3-bulk_Si"
        / "time_dependent"
    )
    assert run.default.td.total_current.attrs["units"]["t"] == "Units not specified"


def test_attrs_attribute():
    ptf = PandasTextFile(testdata_dir / "methane" / "td.general" / "laser")
    assert ptf.attrs is not None


def test_multisystems_reading():
    run = Run(testdata_dir / "celestial_bodies")
    assert run.SolarSystem.Earth.td.coordinates.shape == (73, 10)
    assert run.SolarSystem.Sun.td.coordinates.shape == (73, 10)
    assert run.SolarSystem.Moon.td.coordinates.shape == (73, 10)


# TODO: Something like test_find_static_without_cm_in_output_iter in static_data_test.py
