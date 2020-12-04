"""Testing exporting."""
import os
import secrets
import string
import tempfile
from pathlib import Path
from typing import Any

from pyclip2org import exporter
from pyclip2org.parser import Book
from pyclip2org.parser import Clipping


def get_tmp_path_dir() -> Any:
    """Generate a random path."""
    output_random = os.path.join(
        tempfile.gettempdir(),
        "".join(secrets.choice(string.hexdigits) for i in range(7)),
    )
    return Path(output_random)


def test_export_empty_book() -> None:
    """Write empty book."""
    book = Book("", "Author 1")

    output = get_tmp_path_dir()

    # with open(f'/tmp/{output_random}', 'w') as file:
    #     file.write('This is a test')

    exporter.write_book(book, output)

    assert not output.exists()


def test_export_empty_clippings() -> None:
    """Write book with no clippings."""
    book = Book("Test", "Author 1")

    output = get_tmp_path_dir()

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

    output = get_tmp_path_dir()

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

    output = get_tmp_path_dir()

    with output.open("w") as file:
        file.write("This is a test")

    exporter.write_book(book, output)

    fo = output / "test.org"

    assert not fo.exists()


def test_export_basic_book() -> None:
    """Write basic book."""
    book = Book("Test", "Author 1")
    clipping = Clipping("Test", "Test", "Test", "Test")
    book.add_clipping(clipping)

    output = get_tmp_path_dir()

    output.mkdir(parents=True)

    exporter.write_book(book, output)

    fo = output / "test.org"

    assert fo.exists()
