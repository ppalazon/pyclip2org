"""Testing exporting."""


from pyclip2org.parser import Book, Clipping
from pyclip2org import exporter
from pathlib import Path
import random
import string


def test_export_empty_book() -> None:
    """Write empty book."""
    book = Book("", "Author 1")

    output_random = "".join(random.choice(string.hexdigits) for i in range(7))
    output = Path(output_random)

    # with open(f'/tmp/{output_random}', 'w') as file:
    #     file.write('This is a test')

    exporter.write_book(book, output)

    assert not output.exists()


def test_export_empty_clippings() -> None:
    """Write book with no clippings."""
    book = Book("Test", "Author 1")

    output_random = "".join(random.choice(string.hexdigits) for i in range(7))
    output = Path("/tmp") / output_random

    # with open(f'/tmp/{output_random}', 'w') as file:
    #     file.write('This is a test')

    exporter.write_book(book, output)

    fo = output / "test.org"

    assert not fo.exists()


def test_export_empty_output() -> None:
    """Fail empty folder."""
    book = Book("Test", "Author 1")
    clipping = Clipping("Test", "Test", "Test", "Test")
    book.add_clipping(clipping)

    output_random = "".join(random.choice(string.hexdigits) for i in range(7))
    output = Path("/tmp") / output_random

    # with open(f'/tmp/{output_random}', 'w') as file:
    #     file.write('This is a test')

    exporter.write_book(book, output)

    fo = output / "test.org"

    assert not fo.exists()


def test_export_incorrect_output() -> None:
    """Fail incorrect output."""
    book = Book("Test", "Author 1")
    clipping = Clipping("Test", "Test", "Test", "Test")
    book.add_clipping(clipping)

    output_random = "".join(random.choice(string.hexdigits) for i in range(7))
    output = Path("/tmp") / output_random

    with output.open('w') as file:
        file.write('This is a test')

    exporter.write_book(book, output)

    fo = output / "test.org"

    assert not fo.exists()


def test_export_basic_book() -> None:
    """Write basic book."""
    book = Book("Test", "Author 1")
    clipping = Clipping("Test", "Test", "Test", "Test")
    book.add_clipping(clipping)

    output_random = "".join(random.choice(string.hexdigits) for i in range(7))
    output = Path("/tmp") / output_random

    output.mkdir(parents=True)

    exporter.write_book(book, output)

    fo = output / "test.org"

    assert fo.exists()
