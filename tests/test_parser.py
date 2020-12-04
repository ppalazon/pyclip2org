"""Testing parser.py module."""
from pyclip2org import parser
from pyclip2org.parser import Book
from pyclip2org.parser import Clipping


def test_book_add_none_clipping() -> None:
    """Add none as clipping."""
    book = Book("Test", "Author")
    book.add_clipping(None)

    assert len(book.clippings) == 0
    assert str(book) == "Title:Test\tAuthor:Author\tClippings:0"


def test_clipping_head() -> None:
    """Add none as clipping."""
    clipping = Clipping(
        "Test",
        "Author",
        "- Mi nota Posición 128 | Añadido el miércoles 6 de febrero de 2013, 13:00:19",
        "Magni iste minus vitae, laudantium vero laborum obcaecati recusandae ipsum?",
    )

    assert (
        clipping.get_header()
        == "** Mi nota Posición 128 | Añadido el miércoles 6 de febrero de 2013, 13:00:19"
    )
    assert (
        clipping.get_wrap_content()
        == "Magni iste minus vitae, laudantium vero laborum obcaecati recusandae ipsum?"
    )


def test_parse_bad_clipping_size() -> None:
    """Testing a bad clipping format."""
    raw_string = """Book 2 (Spanish Edition) (Author 2)
- Your Bookmark on Location 1012 | Added on Saturday, February 9, 2013 10:40:33"""

    clipping = Clipping.parse_single_highlight(raw_string)

    assert clipping is None


def test_parse_bad_clipping_author() -> None:
    """Testing a bad clipping format."""
    raw_string = """Book 2
- Your Highlight on Location 1012 | Added on Saturday, February 9, 2013 10:40:33

Testing"""

    clipping = Clipping.parse_single_highlight(raw_string)

    assert clipping is None


def test_parse_bad_clipping_title() -> None:
    """Testing a bad clipping format."""
    raw_string = """(Book 2)
- Your Highlight on Location 1012 | Added on Saturday, February 9, 2013 10:40:33

Testing"""

    clipping = Clipping.parse_single_highlight(raw_string)

    assert clipping is None


def test_parse_multiple_books_es() -> None:
    """Testing multiple clippings in Spanish."""
    raw_data = """Book 1 (Author 1)
- Mi nota Posición 128 | Añadido el miércoles 6 de febrero de 2013, 13:00:19

Magni iste minus vitae, laudantium vero laborum obcaecati recusandae ipsum?
==========
Book 1 (Author 1)
- Tu subrayado en la página 23 | Posición 2015-2065 | Añadido el lunes, 4 de \\
agosto de 2014 19:52:23

Delectus hic ipsam iure quae exercitationem distinctio voluptatem.
==========
Book 2 (Spanish Edition) (Author 2)
- Mi marcador Posición 1012 | Añadido el sábado 9 de febrero de 2013, 10:40:33


=========="""

    library = parser.parser_my_clippings_data(raw_data, "es")

    assert len(library) == 2
    assert len(library[0].get_highlights()) == 1
    assert len(library[0].get_notes()) == 1
    assert len(library[0].get_marks()) == 0
    assert len(library[1].get_highlights()) == 0
    assert len(library[1].get_notes()) == 0
    assert len(library[1].get_marks()) == 1


def test_parse_single_note_es() -> None:
    """Testing single note in Spanish."""
    raw_string = """Book 1 (Author 1)
- Mi nota Posición 128 | Añadido el miércoles 6 de febrero de 2013, 13:00:19

Magni iste minus vitae, laudantium vero laborum obcaecati recusandae ipsum?"""

    clipping = Clipping.parse_single_highlight(raw_string)

    assert clipping is not None
    assert clipping.title == "Book 1"
    assert clipping.author == "Author 1"
    assert (
        clipping.metadata
        == "- Mi nota Posición 128 | Añadido el miércoles 6 de febrero de 2013, 13:00:19"
    )
    assert (
        clipping.content
        == "Magni iste minus vitae, laudantium vero laborum obcaecati recusandae ipsum?"
    )

    clipping.parse_metadata("es")

    assert clipping.position_start == 128
    assert clipping.type == "NOTE"


