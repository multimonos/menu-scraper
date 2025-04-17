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

    # merge files by grouping
    for k, group in groups.items():
        typer.echo(f"G {k}")
        sources = sorted(list(group))
        ofile = ofiles[k]
        linecount = 0

        is_first = True
        output = ""

        for file in sources:
            with open(file, "r", encoding=CSV_ENCODING) as f:
                content = f.read()
                lines = content.splitlines()
                if not is_first:
                    lines = list(filter(lambda line: "action" not in line, lines))
                    is_first = False
                count = len(lines)
                linecount += count
                typer.echo(f"- {str(count).rjust(4)} | {file}")
                output += "\n".join(lines)
        typer.echo(f"= {str(linecount).rjust(4)} | lines")

        with open(ofile, "w", encoding=CSV_ENCODING) as o:
            count = len(output.splitlines())
            o.write(output)
            typer.echo(f"+ {str(count).rjust(4)} | {ofile}")
