from pathlib import Path
from unittest import TestCase

from postopus.datacontainers.util.output_collector import OutputCollector


class OutputCollectorTest(TestCase):
    arch_spiral_path = Path(__file__).parents[2] / "data" / "archimedean_spiral"

    def test_fields(self):
        # Data for checking correctness
        check_fields_maxwell = {
            "td": [
                "maxwell_energy_density",
                "poynting_vector-z",
                "e_field-x",
                "b_field-y",
                "poynting_vector-x",
                "b_field-z",
                "e_field-y",
                "poynting_vector-y",
                "e_field-z",
                "b_field-x",
            ]
        }
        # sort fields, so that we can ignore positions in the lists
        check_fields_maxwell["td"].sort()
        check_avail_systems = ["Maxwell", "Medium", "default"]

        oc = OutputCollector(self.arch_spiral_path)
        self.assertEqual(oc._filesystem_systems, check_avail_systems)
        maxwell_td_fields = oc.find_fields("Maxwell")
        # sort fields, so that we can ignore positions in the lists
        maxwell_td_fields["td"].sort()
        self.assertEqual(maxwell_td_fields, check_fields_maxwell)
        self.assertEqual(oc.find_fields("Medium"), {})
        self.assertEqual(oc.find_fields("default"), {})

    def check_found_iterations(self):
        return

    def test_calculationmodes(self):
        return
