import glob
import os
import typer
import re
from constants import CSV_ENCODING


def batch_merge(find: str, group_by: str) -> None:
    typer.echo(f"find: {find}")
    typer.echo(f"group_by: {group_by}")

    pattern = re.compile(group_by)
    files = glob.glob(find)
    groups: dict[str, list[str]] = {}
    ofiles: dict[str, str] = {}

    # group files
    for file in files:
        match = pattern.match(file)
        dirname = os.path.dirname(file)

        if match:
            key = match.group(1)
            groups.setdefault(key, []).append(file)
            ofiles[key] = f"{dirname}/merged_{key}.csv"

    # merge
    for k, group in groups.items():
        typer.echo(f"G {k}")
        items = sorted(list(group))
        ofile = ofiles[k]
        linecount = 0

        output = ""
        for file in items:
            with open(file, "r", encoding=CSV_ENCODING) as f:
                content = f.read()
                count = len(content.splitlines())
                linecount += count
                typer.echo(f"- {str(count).rjust(4)} | {file}")
                output += content
        typer.echo(f"= {str(linecount).rjust(4)} | lines")

        with open(ofile, "w", encoding=CSV_ENCODING) as o:
            count = len(output.splitlines())
            o.write(output)
            typer.echo(f"+ {str(count).rjust(4)} | {ofile}")
