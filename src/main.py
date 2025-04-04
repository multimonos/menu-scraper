from datetime import datetime
from pathlib import Path
from cmd_batch_merge import batch_merge
from cmd_merge import merge_cmd
from cmd_parse_html import parse_html_cmd
from cmd_scrape import scrape_cmd
from typing import Annotated
import typer

from constants import CSV_ENCODING
# @see https://playwright.dev/python/docs/api/class-playwright

cli = typer.Typer()


@cli.command(help="Scrape page html into files")
def scrape(
    site_url: Annotated[
        str, typer.Argument(..., help="Url of site to scrape menus from.")
    ],
) -> None:
    scrape_cmd(site_url)


@cli.command(help="Parse html to generate an impex csv.")
def parse(
    html_path: Annotated[
        str, typer.Argument(help="Path to html file containing menu..")
    ],
    output: Annotated[
        str | None,
        typer.Option(
            "--output",
            "-o",
            help="Write to file instead of stdout",
        ),
    ] = None,
    validate_output: Annotated[
        bool,
        typer.Option(
            "--validate-output", help="Open the output file and dump to stdout"
        ),
    ] = False,
):
    typer.echo(f"src: {html_path}")
    typer.echo(f"dst: {output if output else 'None'}")
    parse_html_cmd(html_path, output)
    typer.echo(datetime.now().timestamp())

    # open the output file and dump to stdout
    if validate_output and output:
        with open(output, "r", encoding=CSV_ENCODING) as f:
            print(f.read())


@cli.command(help="Merge many csv into one csv")
def merge(
    files: Annotated[
        list[Path],
        typer.Argument(
            ...,
            help="List of CSV file paths",
            exists=True,
            readable=True,
        ),
    ],
    output: Annotated[
        str | None,
        typer.Option(
            "--output",
            "-o",
            help="Write to file instead of stdout",
        ),
    ] = None,
):
    merge_cmd(files, output)


@cli.command(name="merge-batch", help="Batch merge using regex to aggregate files.")
def batch_merge_cmd(
    find: Annotated[str, typer.Option(help="Input file glob.")],
    group_by: Annotated[
        str, typer.Option(help="Regex pattern used to aggregate files.")
    ],
):
    batch_merge(find, group_by)


if __name__ == "__main__":
    cli()