def test_parse_single_highlight_es() -> None:
    """Testing single highlight in spanish."""
    raw_string = """Book 2 (Spanish Edition) (Author 2)
- Tu subrayado en la página 23 | Posición 2015-2065 | Añadido el lunes, 4 de agosto de 2014 19:52:23

Omnis animi sunt praesentium beatae fugiat, sequi hic debitis deleniti eum, ad eaque dignissimos"""

    clipping = Clipping.parse_single_highlight(raw_string)

    assert clipping is not None
    assert clipping.title == "Book 2 (Spanish Edition)"
    assert clipping.author == "Author 2"
    assert (
        clipping.metadata
        == "- Tu subrayado en la página 23 | Posición 2015-2065 | Añadido el lunes, 4 de agosto de 2014 19:52:23"
    )
    assert (
        clipping.content
        == "Omnis animi sunt praesentium beatae fugiat, sequi hic debitis deleniti eum, ad eaque dignissimos"
    )

    clipping.parse_metadata("es")

    assert clipping.position_start == 2015
    assert clipping.position_end == 2065
    assert clipping.page == 23
    assert clipping.type == "HIGHLIGHT"


def test_parse_single_mark_es() -> None:
    """Testing single mark in Spanish."""
    raw_string = """Book 2 (Spanish Edition) (Author 2)
- Mi marcador Posición 1012 | Añadido el sábado 9 de febrero de 2013, 10:40:33

"""

    clipping = Clipping.parse_single_highlight(raw_string)

    assert clipping is not None
    assert clipping.title == "Book 2 (Spanish Edition)"
    assert clipping.author == "Author 2"
    assert (
        clipping.metadata
        == "- Mi marcador Posición 1012 | Añadido el sábado 9 de febrero de 2013, 10:40:33"
    )
    assert clipping.content == ""

    clipping.parse_metadata("es")

    assert clipping.position_start == 1012
    assert clipping.type == "MARK"


def test_parse_multiple_books_en() -> None:
    """Testing multiples clippings in English."""
    raw_data = """Book 1 (Author 1)
- Your note on Location 128 | Added on Wednesday, February 6, 2013 13:00:19

Magni iste minus vitae, laudantium vero laborum obcaecati recusandae ipsum?
==========
Book 1 (Author 1)
- Your Highlight on Page 73 | Location 1111-1111 | Added on Saturday, November 15, 2014 11:00:28

Delectus hic ipsam iure quae exercitationem distinctio voluptatem autem aliquam assumenda reiciendis.
==========
Book 2 (Spanish Edition) (Author 2)
- Your Bookmark on Location 1012 | Added on Saturday, February 9, 2013 10:40:33


=========="""

    library = parser.parser_my_clippings_data(raw_data, "en")

    assert len(library) == 2
    assert len(library[0].get_highlights()) == 1
    assert len(library[0].get_notes()) == 1
    assert len(library[0].get_marks()) == 0
    assert len(library[1].get_highlights()) == 0
    assert len(library[1].get_notes()) == 0
    assert len(library[1].get_marks()) == 1


def test_parse_multiple_books_wrong_language() -> None:
    """Testing multiples clippings in English."""
    raw_data = """Book 1 (Author 1)
- Your note on Location 128 | Added on Wednesday, February 6, 2013 13:00:19

Magni iste minus vitae, laudantium vero laborum obcaecati recusandae ipsum?
==========
Book 1 (Author 1)
- Your Highlight on Page 73 | Location 1111-1111 | Added on Saturday, November 15, 2014 11:00:28

Delectus hic ipsam iure quae exercitationem distinctio voluptatem autem aliquam assumenda reiciendis.
==========
Book 2 (Spanish Edition) (Author 2)
- Your Bookmark on Location 1012 | Added on Saturday, February 9, 2013 10:40:33


=========="""

    library = parser.parser_my_clippings_data(raw_data, "es")

    assert len(library) == 2
    assert len(library[0].get_highlights()) == 0
    assert len(library[0].get_notes()) == 0
    assert len(library[0].get_marks()) == 0
    assert len(library[1].get_highlights()) == 0
    assert len(library[1].get_notes()) == 0
    assert len(library[1].get_marks()) == 0


def test_parse_single_note_en() -> None:
    """Testing a single note in English."""
    raw_string = """Book 1 (Author 1)
- Your note on Location 128 | Added on Wednesday, February 6, 2013 13:00:19

Magni iste minus vitae, laudantium vero laborum obcaecati recusandae ipsum?"""

    clipping = Clipping.parse_single_highlight(raw_string)

    assert clipping is not None
    assert clipping.title == "Book 1"
    assert clipping.author == "Author 1"
    assert (
        clipping.metadata
        == "- Your note on Location 128 | Added on Wednesday, February 6, 2013 13:00:19"
    )
    assert (
        clipping.content
        == "Magni iste minus vitae, laudantium vero laborum obcaecati recusandae ipsum?"
    )

    clipping.parse_metadata("en")

    assert clipping.position_start == 128
    assert clipping.type == "NOTE"


