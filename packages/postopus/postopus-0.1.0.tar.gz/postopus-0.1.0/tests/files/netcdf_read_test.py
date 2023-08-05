import pathlib

import pytest

from postopus.files.netcdf import NetCDFFile

testdata_dir = (
    pathlib.Path(__file__).parents[1] / "data" / "methane" / "output_iter" / "scf.0005"
)
test_file = testdata_dir / "density.ncdf"

testfile_non_symmetric = (
    pathlib.Path(__file__).parents[1] / "data" / "benzene" / "static" / "density.ncdf"
)


def test_netcdf_cache_building():
    """
    Test opens file, then accesses the data field. Data for values, coords and dims
    will be loaded asynchronously in the background. Therefore need to access both
    as the first action after generation of the object.
    """
    netcdf_file = NetCDFFile(test_file)
    assert netcdf_file.values is not None
    del netcdf_file
    netcdf_file = NetCDFFile(test_file)
    assert netcdf_file.coords is not None
    del netcdf_file
    netcdf_file = NetCDFFile(test_file)
    assert netcdf_file.dims is not None


def test_netcdf_get_coords():
    """
    Test the reading of the coords of a netcdf file.

    """
    ncdf_file = NetCDFFile(test_file)
    coords = ncdf_file.coords

    assert list(coords.keys()) == ["x", "y", "z"]

    assert coords["x"].shape == coords["y"].shape == coords["z"].shape == (45,)

    assert coords["x"][0] == pytest.approx(-7.483315467834473) == coords["x"].min()
    assert coords["x"][1] == pytest.approx(-7.143164753913879)
    assert coords["y"][-1] == pytest.approx(7.483315944671631) == coords["y"].max()
    assert coords["z"][11] == pytest.approx(-3.7416576147079468)

    # Non-symmetric case, x, y, z not eq. long
    ns_xsf_file = NetCDFFile(testfile_non_symmetric)
    ns_coords = ns_xsf_file.coords

    assert list(coords.keys()) == ["x", "y", "z"]

    assert ns_coords["x"].shape == (95,)
    assert ns_coords["y"].shape == (99,)
    assert ns_coords["z"].shape == (67,)

    assert (
        ns_coords["x"][0] == pytest.approx(-7.050000190734863) == ns_coords["x"].min()
    )
    assert (
        ns_coords["x"][-1] == pytest.approx(7.050000369548798) == ns_coords["x"].max()
    )
    assert ns_coords["y"][-1] == pytest.approx(7.35000067949295) == ns_coords["y"].max()
    assert ns_coords["y"][10] == pytest.approx(-5.849999845027924)
    assert (
        ns_coords["z"][-1] == pytest.approx(4.950000584125519) == ns_coords["z"].max()
    )


def test_netcdf_get_dims():
    """
    Test the reading of the dims of a netcdf file

    """
    ncdf_file = NetCDFFile(test_file)
    dims = ncdf_file.dims
    assert dims == ("x", "y", "z")


def test_netcdf_get_values():
    """
    Test the reading of the values of a netcdf file.
    """
    ncdf_file = NetCDFFile(test_file)
    values = ncdf_file.values

    assert values[18][18][18] == pytest.approx(0.014290557698991227)
    assert values[0][13][23] == pytest.approx(1.3888117688797775e-08)
    assert values[1][44][2] == 0.0
    assert values.min() == 0.0
    assert values.max() == pytest.approx(0.30489022753679973)

    assert values.shape == (45, 45, 45)
