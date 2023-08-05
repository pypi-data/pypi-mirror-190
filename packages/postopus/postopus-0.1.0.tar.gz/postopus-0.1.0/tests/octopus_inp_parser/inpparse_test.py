import pathlib
from unittest import TestCase

import pytest

from postopus.octopus_inp_parser.inpparse import Parser


class ParserTest(TestCase):
    testdata_dir = pathlib.Path(__file__).parents[1] / "data"

    def test_input_parsing_multiple_systems(self):
        # Comparison data for testing
        check_keys = [
            "CalculationMode",
            "RestartWrite",
            "ExperimentalFeatures",
            "Debug",
            "Systems",
            "LinearMediumBoxShape",
            "LinearMediumBoxFile",
            "LinearMediumProperties",
            "CheckPointsMediumFromFile",
            "Maxwell.ParDomains",
            "Maxwell.ParStates",
            "lsize_mx",
            "lsize_mz",
            "dx_mx",
            "Maxwell.BoxShape",
            "Maxwell.Lsize",
            "Maxwell.Spacing",
            "MaxwellHamiltonianOperator",
            "MaxwellBoundaryConditions",
            "MaxwellAbsorbingBoundaries",
            "MaxwellABWidth",
            "MaxwellABPMLPower",
            "MaxwellABPMLReflectionError",
            "OutputFormat",
            "MaxwellOutput",
            "MaxwellOutputInterval",
            "MaxwellTDOutput",
            "MaxwellFieldsCoordinate",
            "Maxwell.TDSystemPropagator",
            "timestep",
            "Maxwell.TDTimeStep",
            "Medium.TDTimeStep",
            "TDPropagationTime",
            "lambda",
            "omega",
            "kz",
            "Ey",
            "pw",
            "p_s",
            "MaxwellIncidentWaves",
            "MaxwellFunctions",
        ]
        check_systems = ["Maxwell", "Medium", "default"]

        inp = Parser(self.testdata_dir / "archimedean_spiral" / "inp")
        self.assertEqual(list(inp.fields_raw.keys()), check_keys)
        self.assertEqual(list(inp.systems), check_systems)

    def test_input_parsing_default_system(self):
        inp = Parser(self.testdata_dir / "methane" / "inp")

        self.assertEqual(inp.systems["default"]["_systemtype"], "electronic")

    @pytest.mark.skip(reason="Multisystem 'inp' parsing is completely broken.")
    def test_multisystem_parsing(self):
        check_systems = [
            "SolarSystem",
            "SolarSystem.Sun",
            "SolarSystem.Earth",
            "SolarSystem.Moon",
            "_Global",
        ]
        particlemass_sun = "1.98855e30"

        inp = Parser(self.testdata_dir / "celestial_bodies" / "inp")

        self.assertListEqual(list(inp.systems.keys()), check_systems)
        self.assertEqual(inp.systems["SolarSystem"], particlemass_sun)
