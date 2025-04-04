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
        # print(rows)
        print(len(rows))


#
# def parse_cmd_old(html_path: str) -> None:
#     print(f"parse: {html_path}")
#
#     with open(html_path, "r") as f:
#         html = f.read()
#
#     tree = HTMLParser(html)
#
#     rows, err = collect_menu_rows(tree)
#
#     if err is not None:
#         print(f"! error: {err}")
#         return
#
#     ofile = html_path.replace(".html", ".csv")
#     write_menu_rows(ofile, rows)
#
#     for row in rows:
#         print(row)
#     print(f"wrote csv: {ofile}")
#


# def write_menu_rows(filepath: str, data: list[CsvRow]) -> None:
#     with open(filepath, "w") as f:
#         writer = csv.DictWriter(f, fieldnames=CsvRow.fields())
#
#         writer.writeheader()
#
#         rows = [row.to_dict() for row in data]
#         writer.writerows(rows)


#
# def collect_menu_rows(tree: HTMLParser) -> tuple[list[CsvRow], str | None]:
#     rows: list[CsvRow] = []
#
#     location = menu_location(tree)
#     if not location:
#         return rows, "location not found in tree"
#     rows.append(CsvRow.location(location))
#
#     page = menu_pagename(tree)
#     if not page:
#         return rows, "page not found in tree"
#     rows.append(CsvRow.page(page))
#
#     sections = menu_sections(tree)
#     if not sections:
#         return rows, "no sections were found"
#
#     for section in sections:
#         # rows.append(CsvRow.spacer())
#
#         # category
#         category_title = section_title(section)
#         category_slug = section_slug(section)
#         if category_title:
#             rows.append(CsvRow.item(category_slug, ItemType.Category, category_title))
#
#         # subcategories
#         subcategories = section_subcategories(section)
#
#         if subcategories:
#             for subcategory in subcategories:
#                 subcategory_title = section_title(subcategory)
#                 subcategory_slug = section_slug(subcategory)
#
#                 if subcategory_title:
#                     rows.append(
#                         CsvRow.item(
#                             subcategory_slug, ItemType.Subcategory, subcategory_title
#                         )
#                     )
#
#                 # subcategory menuitems
#                 menuitems = section_menuitems(subcategory)
#
#                 if not menuitems:
#                     continue
#
#                 for item in menuitems:
#                     mrows = collect_menuitem_rows(item)
#                     rows.extend(mrows)
#
#         else:
#             # menuitems
#             menuitems = section_menuitems(section)
#
#             if not menuitems:
#                 continue
#
#             for item in menuitems:
#                 mrows = collect_menuitem_rows(item)
#                 rows.extend(mrows)
#
#     return rows, None
#
#
# def collect_menuitem_rows(node: Node) -> list[CsvRow]:
#     rows: list[CsvRow] = []
#
#     # menuitem
#     item_type = menuitem_type(node)
#     item_title = menuitem_title(item_type, node)
#     item_id = menuitem_id(node)
#     rows.append(CsvRow.item(item_id, item_type, item_title))
#
#     # options
#     if menuitem_has_options(node):
#         options = menuitem_options(node)
#         for option in options:
#             option_id = menuitem_id(option)
#             option_type = menuitem_type(option)
#             option_title = menuitem_title(option_type, option)
#             rows.append(CsvRow.item(option_id, option_type, option_title))
#
#     # addons
#     if menuitem_has_addons(node):
#         addons = menuitem_addons(node)
#         for addon in addons:
#             addon_id = menuitem_id(addon)
#             addon_type = menuitem_type(addon)
#             addon_title = menuitem_title(addon_type, addon)
#             rows.append(CsvRow.item(addon_id, addon_type, addon_title))
#
#     return rows