def test_parse_single_highlight_en() -> None:
    """Testing a single highlight in English."""
    raw_string = """Book 2 (Spanish Edition) (Author 2)
- Your Highlight on Page 104 | Location 1581-1586 | Added on Thuesday, February 7, 2013 15:54:12

Omnis animi sunt praesentium beatae fugiat, sequi hic debitis deleniti eum, ad eaque dignissimos"""

    clipping = Clipping.parse_single_highlight(raw_string)

    assert clipping is not None
    assert clipping.title == "Book 2 (Spanish Edition)"
    assert clipping.author == "Author 2"
    assert (
        clipping.metadata
        == "- Your Highlight on Page 104 | Location 1581-1586 | Added on Thuesday, February 7, 2013 15:54:12"
    )
    assert (
        clipping.content
        == "Omnis animi sunt praesentium beatae fugiat, sequi hic debitis deleniti eum, ad eaque dignissimos"
    )

    clipping.parse_metadata("en")

    assert clipping.position_start == 1581
    assert clipping.position_end == 1586
    assert clipping.page == 104
    assert clipping.type == "HIGHLIGHT"


def test_parse_single_mark_en() -> None:
    """Testing a single bookmark in English."""
    raw_string = """Book 2 (Spanish Edition) (Author 2)
- Your Bookmark on Location 1012 | Added on Saturday, February 9, 2013 10:40:33

"""

    clipping = Clipping.parse_single_highlight(raw_string)

    assert clipping is not None
    assert clipping.title == "Book 2 (Spanish Edition)"
    assert clipping.author == "Author 2"
    assert (
        clipping.metadata
        == "- Your Bookmark on Location 1012 | Added on Saturday, February 9, 2013 10:40:33"
    )
    assert clipping.content == ""

    clipping.parse_metadata("en")

    assert clipping.position_start == 1012
    assert clipping.type == "MARK"


def test_parse_single_note_en_incomplete() -> None:
    """Testing a single note in English."""
    raw_string = """Book 1 (Author 1)
- Your note on

Magni iste minus vitae, laudantium vero laborum obcaecati recusandae ipsum?"""

    clipping = Clipping.parse_single_highlight(raw_string)

    assert clipping is not None
    assert clipping.title == "Book 1"
    assert clipping.author == "Author 1"
    assert clipping.metadata == "- Your note on"
    assert (
        clipping.content
        == "Magni iste minus vitae, laudantium vero laborum obcaecati recusandae ipsum?"
    )

    clipping.parse_metadata("en")

    assert clipping.position_start == -1
    assert clipping.type == "NOTE"


def test_parse_single_highlight_en_incomplete() -> None:
    """Testing a single highlight in English."""
    raw_string = """Book 2 (Spanish Edition) (Author 2)
- Your Highlight on

Omnis animi sunt praesentium beatae fugiat, sequi hic debitis deleniti eum, ad eaque dignissimos"""

    clipping = Clipping.parse_single_highlight(raw_string)

    assert clipping is not None
    assert clipping.title == "Book 2 (Spanish Edition)"
    assert clipping.author == "Author 2"
    assert clipping.metadata == "- Your Highlight on"
    assert (
        clipping.content
        == "Omnis animi sunt praesentium beatae fugiat, sequi hic debitis deleniti eum, ad eaque dignissimos"
    )

    clipping.parse_metadata("en")

    assert clipping.position_start == -1
    assert clipping.position_end == -1
    assert clipping.page == -1
    assert clipping.type == "HIGHLIGHT"


def test_parse_single_mark_en_incomplete() -> None:
    """Testing a single bookmark in English."""
    raw_string = """Book 2 (Spanish Edition) (Author 2)
- Your Bookmark on

"""

    clipping = Clipping.parse_single_highlight(raw_string)

    assert clipping is not None
    assert clipping.title == "Book 2 (Spanish Edition)"
    assert clipping.author == "Author 2"
    assert clipping.metadata == "- Your Bookmark on"
    assert clipping.content == ""

    clipping.parse_metadata("en")

    assert clipping.position_start == -1
    assert clipping.type == "MARK"
