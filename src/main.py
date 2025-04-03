from parse_cmd import parse_cmd
from scrape_cmd import scrape_cmd
from typing import Annotated
import typer
# @see https://playwright.dev/python/docs/api/class-playwright

cli = typer.Typer()


@cli.command()
def parse(
    html_file: Annotated[
        str, typer.Argument(..., help="Path to html file containing menu..")
    ],
):
    parse_cmd(html_file)


@cli.command()
def scrape(
    site_url: Annotated[
        str, typer.Argument(..., help="Url of site to scrape menus from.")
    ],
) -> None:
    scrape_cmd(site_url)


if __name__ == "__main__":
    cli()
