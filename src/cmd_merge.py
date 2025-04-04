from pathlib import Path


def merge_cmd(filepaths: list[Path], output: str | None = None):
    content = ""
    for file in filepaths:
        s = file.read_text(encoding="utf-8")
        content += s

    if output is not None:
        with open(output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Merge written to {output}")
    else:
        print(content)
