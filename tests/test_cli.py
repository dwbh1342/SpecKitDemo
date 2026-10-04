"""T009, T014, T019 — end-to-end CLI contract (contracts/cli.md)."""

import json

from tests.helpers import TempShelfCase


class US1Cli(TempShelfCase):
    def test_empty_list_message(self):
        r = self.run_cli("list")
        self.assertEqual((r.returncode, r.stdout.strip()), (0, "Your reading list is empty."))

    def test_add_then_list(self):
        r = self.run_cli("add", "Dune", "Frank Herbert")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Added #1: Dune — Frank Herbert", r.stdout)
        r = self.run_cli("list")
        self.assertIn("[to-read]", r.stdout)
        self.assertIn("Dune — Frank Herbert", r.stdout)

    def test_duplicate_is_error_on_stderr(self):
        self.run_cli("add", "Dune", "Frank Herbert")
        r = self.run_cli("add", "dune", "frank herbert")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout, "")
        self.assertIn("already on your list", r.stderr)

    def test_list_json(self):
        self.run_cli("add", "Dune", "Frank Herbert")
        data = json.loads(self.run_cli("list", "--json").stdout)
        self.assertEqual(data[0]["title"], "Dune")

    def test_usage_error_exit_2(self):
        self.assertEqual(self.run_cli("add", "only-title").returncode, 2)


class US2Cli(TempShelfCase):
    def test_finish_and_unread(self):
        self.run_cli("add", "Dune", "Frank Herbert")
        self.run_cli("add", "Kindred", "Octavia E. Butler")
        r = self.run_cli("finish", "1")
        self.assertIn("Finished #1: Dune (2026-10-04)", r.stdout)
        r = self.run_cli("list", "--unread")
        self.assertNotIn("Dune", r.stdout)
        self.assertIn("Kindred", r.stdout)

    def test_finish_twice(self):
        self.run_cli("add", "Dune", "Frank Herbert")
        self.run_cli("finish", "1", today="2026-01-01")
        r = self.run_cli("finish", "1")
        self.assertEqual(r.returncode, 0)
        self.assertIn("already finished on 2026-01-01", r.stdout)

    def test_finish_unknown(self):
        r = self.run_cli("finish", "99")
        self.assertEqual(r.returncode, 1)
        self.assertIn("no book with id 99", r.stderr)


class US3Cli(TempShelfCase):
    def test_default_year_and_json(self):
        self.run_cli("add", "Dune", "Frank Herbert")
        self.run_cli("finish", "1")
        r = self.run_cli("year")
        self.assertIn("Finished in 2026: 1", r.stdout)
        data = json.loads(self.run_cli("year", "2026", "--json").stdout)
        self.assertEqual((data["year"], data["count"]), (2026, 1))

    def test_empty_year(self):
        r = self.run_cli("year", "2024")
        self.assertEqual(r.stdout.strip(), "No books finished in 2024.")
