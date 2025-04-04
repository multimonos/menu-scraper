import csv
from datetime import datetime
import os
from impex import ImpexMenuTransformer
from menu import MenuParser
from menu_printer import MenuPrinter


def parse_cmd(html_path: str, output_format: str) -> None:
    os.system("clear")
    print(f"--- parse : {datetime.now().timestamp()} ---")
    print("file:", html_path)

    with open(html_path, "r") as f:
        html = f.read()

    menu = MenuParser.parse(html)

    if "text" == output_format:
        MenuPrinter.print(menu)
        print(datetime.now().timestamp())

    elif "csv" == output_format:
        csv_path = html_path.replace(".html", ".csv")
        print("csv time", html_path, "->", csv_path)
        rows = ImpexMenuTransformer.transform(menu)
        with open(csv_path, "w+", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=ImpexMenuTransformer.fields)
            writer.writeheader()
            rows = [row.data for row in rows]
            writer.writerows(rows)

        with open(csv_path, "r", encoding="utf-8") as f:
            print(f.read())

        print(len(rows))
