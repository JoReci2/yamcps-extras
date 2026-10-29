"""Development examples must not escape the project virtual environment."""

import re
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[1] / "src/yamcps_extras/skills"


class VenvGuidanceTests(unittest.TestCase):
    def test_python_shell_examples_use_explicit_venv_interpreter(self):
        for relative in (
            "extras-python/SKILL.md",
            "extras-develop-plugin/SKILL.md",
            "extras-develop-plugin/assets/plugin-template.md",
        ):
            text = (SKILLS / relative).read_text()
            for block in re.findall(r"```sh\n(.*?)```", text, re.DOTALL):
                for line in block.splitlines():
                    with self.subTest(resource=relative, command=line):
                        self.assertIsNone(
                            re.match(
                                r"(?:python|python3) (?!-m venv )|"
                                r"(?:pip|ruff|mypy|radon|bandit|coverage) ",
                                line,
                            )
                        )

    def test_generated_agent_instructions_require_environment(self):
        text = (SKILLS / "extras-configure-agents/assets/AGENTS.template.md").read_text()
        self.assertIn(".venv/bin/python", text)
        self.assertIn(".venv\\Scripts\\python.exe", text)
        self.assertIn("skill://extras-python/SKILL.md", text)


if __name__ == "__main__":
    unittest.main()
