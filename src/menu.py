from typing import override
from selectolax.parser import HTMLParser, Node
from menu_category import MenuCategory, MenuCategoryParser


class Menu:
    def __init__(self, id: str = "", page: str = "") -> None:
        self.id: str = id
        self.page: str = page
        self.categories: list[MenuCategory] = []

    @override
    def __repr__(self) -> str:
        return f"Menu(id={self.id}, page={self.page})"

    def to_csv(self) -> list[list[str]]:
        return []


class MenuParser:
    @classmethod
    def parse(cls, html: str) -> Menu:
        tree = HTMLParser(html)
        body = tree.css_first("body")

        # body
        if not body:
            raise ValueError("no <body> found in html")

        # menu
        if not cls.has_menu(body):
            raise ValueError("menu not found in html")

        # location
        location = cls.get_location(body)
        if location is None:
            raise ValueError("menu location not found")

        # page
        page = cls.get_page(body)
        if page is None:
            raise ValueError("menu page not found")

        menu = Menu(id=location, page=page)

        # categories
        category_nodes = cls.get_category_nodes(body)
        if not category_nodes:
            raise ValueError("menu categories not found")

        # iter category_nodes
        # print(f"sections: {len(category_nodes)}")
        for category_node in category_nodes:
            categories = MenuCategoryParser.parse(category_node)
            menu.categories.extend(categories)
        # print(category)

        # now we can make a menu

        return menu

    @staticmethod
    def has_menu(node: Node) -> bool:
        el = node.css_first("#ccc-menu")
        return True if el else False

    @staticmethod
    def get_location(node: Node) -> str | None:
        el = node.css_first("[data-location]")
        return str(el.attributes.get("data-location")) if el else None

    @staticmethod
    def get_page(node: Node) -> str | None:
        el = node.css_first("#ccc-menu-filters .filter.selected")
        return str(el.attributes.get("data-filter")) if el else None

    @staticmethod
    def get_category_nodes(node: Node) -> list[Node]:
        return node.css("#ccc-menu div > section:not(.sub-categories)")
