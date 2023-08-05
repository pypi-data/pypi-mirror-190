from typing import Dict, Tuple

import numpy as np
import pyvista as pv

from postopus.files.file import File
from postopus.files.utils.units import get_units


class VTKFile(File):
    EXTENSIONS = ["vtk"]

    def __init__(self, filepath):
        """
        Enable Postopus to read VTK data, as written by Octopus.
        https://vtk.org/wp-content/uploads/2015/04/file-formats.pdf
        To write VTK output, 'inp' files must set 'OutputFormat' to 'vtk'.

        Parameters
        ----------
        filepath: pathlib.Path
            path to the file in VTK format
        """
        self.filepath = filepath

    def _readfile(self):
        """
        Actual reading of the file happens here.
        """
        self._mesh = pv.read(self.filepath)
        self._dims, self._coords = self._get_coords_and_dims()
        self._values = self._get_values()
        self._units = get_units(self.filepath)

    def _get_coords_and_dims(
        self,
    ) -> Tuple[Tuple[str, str, str], Dict[str, np.ndarray]]:
        """
        Get coords and dims from a vtk mesh.

        Coords is analogous to xarray.Dataset.coords, same for dims.

        From the documentation
         https://vtk.org/wp-content/uploads/2015/04/file-formats.pdf:
        'The file format supports 1D, 2D, and 3D structured point datasets.
         The dimensions nx, ny, nz must be greater than or equal to 1'.
         So that x, y and z will always exist, even for 1D or 2D data.

        Returns
        -------
        Tuple[str, str, str]
            dims

        Dict[str, np.ndarray]
            coords

        """
        dims = ("x", "y", "z")
        coords = {
            "x": np.unique(self._mesh.x),
            "y": np.unique(self._mesh.y),
            "z": np.unique(self._mesh.z),
        }
        return dims, coords

    def _get_values(self) -> np.ndarray:
        """
        Get data values from vtk mesh

        self._mesh.points and self._mesh.active scalars needs to be taken into account
        for generating the value grid. A simple
        lin_data.reshape(grid_size) would only work, if the length of
        each dimension is equal.

        Returns
        -------
        np.ndarray
            data values
        """
        grid_size = self._mesh.dimensions
        lin_data = np.array(self._mesh.active_scalars)
        # associate the value to the right point in space ###
        filled_arr = np.empty(grid_size)
        filled_arr[:] = np.nan

        # concatenate points in space with values
        points = np.c_[self._mesh.points, lin_data]

        # index-coordinate maps of dims, in vtk always 3 dims
        dim0_c_map = {co: idx for idx, co in enumerate(self._coords[self._dims[0]])}
        dim1_c_map = {co: idx for idx, co in enumerate(self._coords[self._dims[1]])}
        dim2_c_map = {co: idx for idx, co in enumerate(self._coords[self._dims[2]])}

        for point in points:
            filled_arr[
                dim0_c_map[point[0]], dim1_c_map[point[1]], dim2_c_map[point[2]]
            ] = point[3]

        values = filled_arr
        return values
