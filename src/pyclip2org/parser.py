"""Parse My Clippings highlights from kindle."""
import re
from typing import Any
from typing import List

from textwrap3 import wrap

# import dateparser


regexp_author = re.compile(r"\((.*?)\)", re.IGNORECASE)
regexp_page = re.compile(r"Página ([0-9]+)", re.IGNORECASE)
regexp_position_high = re.compile(r"Posición ([0-9]+)-([0-9]+)", re.IGNORECASE)
regexp_position_note = re.compile(r"Posición ([0-9]+)", re.IGNORECASE)
regexp_date = re.compile(r"Añadido el\s+(.+)$", re.IGNORECASE)


class Book:
    """Book information with a list of clippings."""

    def __init__(self, title: str, author: str) -> None:
        """Basic initialization of a Book."""
        self.author = author
        self.title = title
        self.clippings: List[Any] = []

    def add_clipping(self, clipping: Any) -> None:
        """Add a clipping to this list."""
        if clipping and clipping.content:
            self.clippings.append(clipping)

    def get_hightlights(self) -> List[Any]:
        """Get all hightlights of the book."""
        return [m for m in self.clippings if m.type == "HIGHLIGHT"]

    def get_marks(self) -> List[Any]:
        """Get all marks of the book."""
        return [m for m in self.clippings if m.type == "MARK"]

    def get_notes(self) -> List[Any]:
        """Get all notes of the book."""
        return [m for m in self.clippings if m.type == "NOTE"]

    def __str__(self) -> str:
        """Generate a string representation."""
        return (
            f"Title:{self.title}\tAuthor:{self.author}\tClippings:{len(self.clippings)}"
        )


class Clipping:
    """Information about a single clipping."""

    def __init__(self, title: str, author: str, metadata: str, content: str) -> None:
        """Basic initialization for a clipping."""
        self.title = title
        self.author = author
        self.metadata = metadata
        self.content = content

    def get_header(self) -> str:
        """Get a header for the clipping."""
        return self.metadata.replace("- ", "** ")

    def get_wrap_content(self) -> str:
        """Get a word wrap text from content."""
        clean_text = self.content.replace("\n", " ")
        return "\n".join(wrap(clean_text, 80))

    def parse_metadata(self, language: str) -> None:
        """Extract information from metadata line."""
        if self.metadata:
            if re.search("subrayado", self.metadata, re.IGNORECASE):
                self.type = "HIGHLIGHT"
                match_page = regexp_page.search(self.metadata)
                if match_page:
                    self.page = int(match_page.group(1))
                match_position = regexp_position_high.search(self.metadata)
                if match_position:
                    self.position_start = int(match_position.group(1))
                    self.position_end = int(match_position.group(2))
            if re.search("nota", self.metadata, re.IGNORECASE):
                self.type = "NOTE"
                match_position = regexp_position_note.search(self.metadata)
                if match_position:
                    self.position_start = int(match_position.group(1))
            if re.search("marcador", self.metadata, re.IGNORECASE):
                self.type = "MARK"
                match_position = regexp_position_note.search(self.metadata)
                if match_position:
                    self.position_start = int(match_position.group(1))
            # match_date = regexp_date.search(metadata)
            # if match_date:
            #     h.date = dateparser.parse(match_date.group(1))

    @classmethod
    def parse_single_highlight(cls, highlight_string: str) -> Any:
        """Parse a single clipping."""
        splitted_string = highlight_string.split("\n")
        if len(splitted_string) != 4:
            return None
        author_line = splitted_string[0]
        metadata = splitted_string[1]
        content = splitted_string[3]
        # regex = r"\((.*?)\)"
        # Solving problems with titles with parenthesis
        match_author = regexp_author.findall(author_line)
        if len(match_author) == 0:
            return None
        for a in match_author:
            author = a
            title = author_line.replace(f"({a})", "").strip()
        return Clipping(title, author, metadata, content)


def parser_my_clippings_data(my_clipping_data: str, language: str) -> List[Any]:
    """Parser 'My Clippings.txt' data."""
    clipping_separator = "\n==========\n"

    clippings = my_clipping_data.split(clipping_separator)

    book_title_list = []
    library = []
    for raw_string in clippings:
        clipping = Clipping.parse_single_highlight(raw_string)

        if not clipping:
            continue

        clipping.parse_metadata(language)
        if clipping.title not in book_title_list:
            book = Book(clipping.title, clipping.author)
            book.add_clipping(clipping)
            book_title_list.append(clipping.title)
            library.append(book)
        else:
            for book in library:
                if book.title == clipping.title:
                    book.add_clipping(clipping)

    return library
