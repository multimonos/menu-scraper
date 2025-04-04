from pathlib import Path

from constants import CSV_ENCODING


def merge_cmd(filepaths: list[Path], output: str | None = None):
    content = ""
    for file in filepaths:
        s = file.read_text(encoding=CSV_ENCODING)
        content += s

    if output is not None:
        with open(output, "w", encoding=CSV_ENCODING) as f:
            f.write(content)
        print(f"Merge written to {output}")
    else:
        print(content)
