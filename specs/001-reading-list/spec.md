# Feature Specification: Reading List Tracker

**Feature Branch**: `001-reading-list`

**Created**: 2026-10-04

**Status**: Ready for planning

**Input**: User description: "Build a reading list tool I can use from the terminal. I can add books I want to read with a title and author, see what's on my list, and mark a book as finished. I'd also like to see what I've finished in a given year."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add and list books (Priority: P1)

A reader adds books they intend to read, giving a title and an author, and can see their list at any time.

**Why this priority**: Capturing and viewing the list is the core value. Without it nothing else matters, and on its own it already replaces a sticky note.

**Independent Test**: Add two books, list them, and confirm both appear with their titles, authors, and an identifier the reader can refer to later.

**Acceptance Scenarios**:

1. **Given** an empty list, **When** the reader adds "Dune" by "Frank Herbert", **Then** the tool confirms the addition and shows the identifier assigned to the book.
2. **Given** a list with two unread books, **When** the reader lists books, **Then** both books are shown in the order they were added, each with identifier, title, author, and status "to-read".
3. **Given** an empty list, **When** the reader lists books, **Then** the tool says the list is empty rather than showing nothing.
4. **Given** "Dune" by "Frank Herbert" is already on the list, **When** the reader adds it again (ignoring letter case), **Then** the tool refuses and explains that the book is already on the list.

---

### User Story 2 - Mark a book as finished (Priority: P2)

A reader who finishes a book marks it as finished so the list reflects what is still left to read.

**Why this priority**: Turns the list from a capture tool into a progress tracker. Depends on books existing (US1) but is testable on its own once a book is added.

**Independent Test**: Add a book, mark it finished, list books, and confirm its status is "finished" with the date it was finished.

**Acceptance Scenarios**:

1. **Given** an unread book with identifier 1, **When** the reader marks book 1 as finished, **Then** its status becomes "finished" and today's date is recorded as the finish date.
2. **Given** a list with finished and unread books, **When** the reader lists only unread books, **Then** finished books are not shown.
3. **Given** no book with identifier 99, **When** the reader marks book 99 as finished, **Then** the tool reports that no such book exists and nothing changes.
4. **Given** book 1 is already finished, **When** the reader marks it finished again, **Then** the tool says it is already finished and keeps the original finish date.

---

### User Story 3 - Year in review (Priority: P3)

A reader sees which books they finished in a given year and how many, defaulting to the current year.

**Why this priority**: A motivating summary, but the tool is fully useful without it.

**Independent Test**: With books finished in two different years, request the summary for one year and confirm only that year's books and the correct count are shown.

**Acceptance Scenarios**:

1. **Given** three books finished in 2026 and one in 2025, **When** the reader requests the summary for 2026, **Then** the three 2026 books are shown with their finish dates, and the total reads 3.
2. **Given** no year is specified, **When** the reader requests the summary, **Then** the current calendar year is used.
3. **Given** no books were finished in 2024, **When** the reader requests the summary for 2024, **Then** the tool says no books were finished that year.

---

### Edge Cases

- Title or author is empty or only whitespace → the book is rejected with a clear message.
- Leading/trailing whitespace in title or author is trimmed before saving and before duplicate checks.
- The data file does not exist yet → it is treated as an empty list and created on the first write.
- The data file exists but is unreadable or corrupted → the tool reports the problem and does not overwrite the file.
- Identifiers are never reused, even if books are later removed by a future feature.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Users MUST be able to add a book with a title and an author.
- **FR-002**: The system MUST assign each book a unique, never-reused numeric identifier shown on add and on list.
- **FR-003**: The system MUST reject a book whose title or author is empty after trimming whitespace.
- **FR-004**: The system MUST reject a book whose title and author both match an existing book, ignoring letter case and surrounding whitespace.
- **FR-005**: Users MUST be able to list all books in the order added, showing identifier, title, author, and status.
- **FR-006**: Users MUST be able to list only unread books.
- **FR-007**: Users MUST be able to mark a book as finished by identifier; the system MUST record the date it was marked.
- **FR-008**: Marking an already-finished book MUST NOT change its recorded finish date.
- **FR-009**: Users MUST be able to see the books finished in a given calendar year, with a count, defaulting to the current year.
- **FR-010**: Every command that returns data MUST also be available in a machine-readable format.
- **FR-011**: The reading list MUST persist between uses on the same machine.
- **FR-012**: The system MUST NOT overwrite or lose existing data when the stored list cannot be read.

### Key Entities

- **Book**: Something the reader intends to read or has read. Has an identifier, title, author, status (to-read or finished), the date it was added, and the date it was finished (only when finished).
- **Reading List**: The reader's whole collection of books plus the next identifier to assign.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A first-time user can add a book and see it in their list within 1 minute using only the built-in help.
- **SC-002**: Every command responds in under 1 second for a list of 1,000 books.
- **SC-003**: 100% of acceptance scenarios above are covered by automated tests that pass.
- **SC-004**: No data is lost when the tool is interrupted mid-save (the list is either the old version or the new version, never partial).

## Assumptions

- Single user on a single machine; no syncing or sharing in this feature.
- "Finished" is recorded as a calendar date (no time of day); the reader's local date is used.
- Removing or editing books is out of scope for this feature and will be specified separately.
- Year-in-review uses calendar years (January–December), not rolling 12 months.
