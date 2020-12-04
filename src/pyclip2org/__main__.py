"""Command-line interface."""
from pathlib import Path

import click

from pyclip2org import exporter
from pyclip2org import parser


@click.command()
@click.version_option()
@click.option(
    "-o",
    "--output-dir",
    default="/tmp/pyclip2org",
    help="Output directory, '/tmp/pyclip2org' by default",
)
@click.option(
    "-c", "--my-clippings", required=True, help="'My Clippings.txt' file path"
)
@click.option(
    "-l",
    "--language",
    default="en",
    help="'My Clippings.txt' metadata language, (es|en)",
)
def main(my_clippings: str, output_dir: str, language: str) -> None:
    """My Clipping to org-mode notes."""
    directory_path = Path(output_dir)

    if language != "en" and language != "es":
        raise click.UsageError(f"Incorrect language {language}, must be 'en' or 'es'")

    if not directory_path.exists():
        directory_path.mkdir(parents=True)

    if not directory_path.is_dir():
        raise click.UsageError("Output directory is not a folder")

    with open(my_clippings, "r") as file:
        data = file.read()

    library = parser.parser_my_clippings_data(data, language)
    for book in library:
        click.echo(f"Writing {book.title} with {len(book.clippings)} highlights")
        exporter.write_book(book, directory_path)


if __name__ == "__main__":
    main(prog_name="pyclip2org")  # pragma: no cover
