import pathlib

import pytest

from postopus.files.vtk import VTKFile

testdata_dir = (
    pathlib.Path(__file__).parents[1] / "data" / "methane" / "output_iter" / "scf.0005"
)

test_file = testdata_dir / "density.vtk"

testfile_non_symmetric = (
    pathlib.Path(__file__).parents[1] / "data" / "benzene" / "static" / "density.vtk"
)


def test_vtk_cache_building():
    """
    Test opens file, then accesses the data field. Data for values, coords and dims
    will be loaded asynchronously in the background. Therefore need to access both
    as the first action after generation of the object.
    """
    vtkfile = VTKFile(test_file)
    assert vtkfile.values is not None
    del vtkfile
    vtkfile = VTKFile(test_file)
    assert vtkfile.coords is not None
    del vtkfile
    vtkfile = VTKFile(test_file)
    assert vtkfile.dims is not None


def test_vtk_get_coords_and_dims():
    """
    Test reading coordinates and dimensions from vtk file.

    """
    vtk_file = VTKFile(test_file)
    coords = vtk_file.coords

    assert list(coords.keys()) == ["x", "y", "z"]

    assert coords["x"].shape == coords["y"].shape == coords["z"].shape == (45,)

    assert coords["x"][0] == pytest.approx(-7.483315) == coords["x"].min()
    assert coords["x"][1] == pytest.approx(-7.1431640000000005)
    assert coords["y"][-1] == pytest.approx(7.4833290000000074) == coords["y"].max()
    assert coords["z"][11] == pytest.approx(-3.7416539999999996)

    assert vtk_file.dims == ("x", "y", "z")

    # Non-symmetric case, x, y, z not eq. long
    ns_vtk_file = VTKFile(testfile_non_symmetric)
    ns_coords = ns_vtk_file.coords

    assert list(coords.keys()) == ["x", "y", "z"]

    assert ns_coords["x"].shape == (95,)
    assert ns_coords["y"].shape == (99,)
    assert ns_coords["z"].shape == (67,)

    assert ns_coords["x"][0] == -7.05 == ns_coords["x"].min()
    assert ns_coords["x"][-1] == pytest.approx(7.05) == ns_coords["x"].max()
    assert ns_coords["y"][-1] == pytest.approx(7.35) == ns_coords["y"].max()
    assert ns_coords["y"][10] == -5.85
    assert ns_coords["z"][-1] == pytest.approx(4.95) == ns_coords["z"].max()

    assert ns_vtk_file.dims == ("x", "y", "z")


def test_vtk_get_values():
    """
    Test reading data values from a vtk file.

    """
    vtk_file = VTKFile(test_file)
    values = vtk_file.values

    assert values[18][18][18] == pytest.approx(0.014290557698991227)
    assert values[0][13][23] == pytest.approx(1.3888117688797775e-08)
    assert values[1][44][2] == 0.0
    assert values.min() == 0.0
    assert values.max() == pytest.approx(0.30489022753679973)

    assert values.shape == (45, 45, 45)
