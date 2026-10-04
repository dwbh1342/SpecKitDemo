"""T022 — SC-002: every command under 1 s with 1,000 books."""

import time
from datetime import date

from tests.helpers import TempShelfCase
from shelf import service, store


class Perf(TempShelfCase):
    def test_thousand_books(self):
        rl = store.load()
        for i in range(1000):
            service.add_book(rl, f"Book {i}", f"Author {i}", date(2026, 1, 1))
        for i in range(1, 501):
            service.finish_book(rl, i, date(2026, 5, 1))
        store.save(rl)
        for args in (["add", "New", "Book"], ["list"], ["finish", "900"], ["year", "2026"]):
            start = time.perf_counter()
            r = self.run_cli(*args)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertLess(time.perf_counter() - start, 1.0, args)
