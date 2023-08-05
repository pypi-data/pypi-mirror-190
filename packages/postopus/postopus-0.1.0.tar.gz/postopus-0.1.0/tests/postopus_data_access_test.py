import pathlib
from unittest import TestCase

import pandas as pd
import pytest

from postopus import Run


class PostopusDataReading(TestCase):
    testdata_dir = pathlib.Path(__file__).parent / "data"

    def test_read_scalarfield(self):
        run = Run(self.testdata_dir / "methane")
        self.assertListEqual(
            sorted(list(run.default.system_data.keys())), sorted(["td", "scf"])
        )

    def test_read_vectorfield(self):
        run = Run(self.testdata_dir / "archimedean_spiral")
        self.assertListEqual(list(run.Maxwell.system_data.keys()), ["td"])
        self.assertListEqual(sorted(run.Maxwell.td.e_field.components), ["x", "y", "z"])
        self.assertEqual(
            run.Maxwell.td.e_field.z.get(0, source="z=0").values.shape,
            (1, 401, 401),
        )

    def test_read_tdgeneralvectorfield(self):
        """
        Test reading td.general vector fields
        """
        run = Run(self.testdata_dir / "archimedean_spiral")
        self.assertListEqual(list(run.Maxwell.system_data.keys()), ["td"])
        self.assertListEqual(
            sorted(run.Maxwell.td.total_e_field.dimensions), ["x", "y", "z"]
        )
        self.assertEqual(
            run.Maxwell.td.total_e_field.z.shape,
            (801, 2),
        )
        self.assertEqual(
            type(run.Maxwell.td.total_e_field.z),
            pd.DataFrame,
        )

        self.assertAlmostEqual(
            run.Maxwell.td.total_e_field.z.loc[796][1],
            0.005419478420722,
        )

        self.assertAlmostEqual(
            run.Maxwell.td.total_e_field.y.loc[796][1],
            0.1245050904509,
        )

        self.assertEqual(
            run.Maxwell.td.total_e_field.z.attrs.keys(), {"units", "metadata"}
        )

        self.assertEqual(
            run.Maxwell.td.total_e_field.z.attrs["units"],
            {"Iter": "[Iter n.]", "t": "[hbar/H]", "E(1)": "[H/b]"},
        )

        self.assertEqual(
            run.Maxwell.td.total_e_field.z.attrs["metadata"],
            {"filename": "total_e_field_z", "dt": ["0.105328211714E-02 [hbar/H]"]},
        )

    def test_read_broken_vectorfield(self):
        with pytest.raises(
            FileNotFoundError,
            match=r"Error: inconsistent number of "
            r"files found for file_type [a-zA-z0-9!.:.,]",
        ):
            Run(self.testdata_dir / "archimedean_spiral_missing_vector_dimensions")

    def test_bad_path(self):
        with self.assertRaises(NotADirectoryError):
            run = Run(self.testdata_dir / "methane" / "inp")

        with self.assertRaises(FileNotFoundError):
            run = Run(self.testdata_dir)
            run

    def test_bad_outputformat_param(self):
        # Check Error on not-present data-format
        with self.assertRaises(ValueError):
            run = Run(self.testdata_dir / "methane")
            run.default.scf.density.get(1, source="z=0")

        # Check trying an illegal outputformat argument
        with self.assertRaises(ValueError):
            run.default.scf.density.get(1, source="bla")
