"""Dependency metadata exposed to package installers."""

import unittest
from importlib.metadata import requires

from packaging.requirements import Requirement


class DependencyTests(unittest.TestCase):
    def test_standard_install_requests_engine_dev_dependencies(self):
        requirements = [Requirement(value) for value in requires("yamcps-extras") or []]
        engine = [value for value in requirements if value.name == "yamcps"]
        self.assertEqual(len(engine), 1)
        requirement = engine[0]
        self.assertEqual(requirement.extras, {"dev"})
        self.assertIsNone(requirement.marker)
        self.assertIn("0.4.0", requirement.specifier)
        self.assertNotIn("0.5.0", requirement.specifier)


if __name__ == "__main__":
    unittest.main()
