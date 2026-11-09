"""Run with python3 -m unittest discover -s tests -v (requires yard and PyYAML)."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOWNLOAD = re.compile(r"(?:^|[;&|(`])\s*(?:curl|wget)\s", re.MULTILINE)


def run_instructions(source):
    source = "\n".join(line for line in source.splitlines() if line.strip() and not line.lstrip().startswith("#"))
    return [instruction.replace("\\\n", " ") for instruction in re.findall(r"^RUN\s+((?:[^\n]*\\\n)*[^\n]*)", source, re.MULTILINE | re.IGNORECASE)]


def module_config(source):
    config = re.search(r"^```yaml name=config\s*\n(.*?)^```", source, re.MULTILINE | re.DOTALL)
    return (yaml.safe_load(config[1]) or {}) if config else {}


def discover_download_cases(root):
    cases = {}
    for path in sorted(root.rglob("*.md")):
        source = path.read_text()
        fragments = re.findall(r"^```dockerfile\b[^\n]*\n(.*?)^```", source, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        # Remove template tags so a conditional command is still discoverable.
        dockerfile = re.sub(r"{{.*?}}|{%.*?%}", "", "\n".join(fragments), flags=re.DOTALL)
        if not any(DOWNLOAD.search(instruction) for instruction in run_instructions(dockerfile)):
            continue
        arguments = module_config(source).get("args", {})
        # Only rendering and failure propagation matter, so synthetic inputs
        # work without real identities or release versions.
        required = {argument: "test" for argument in arguments.get("required", [])}
        variants = {"default": required}
        for argument in arguments.get("optional", []):
            if argument == "version" or argument.endswith("_version"):
                variants[argument] = {**required, argument: "1.2.3"}
        cases[path.relative_to(root).as_posix()] = variants
    return cases


class DownloadTests(unittest.TestCase):
    def test_discovers_new_recipes_and_declared_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recipe = root / "another-platform/features/nested/new-installer.md"
            recipe.parent.mkdir(parents=True)
            recipe.write_text('''```yaml name=config
args:
  required: [account, contact]
  optional: [tool_version, enable_extra]
```
```dockerfile name=main
{% if tool_version %}
RUN wget https://example.invalid/{{ tool_version }}/installer -O installer
{% else %}
RUN curl \\
    --fail https://example.invalid/installer -o installer
{% endif %}
```
''')
            package = root / "download-tools.md"
            package.write_text('''```Dockerfile name=main
RUN apt-get install -y curl \\
    wget
```
Documentation mentions curl --fail https://example.invalid
''')
            expected = {
                "default": {"account": "test", "contact": "test"},
                "tool_version": {"account": "test", "contact": "test", "tool_version": "1.2.3"},
            }
            self.assertEqual(discover_download_cases(root), {recipe.relative_to(root).as_posix(): expected})
            renamed = recipe.with_name("renamed-installer.md")
            recipe.rename(renamed)
            self.assertEqual(discover_download_cases(root), {renamed.relative_to(root).as_posix(): expected})

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
        cases = discover_download_cases(ROOT)
        self.assertTrue(cases, "No download recipes discovered")
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            shutil.copytree(ROOT, work / "modules", ignore=shutil.ignore_patterns(".git", "__pycache__"))
            modules = {f"module-{index}": f"modules/{path}" for index, path in enumerate(cases)}
            outputs = {}
            rendered_cases = {}
            for name, (path, variants) in zip(modules, cases.items()):
                # Local yard modules expect their declared assets beside yard.yaml.
                recipe = ROOT / path
                for asset in module_config(recipe.read_text()).get("files", []):
                    destination = work / asset["path"]
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(recipe.parent / asset["path"], destination)
                for variant, arguments in variants.items():
                    filename = f"{name}-{variant}.Containerfile"
                    outputs[filename] = ["FROM ubuntu:latest", {name: arguments}]
                    rendered_cases[filename] = path
            manifest = {
                "inputs": {"modules": modules},
                "outputs": outputs,
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
            # Architecture detection must succeed before Rustup's download.
            dpkg = commands / "dpkg"
            dpkg.write_text('#!/bin/sh\nprintf "dpkg\\n" >> "$DOWNLOAD_TEST_LOG"\nprintf "amd64\\n"\n')
            dpkg.chmod(0o755)
            temporary_file = commands / "mktemp"
            temporary_file.write_text('#!/bin/sh\nprintf "%s/stub-download\\n" "$HOME"\n')
            temporary_file.chmod(0o755)
            environment = {**os.environ, "PATH": str(commands), "HOME": str(work), "FLUTTER_HOME": str(work / "flutter"), "DOWNLOAD_TEST_LOG": str(log)}
            checked = set()
            for filename, path in rendered_cases.items():
                instructions = run_instructions((work / filename).read_text())
                downloads = [instruction for instruction in instructions if DOWNLOAD.search(instruction)]
                for instruction in downloads:
                    with self.subTest(module=path, output=filename, command=instruction):
                        log.unlink(missing_ok=True)
                        result = subprocess.run(["/bin/sh", "-c", instruction], cwd=work, env=environment, capture_output=True, text=True)
                        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                        executed = log.read_text().splitlines() if log.exists() else []
                        self.assertTrue(set(executed) & {"curl", "wget"}, executed)
                        self.assertIn(executed[-1], {"curl", "wget"}, executed)
                        checked.add(path)
            self.assertEqual(checked, set(cases), "Discovered recipes must reach a download in at least one variant")


if __name__ == "__main__":
    unittest.main()
