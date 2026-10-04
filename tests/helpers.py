"""Shared test helpers: isolate every test in its own SHELF_FILE."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class TempShelfCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.data_file = Path(self._tmp.name) / "shelf.json"
        self._old = os.environ.get("SHELF_FILE")
        os.environ["SHELF_FILE"] = str(self.data_file)

    def tearDown(self):
        if self._old is None:
            os.environ.pop("SHELF_FILE", None)
        else:
            os.environ["SHELF_FILE"] = self._old
        self._tmp.cleanup()

    def run_cli(self, *args, today="2026-10-04"):
        env = {**os.environ, "SHELF_FILE": str(self.data_file), "PYTHONPATH": str(SRC), "SHELF_TODAY": today}
        return subprocess.run(
            [sys.executable, "-m", "shelf", *args], capture_output=True, text=True, env=env
        )
