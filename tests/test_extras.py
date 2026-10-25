"""Skills-only connector discovery and MCP resource delivery."""

import asyncio
import hashlib
import importlib.util
import re
import socket
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mcp import Client, StdioServerParameters
from mcp.client.extension import advertise
from mcp.types import Request, RequestParams, Result
from yamcps import RagContext
from yamcps.connectors import load
from yamcps.rag import Document, Index
from yamcps.server import create_server
from yamcps.skills import GetSkillParams

from yamcps_extras import ExtrasConnector


class SkillsResult(Result):
    skills: list[dict]


class SkillResult(Result):
    skill: dict


class ExtrasTests(unittest.TestCase):
    def test_entry_point_and_bundled_references(self):
        connector = load(["extras"])[0]
        self.assertIsInstance(connector, ExtrasConnector)
        roots = list(connector.skill_roots())
        self.assertEqual(
            {root.name for root in roots},
            {
                "extras-configure-agents",
                "extras-develop-plugin",
                "extras-create-cicd",
                "extras-changelog",
                "extras-python",
            },
        )
        for root in roots:
            text = (root / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(root.name.startswith("extras-"))
            self.assertNotIn("TODO", text)
            for target in re.findall(r"\]\(((?:assets|references)/[^)]+)\)", text):
                self.assertTrue((root / target).is_file(), target)
        self.assertFalse(hasattr(connector, "required_secrets"))
        self.assertFalse(hasattr(connector, "configure"))


def bundled_resource_count():
    return sum(
        1 for root in ExtrasConnector().skill_roots() for path in root.rglob("*") if path.is_file()
    )


class ExtrasIntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def exercise(self, target):
        expected = {root.name for root in ExtrasConnector().skill_roots()}
        async with Client(
            target, extensions=[advertise("io.modelcontextprotocol/skills")]
        ) as client:
            self.assertEqual((await client.list_tools()).tools, [])
            self.assertEqual((await client.list_prompts()).prompts, [])
            listed = await client.session.send_request(
                Request(method="skills/list", params=RequestParams()), SkillsResult
            )
            self.assertEqual({s["frontmatter"]["name"] for s in listed.skills}, expected)
            resources = (await client.list_resources()).resources
            self.assertEqual(len(resources), bundled_resource_count())
            self.assertTrue(all(str(r.uri).startswith("skill://extras-") for r in resources))
            for skill in listed.skills:
                fetched = await client.session.send_request(
                    Request(method="skills/get", params=GetSkillParams(uri=skill["uri"])),
                    SkillResult,
                )
                self.assertEqual(fetched.skill, skill)
                for resource in skill["resources"]:
                    response = await client.read_resource(resource["uri"])
                    data = response.contents[0].text.encode()
                    self.assertEqual(len(data), resource["size"])
                    self.assertEqual(
                        "sha256:" + hashlib.sha256(data).hexdigest(), resource["digest"]
                    )
            with self.assertRaises(Exception):
                await client.read_resource("skill://extras-configure-agents/../private")
            for removed in ("extras-add-core-feature", "extras-fix-core-bug"):
                with self.assertRaises(Exception):
                    await client.read_resource(f"skill://{removed}/SKILL.md")

    async def test_documented_conditional_secrets_recipe(self):
        from yamcps import ConfigSpec, ConnectorConfigs, ConnectorSecrets, SecretSpec
        from yamcps.connectors import ConnectorError
        from yamcps.secrets import SecretError

        root = next(
            root for root in ExtrasConnector().skill_roots() if root.name == "extras-develop-plugin"
        )
        text = (root / "assets/plugin-template.md").read_text(encoding="utf-8")
        recipe = text.split("## Recette : secrets conditionnels (yamcps 0.4.0)", 1)[1]
        code = re.search(r"```python\n(.*?)```", recipe, re.DOTALL).group(1)
        namespace = {
            "ConfigSpec": ConfigSpec,
            "ConnectorConfigs": ConnectorConfigs,
            "ConnectorSecrets": ConnectorSecrets,
            "SecretSpec": SecretSpec,
        }
        exec(compile(code, str(root), "exec"), namespace)
        methods = {
            name: value
            for name, value in namespace.items()
            if name
            in {
                "required_configs",
                "required_secrets",
                "required_secrets_for_configs",
                "configure",
                "configure_configs",
            }
        }
        methods.update(id="weather", register=lambda self, server: None)
        connector_type = type("Weather", (), methods)
        for mode, secrets, expected_error in (
            ("public", {}, None),
            ("private", {"YAMCPS_WEATHER_API_TOKEN": "fake-token"}, None),
            ("private", {}, ConnectorError),
            ("invalid", {}, ConnectorError),
        ):
            with self.subTest(mode=mode, missing=not secrets):
                connector = connector_type()
                with patch("yamcps.server.load", return_value=[ExtrasConnector(), connector]):
                    kwargs = dict(
                        config_values={"YAMCPS_WEATHER_MODE": mode}, secret_values=secrets
                    )
                    if expected_error:
                        with self.assertRaises((expected_error, SecretError)):
                            create_server(**kwargs)
                    else:
                        server = create_server(**kwargs)
                        self.assertEqual(connector.mode, mode)
                        self.assertEqual(connector.token is None, mode == "public")
                        async with Client(server) as client:
                            self.assertEqual((await client.list_tools()).tools, [])

    async def test_memory(self):
        await self.exercise(create_server(["extras"]))

    async def test_stdio(self):
        await self.exercise(
            StdioServerParameters(
                command=sys.executable, args=["-m", "yamcps", "serve", "--connector", "extras"]
            )
        )

    async def test_http(self):
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        with tempfile.TemporaryFile() as output:
            process = await asyncio.create_subprocess_exec(
                sys.executable,
                "-m",
                "yamcps",
                "serve",
                "--connector",
                "extras",
                "--transport",
                "http",
                "--port",
                str(port),
                stdout=output,
                stderr=output,
            )
            try:
                async with asyncio.timeout(15):
                    while True:
                        if process.returncode is not None:
                            self.fail("Extras HTTP process exited")
                        try:
                            _, writer = await asyncio.open_connection("127.0.0.1", port)
                            writer.close()
                            await writer.wait_closed()
                            break
                        except OSError:
                            await asyncio.sleep(0.05)
                await self.exercise(f"http://127.0.0.1:{port}/mcp")
            finally:
                if process.returncode is None:
                    process.terminate()
                await asyncio.wait_for(process.wait(), timeout=10)

    async def test_coexists_with_sibling(self):
        class Sibling:
            id = "sibling"

            def register(self, server):
                @server.tool()
                def sibling_echo(message: str) -> str:
                    return message

        with patch("yamcps.server.load", return_value=[ExtrasConnector(), Sibling()]):
            server = create_server(config_values={})
        async with Client(server) as client:
            self.assertEqual({t.name for t in (await client.list_tools()).tools}, {"sibling_echo"})
            self.assertEqual(
                len((await client.list_resources()).resources), bundled_resource_count()
            )
            response = await client.call_tool("sibling_echo", {"message": "extras coexist"})
            self.assertEqual(response.structured_content["result"], "extras coexist")

    async def test_documented_backend_recipe_coexists_with_extras(self):
        asset = (
            next(
                root
                for root in ExtrasConnector().skill_roots()
                if root.name == "extras-develop-plugin"
            )
            / "assets"
            / "plugin-template.md"
        )
        recipe = asset.read_text(encoding="utf-8").split(
            "### Backend détenu par le plugin (yamcps 0.3)", 1
        )[1]
        code = re.search(r"```python\n(.*?)```", recipe, re.DOTALL).group(1)
        namespace = {}
        exec(compile(code, str(asset), "exec"), namespace)

        class Weather:
            id = "weather"

            def rag_config(self):
                return namespace["config"]

            def configure_rag(self, context: RagContext):
                self.rag = context

            def register(self, server):
                @server.tool()
                def weather_search(query: str) -> list[str]:
                    return [hit.source_uri for hit in self.rag.index.search(query, "example")]

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "weather.sqlite3"
            weather = Weather()
            with (
                patch.dict("os.environ", {"YAMCPS_RAG_DIR": directory}),
                patch("yamcps.server.load", return_value=[ExtrasConnector(), weather]),
            ):
                server = create_server(config_values={}, secret_values={})
            self.assertFalse(path.exists())
            weather.rag.index.sync(
                "example",
                [
                    Document(
                        corpus="example",
                        document_id="guide",
                        revision="1",
                        text="evidence",
                        source_namespace="weather",
                    )
                ],
            )
            async with Client(server) as client:
                self.assertEqual(
                    len((await client.list_resources()).resources), bundled_resource_count()
                )
                result = await client.call_tool("weather_search", {"query": "evidence"})
                self.assertFalse(result.is_error)
                self.assertIn("weather://source/example/guide/1", str(result.structured_content))

    @unittest.skipUnless(importlib.util.find_spec("yamcps_docs"), "Optional cross-repo docs plugin")
    async def test_coexists_with_configured_docs_and_lazy_rag(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "docs.sqlite3"
            server = create_server(
                ["extras", "docs"],
                config_values={"YAMCPS_DOCS_INDEX": str(path), "YAMCPS_DOCS_MODEL": ""},
            )
            async with Client(server) as client:
                self.assertEqual(
                    {tool.name for tool in (await client.list_tools()).tools},
                    {"docs_search", "docs_get_document", "docs_get_passage", "docs_index_status"},
                )
                self.assertEqual((await client.list_prompts()).prompts, [])
                self.assertEqual(
                    len((await client.list_resources()).resources), bundled_resource_count() + 1
                )
                skill = await client.read_resource("skill://extras-develop-plugin/SKILL.md")
                self.assertIn("required_configs()", skill.contents[0].text)
                self.assertIn("yamcps.rag", skill.contents[0].text)
                self.assertFalse(path.exists())
                Index(path).sync(
                    "example",
                    [Document(corpus="example", document_id="SSS", revision="1", text="evidence")],
                )
                response = await client.call_tool(
                    "docs_search", {"query": "evidence", "corpus": "example"}
                )
                self.assertFalse(response.is_error)
                self.assertIn("evidence", str(response.structured_content))


if __name__ == "__main__":
    unittest.main()
