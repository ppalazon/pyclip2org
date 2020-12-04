"""Exporter module for books and clippings."""
from typing import Any

from slugify import slugify


def write_book(book: Any, directory: Any) -> None:
    """Write all clippings in a file within the output folder."""
    if not book.title or len(book.clippings) == 0:
        print(f"Not writting {book.title} because name is {len(book.clippings)}")
        return None
    clean_title = "".join(
        [c for c in book.title if c.isalpha() or c.isdigit() or c == " "]
    ).rstrip()

    book.clippings.sort(
        key=lambda h: h.position_start if h.position_start else h.page if h.page else 0
    )

    if not directory.is_dir():
        return None

    path_file = directory / f"{slugify(clean_title)}.org"
    with path_file.open(mode="w") as file:
        file.write(f"#+title: {clean_title}\n")
        file.write(f"#+author: {book.author}\n")
        file.write("\n")

        notes = book.get_notes()
        if len(notes) > 0:
            file.write("* Notes")
            file.write("\n")
            for h in notes:
                file.write(f"\n{h.get_header()}\n")
                file.write(f"\n{h.get_wrap_content()}\n")

        marks = book.get_marks()
        if len(marks) > 0:
            file.write("* Bookmarks")
            file.write("\n")
            for h in marks:
                file.write(f"\n{h.get_header()}\n")

        highlights = book.get_highlights()
        if len(highlights) > 0:
            file.write("* Highlights")
            file.write("\n")
            for h in highlights:
                file.write(f"\n{h.get_header()}\n")
                file.write(
                    f"\n#+caption: {clean_title} \
                    ({book.author}) in position {h.position_start}\n"
                )
                file.write("#+begin_quote\n")
                file.write(h.get_wrap_content())
                file.write("\n#+end_quote\n")

        file.close()
