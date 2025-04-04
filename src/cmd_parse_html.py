import csv
from constants import CSV_ENCODING
from impex import ImpexMenuTransformer
from menu import MenuParser
from menu_printer import MenuPrinter


def parse_html_cmd(html_path: str, csv_path: str | None) -> None:
    with open(html_path, "r") as f:
        html = f.read()

    menu = MenuParser.parse(html)

    if csv_path is None:
        MenuPrinter.print(menu)

    else:
        rows = ImpexMenuTransformer.transform(menu)

        with open(csv_path, "w", encoding=CSV_ENCODING) as f:
            # header rows
            for header_row in ImpexMenuTransformer.header_rows(menu):
                f.write(f"{header_row}\n")

            # content
            writer = csv.DictWriter(f, fieldnames=ImpexMenuTransformer.fields)
            writer.writeheader()
            rows = [row.data for row in rows]
            writer.writerows(rows)
