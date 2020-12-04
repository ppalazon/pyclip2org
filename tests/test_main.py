"""Test cases for the __main__ module."""
import string

import pytest
import secrets
from click.testing import CliRunner

from pyclip2org import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeed_en(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main, "-c tests/clippings-en.txt")
    assert result.exit_code == 0


def test_main_succeed_es(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main, "-c tests/clippings-es.txt -l es")
    assert result.exit_code == 0


def test_main_random_output(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    output_random = "".join(secrets.choice(string.hexdigits) for i in range(7))
    result = runner.invoke(
        __main__.main, f"-c tests/clippings-es.txt -o /tmp/{output_random}"
    )
    assert result.exit_code == 0


def test_main_error_output(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    output_random = "".join(secrets.choice(string.hexdigits) for i in range(7))

    with open(f"/tmp/{output_random}", "w") as file:
        file.write("This is a test")

    result = runner.invoke(
        __main__.main, f"-c tests/clippings-es.txt -o /tmp/{output_random}"
    )
    assert result.exit_code != 0


def test_main_incorrect_lang(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main, "-c tests/clippings-es.txt -l invented")
    assert result.exit_code != 0


def test_main_fail_no_arguments(runner: CliRunner) -> None:
    """It exits with a status code of non zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code != 0
