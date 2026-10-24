"""Run with python3 -m unittest discover -s tests -v (requires yard)."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DownloadTests(unittest.TestCase):
    def test_downloads_fail_on_http_errors_and_are_not_piped(self):
        for path in ROOT.rglob("*.md"):
            for number, line in enumerate(path.read_text().splitlines(), 1):
                line = re.sub(r"{{.*?}}|{%.*?%}", "TEMPLATE", line)
                command = re.search(r"\b(curl|wget)\s+(.+)", line)
                if not command or command[2].strip() == "\\":
                    continue
                with self.subTest(path=str(path.relative_to(ROOT)), line=number):
                    arguments = command[2]
                    self.assertNotRegex(arguments, r"(?<!\|)\|(?!\|)")
                    if command[1] == "curl":
                        self.assertRegex(arguments, r"(?:^|\s)(?:--fail(?:-with-body)?\b|-[A-Za-z]*f[A-Za-z]*\b)")

    def test_rendered_download_failures_stop_before_consumers(self):
        cases = {
            "codex": ("codex-cli.md", {}),
            "claude": ("claude-cli.md", {}),
            "copilot": ("copilot-cli.md", {}),
            "bun": ("bun.md", {}),
            "bun-pinned": ("bun.md", {"version": "bun-v1.2.19"}),
            "deno": ("deno.md", {}),
            "deno-pinned": ("deno.md", {"version": "2.0.0"}),
            "turso": ("turso.md", {}),
            "uv": ("python/uv.md", {}),
            "uv-pinned": ("python/uv.md", {"version": "0.5.18"}),
            "nvm": ("nodejs/nvm.md", {}),
            "node": ("nodejs/node.js.md", {}),
            "zig": ("zig.md", {}),
            "jj": ("jujutsu.md", {"user_name": "test", "email": "test@example.com"}),
            "jj-pinned": ("jujutsu.md", {"version": "v0.35.0", "user_name": "test", "email": "test@example.com"}),
            "chrome": ("chrome.md", {}),
            "stripe": ("stripe.md", {}),
            "hurl": ("hurl.md", {}),
            "flutter": ("flutter/latest.md", {}),
            "github": ("github-cli.md", {}),
            "docker": ("docker.md", {}),
            "desktop": ("codex-desktop.md", {}),
        }
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            shutil.copytree(ROOT / "ubuntu", work / "modules/ubuntu")
            modules = {name: f"modules/ubuntu/features/{path}" for name, (path, _) in cases.items()}
            modules["base"] = "modules/ubuntu/bases/ubuntu.md"
            manifest = {
                "inputs": {"modules": modules},
                "outputs": {f"{name}.Containerfile": [{"base": {}}, {name: arguments}] for name, (_, arguments) in cases.items()},
            }
            (work / "yard.yaml").write_text(json.dumps(manifest))
            rendered = subprocess.run(["yard", "build", "--ignore-all-requires"], cwd=work, capture_output=True, text=True)
            self.assertEqual(rendered.returncode, 0, rendered.stdout + rendered.stderr)
            commands = work / "bin"
            commands.mkdir()
            log = work / "commands.log"
            # Keep all commands inside this temporary directory. The real shell
            # executes the generated RUN, while downloads fail without a network.
            for name in ("curl", "wget", "apt-get", "apt", "mkdir", "rm", "update-ca-certificates", "bash", "sh", "tar", "gpg", "install", "mv", "unzip", "jq"):
                status = 22 if name == "curl" else 8 if name == "wget" else 0
                stub = commands / name
                stub.write_text(f'#!/bin/sh\nprintf "%s\\n" "{name}" >> "$DOWNLOAD_TEST_LOG"\nexit {status}\n')
                stub.chmod(0o755)
            temporary_file = commands / "mktemp"
            temporary_file.write_text('#!/bin/sh\nprintf "%s/stub-download\\n" "$HOME"\n')
            temporary_file.chmod(0o755)
            environment = {**os.environ, "PATH": str(commands), "HOME": str(work), "FLUTTER_HOME": str(work / "flutter"), "DOWNLOAD_TEST_LOG": str(log)}
            checked = 0
            for name in cases:
                source = (work / f"{name}.Containerfile").read_text()
                source = "\n".join(line for line in source.splitlines() if line.strip() and not line.lstrip().startswith("#"))
                instructions = re.findall(r"^RUN ((?:[^\n]*\\\n)*[^\n]*)", source, re.MULTILINE)
                downloads = [instruction.replace("\\\n", " ") for instruction in instructions if re.search(r"\b(?:curl|wget)\s", instruction)]
                self.assertTrue(downloads, name)
                for instruction in downloads:
                    with self.subTest(module=name, command=instruction):
                        log.unlink(missing_ok=True)
                        result = subprocess.run(["/bin/sh", "-c", instruction], cwd=work, env=environment, capture_output=True, text=True)
                        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                        executed = log.read_text().splitlines()
                        self.assertTrue(set(executed) & {"curl", "wget"}, executed)
                        self.assertIn(executed[-1], {"curl", "wget"}, executed)
                        checked += 1
            self.assertGreaterEqual(checked, len(cases))


if __name__ == "__main__":
    unittest.main()
