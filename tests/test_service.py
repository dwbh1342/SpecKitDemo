"""T008, T013, T018 — acceptance scenarios at the service layer."""

import unittest
from datetime import date

import tests.helpers  # noqa: F401  (puts src/ on sys.path)
from shelf import service
from shelf.models import FINISHED, TO_READ, ReadingList

D = date(2026, 10, 4)


class US1AddAndList(unittest.TestCase):
    def test_ac1_add_assigns_id(self):
        rl = ReadingList()
        book = service.add_book(rl, "Dune", "Frank Herbert", D)
        self.assertEqual(book.id, 1)

    def test_ac2_list_in_order_with_status(self):
        rl = ReadingList()
        service.add_book(rl, "Dune", "Frank Herbert", D)
        service.add_book(rl, "Kindred", "Octavia E. Butler", D)
        books = service.list_books(rl)
        self.assertEqual([b.title for b in books], ["Dune", "Kindred"])
        self.assertTrue(all(b.status == TO_READ for b in books))

    def test_ac3_empty_list(self):
        self.assertEqual(service.list_books(ReadingList()), [])

    def test_ac4_duplicate_ignoring_case(self):
        rl = ReadingList()
        service.add_book(rl, "Dune", "Frank Herbert", D)
        with self.assertRaises(service.ShelfError):
            service.add_book(rl, "dune", "FRANK HERBERT", D)

    def test_fr003_blank_title_or_author_rejected(self):
        rl = ReadingList()
        for title, author in [("", "x"), ("x", "   "), ("  ", "  ")]:
            with self.assertRaises(service.ShelfError):
                service.add_book(rl, title, author, D)

    def test_edge_whitespace_trimmed(self):
        rl = ReadingList()
        book = service.add_book(rl, "  Dune ", " Frank Herbert  ", D)
        self.assertEqual((book.title, book.author), ("Dune", "Frank Herbert"))

    def test_fr002_ids_not_reused(self):
        rl = ReadingList()
        service.add_book(rl, "A", "a", D)
        service.add_book(rl, "B", "b", D)
        rl.books.pop()  # simulate a future delete
        self.assertEqual(service.add_book(rl, "C", "c", D).id, 3)


class US2Finish(unittest.TestCase):
    def setUp(self):
        self.rl = ReadingList()
        service.add_book(self.rl, "Dune", "Frank Herbert", D)
        service.add_book(self.rl, "Kindred", "Octavia E. Butler", D)

    def test_ac1_finish_records_date(self):
        r = service.finish_book(self.rl, 1, D)
        self.assertEqual((r.book.status, r.book.finished_on), (FINISHED, "2026-10-04"))

    def test_ac2_unread_filter(self):
        service.finish_book(self.rl, 1, D)
        self.assertEqual([b.id for b in service.list_books(self.rl, unread_only=True)], [2])

    def test_ac3_unknown_id(self):
        with self.assertRaises(service.ShelfError):
            service.finish_book(self.rl, 99, D)

    def test_ac4_finish_twice_keeps_date(self):
        service.finish_book(self.rl, 1, date(2026, 1, 1))
        r = service.finish_book(self.rl, 1, D)
        self.assertTrue(r.already_finished)
        self.assertEqual(r.book.finished_on, "2026-01-01")


class US3YearInReview(unittest.TestCase):
    def setUp(self):
        self.rl = ReadingList()
        for i, d in enumerate([date(2026, 6, 30), date(2026, 2, 11), date(2025, 12, 31), date(2026, 10, 4)]):
            service.add_book(self.rl, f"Book {i}", "Author", D)
            service.finish_book(self.rl, i + 1, d)
        service.add_book(self.rl, "Unread", "Author", D)

    def test_ac1_year_filter_count_and_order(self):
        books = service.year_summary(self.rl, 2026)
        self.assertEqual(len(books), 3)
        self.assertEqual([b.finished_on for b in books], ["2026-02-11", "2026-06-30", "2026-10-04"])

    def test_ac3_no_books_that_year(self):
        self.assertEqual(service.year_summary(self.rl, 2024), [])


if __name__ == "__main__":
    unittest.main()
