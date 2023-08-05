import pathlib

import numpy.testing as npt
import pandas
import pytest

from postopus.octopus_run import Run

testdata_dir = pathlib.Path(__file__).parent / "data"


def test_finding_static_data():
    run = Run(testdata_dir / "methane")
    assert sorted(run.default.scf.fields.keys()) == sorted(
        [
            "density",
            "convergence",
            "forces",
            "info",
        ]
    )


def test_loading_static_data():
    run = Run(testdata_dir / "methane")
    # convergence and forces are DataFrames
    assert type(run.default.scf.convergence) == pandas.DataFrame
    assert type(run.default.scf.forces) == pandas.DataFrame
    # info is a list of strings
    assert type(run.default.scf.info) == list
    assert all(isinstance(item, str) for item in run.default.scf.info)


def test_find_static_without_cm_in_output_iter():
    run = Run(testdata_dir / "benzene")
    assert list(run.default.system_data.keys()) == ["scf"]
    # expect to only find non-fields here
    assert sorted(run.default.scf.fields.keys()) == sorted(
        [
            "density",
            "elf_rs",
            "v0",
            "vh",
            "vks",
            "vxc",
            "wf_st0001",
            "wf_st0002",
            "wf_st0003",
            "wf_st0004",
            "wf_st0005",
            "wf_st0006",
            "wf_st0007",
            "wf_st0008",
            "wf_st0009",
            "wf_st0010",
            "wf_st0011",
            "wf_st0012",
            "wf_st0013",
            "wf_st0014",
            "wf_st0015",
            "convergence",
            "forces",
            "info",
        ]
    )


def test_iteration_num_for_static_benzene():
    run = Run(testdata_dir / "benzene")
    # benzene has no output_iter, only "static" folder. This is added as a iteration
    assert run.default.scf.density.iteration_ids == (1,)
    static_no_arg = run.default.scf.density.get_converged(source="cube")
    static_iter_num = run.default.scf.density.get(1, source="cube")
    npt.assert_equal(static_no_arg.values, static_iter_num.values)


def test_iteration_num_for_static_methane():
    run = Run(testdata_dir / "methane")
    # methane has 16 iterations for 'scf' in output_iter, but we add one more for static
    assert sorted(run.default.scf.density.iteration_ids) == list(range(1, 18))
    assert isinstance(run.default.scf.density.iteration_ids, tuple)
    static_no_arg = run.default.scf.density.get_converged(source="xsf")
    static_iter_num = run.default.scf.density.get(17, source="xsf")
    npt.assert_equal(static_no_arg.values, static_iter_num.values)


def test_bandstructure_data_reading():
    exp_attrs_dict = {
        "units": {
            "coord.": "Coord",
            "kx": "(red.coord.)",
            "ky": "(red.coord.)",
            "kz": "(red.coord.)",
            "band_1": "[eV]",
            "band_2": "[eV]",
            "band_3": "[eV]",
            "band_4": "[eV]",
            "band_5": "[eV]",
            "band_6": "[eV]",
            "band_7": "[eV]",
            "band_8": "[eV]",
            "band_9": "[eV]",
            "band_10": "[eV]",
            "band_11": "[eV]",
            "band_12": "[eV]",
        },
        "metadata": {"filename": "bandstructure"},
    }
    run = Run(
        testdata_dir
        / "octopus-tutorials"
        / "3-periodic_systems"
        / "2-h-BN_monolayer"
        / "unoccupied"
    )
    assert run.default.scf.bandstructure.shape == (32, 15)
    assert run.default.scf.bandstructure.attrs == exp_attrs_dict


def test_eigenvalues_reading():
    info_dict = [
        "All states converged.",
        "Criterion =      0.100000E-06",
        "Eigenvalues [eV]",
    ]
    k_dict = {
        1: (0.0, 0.0, 0.0),
        2: (0.027778, 0.027778, 0.0),
        3: (0.055556, 0.055556, 0.0),
        4: (0.083333, 0.083333, 0.0),
        5: (0.111111, 0.111111, 0.0),
        6: (0.138889, 0.138889, 0.0),
        7: (0.166667, 0.166667, 0.0),
        8: (0.194444, 0.194444, 0.0),
        9: (0.222222, 0.222222, 0.0),
        10: (0.25, 0.25, 0.0),
        11: (0.277778, 0.277778, 0.0),
        12: (0.305556, 0.305556, 0.0),
        13: (0.333333, 0.333333, 0.0),
        14: (0.357143, 0.285714, 0.0),
        15: (0.380952, 0.238095, 0.0),
        16: (0.404762, 0.190476, 0.0),
        17: (0.428571, 0.142857, 0.0),
        18: (0.452381, 0.095238, 0.0),
        19: (0.47619, 0.047619, 0.0),
        20: (0.5, -0.0, 0.0),
        21: (0.458333, 0.0, 0.0),
        22: (0.416667, 0.0, 0.0),
        23: (0.375, -0.0, 0.0),
        24: (0.333333, -0.0, 0.0),
        25: (0.291667, 0.0, 0.0),
        26: (0.25, -0.0, 0.0),
        27: (0.208333, 0.0, 0.0),
        28: (0.166667, 0.0, 0.0),
        29: (0.125, -0.0, 0.0),
        30: (0.083333, -0.0, 0.0),
        31: (0.041667, -0.0, 0.0),
        32: (0.0, 0.0, 0.0),
    }

    run = Run(
        testdata_dir
        / "octopus-tutorials"
        / "3-periodic_systems"
        / "2-h-BN_monolayer"
        / "unoccupied"
    )

    assert run.default.scf.eigenvalues.shape == (384, 4)
    assert run.default.scf.eigenvalues.attrs["metadata"]["info"] == info_dict
    assert run.default.scf.eigenvalues.attrs["metadata"]["k"] == k_dict


def test_warning_on_missing_iteration_scf():
    with pytest.warns(UserWarning):
        # warning is raised in field.py
        run = Run(testdata_dir / "methane_missing_scf_iter")
        assert sorted(run.default.scf.density.iteration_ids)[0:6] == [
            1,
            2,
            3,
            5,
            6,
            7,
        ]


def test_warning_on_missing_iteration_td():
    with pytest.warns(UserWarning):
        # warning is raised in field.py
        run = Run(testdata_dir / "methane_missing_td_iter")
    assert sorted(run.default.td.density.iteration_ids)[0:6] == [0, 1, 2, 4, 5, 6]
