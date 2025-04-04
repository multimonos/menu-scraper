from enum import Enum
from parse_cmd import parse_cmd
from scrape_cmd import scrape_cmd
from typing import Annotated
import typer
# @see https://playwright.dev/python/docs/api/class-playwright

cli = typer.Typer()


class OutputFormat(str, Enum):
    Text = "text"
    Csv = "csv"


@cli.command()
def parse(
    path: Annotated[str, typer.Argument(help="Path to html file containing menu..")],
    output_format: Annotated[
        OutputFormat,
        typer.Option(
            "--format",
            "-f",
            help="Output format [text,csv]",
        ),
    ] = OutputFormat.Text,
):
    parse_cmd(path, output_format)


@cli.command()
def scrape(
    site_url: Annotated[
        str, typer.Argument(..., help="Url of site to scrape menus from.")
    ],
) -> None:
    scrape_cmd(site_url)


if __name__ == "__main__":
    cli()
