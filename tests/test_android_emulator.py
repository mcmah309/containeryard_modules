"""Rendering and launcher preflight checks; live boot uses android_emulator_smoke.sh."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "ubuntu/features/android/developer-tools.md"


class AndroidEmulatorTests(unittest.TestCase):
    def test_emulator_remains_optional_and_avd_creation_is_runtime_only(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            shutil.copyfile(MODULE, work / "android.md")
            variants = {
                "default": {},
                "disabled": {"include_emulator": False},
                "enabled": {
                    "include_emulator": True,
                    "platform": "android-36",
                    "build_tools": "36.0.0",
                },
            }
            manifest = {
                "inputs": {"modules": {"android": "android.md"}},
                "outputs": {
                    f"{name}.Containerfile": ["FROM ubuntu:26.04", {"android": args}]
                    for name, args in variants.items()
                },
            }
            (work / "yard.yaml").write_text(json.dumps(manifest))
            result = subprocess.run(
                ["yard", "build", "--ignore-all-requires"],
                cwd=work, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for name in variants:
                with self.subTest(variant=name):
                    rendered = (work / f"{name}.Containerfile").read_text()
                    self.assertEqual("/usr/local/bin/android-emulator" in rendered, name == "enabled")
                    self.assertEqual("libxkbfile1" in rendered, name == "enabled")
                    self.assertNotRegex(rendered, r"(?m)^RUN .*avdmanager create")
            enabled = (work / "enabled.Containerfile").read_text()
            self.assertIn("ARG platform=android-36", enabled)
            self.assertIn("ARG build_tools=36.0.0", enabled)

    def test_launcher_help_and_missing_display_without_sdk_or_kvm(self):
        launcher = re.search(
            r"<<'EMULATOR_LAUNCHER'\n(.*?)\nEMULATOR_LAUNCHER",
            MODULE.read_text(), re.DOTALL,
        )[1]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "android-emulator"
            path.write_text(launcher)
            path.chmod(0o755)
            environment = {"PATH": os.environ["PATH"], "HOME": directory}
            syntax = subprocess.run(["/bin/sh", "-n", str(path)], capture_output=True, text=True)
            self.assertEqual(syntax.returncode, 0, syntax.stderr)
            help_result = subprocess.run(
                [str(path), "--help"], env=environment, capture_output=True, text=True,
            )
            self.assertEqual(help_result.returncode, 0, help_result.stderr)
            self.assertIn("--device /dev/kvm", help_result.stdout)
            window = subprocess.run(
                [str(path), "--window"], env=environment, capture_output=True, text=True,
            )
            self.assertNotEqual(window.returncode, 0)
            self.assertIn("window mode requires DISPLAY", window.stderr)


if __name__ == "__main__":
    unittest.main()
