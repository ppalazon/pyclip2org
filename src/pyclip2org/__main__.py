"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """My Clipping to org-mode notes."""


if __name__ == "__main__":
    main(prog_name="pyclip2org")  # pragma: no cover
