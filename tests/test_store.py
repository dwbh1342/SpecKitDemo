"""T005 — store behaviour (FR-011, FR-012)."""

from datetime import date

from tests.helpers import TempShelfCase
from shelf import service, store


class StoreTests(TempShelfCase):
    def test_missing_file_is_empty_list(self):
        rl = store.load()
        self.assertEqual(rl.next_id, 1)
        self.assertEqual(rl.books, [])

    def test_round_trip(self):
        rl = store.load()
        service.add_book(rl, "Dune", "Frank Herbert", date(2026, 10, 4))
        store.save(rl)
        again = store.load()
        self.assertEqual(again.next_id, 2)
        self.assertEqual(again.books[0].title, "Dune")

    def test_corrupted_file_raises_and_is_untouched(self):
        self.data_file.write_text("{not json", encoding="utf-8")
        with self.assertRaises(store.StoreError):
            store.load()
        self.assertEqual(self.data_file.read_text(encoding="utf-8"), "{not json")
