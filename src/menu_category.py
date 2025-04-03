from typing import override
from selectolax.parser import Node
import re

import menu
from menu_item import MenuItem


class MenuCategory:
    def __init__(self, level: int = 0) -> None:
        self.level: int = level
        self.id: str = ""
        self.title: str = ""
        self.description: str = ""
        self.menuitems: list[MenuItem] = []
        self.subcategories: list[MenuCategory] = []

    @override
    def __repr__(self) -> str:
        return f"MenuCategory(id={self.id}, level={self.level}, title={self.title}, items={len(self.menuitems)}, subcategories={len(self.subcategories)})"


class MenuCategoryParser:
    @classmethod
    def parse(cls, node: Node) -> MenuCategory:
        if not cls.is_category(node):
            raise ValueError("node is not a MenuCategory")

        # make
        o = MenuCategory()
        o.id = cls.get_slug(node) or ""
        o.title = cls.get_title(node) or ""
        o.description = cls.get_description(node) or ""

        print(o.id)

        # add menuitems
        menuitem_nodes = cls.get_menuitem_nodes(node, o.id)

        # for menuitem_node in menuitem_nodes:
        #     item = MenuItem.create(menuitem_node)
        #     print(item)

        return o

    @classmethod
    def is_category(cls, node: Node) -> bool:
        return node.tag == "section"

    @classmethod
    def get_title(cls, node: Node) -> str | None:
        title = node.css_first(".category-header-title")
        return title.text().upper().strip() if title else None

    @classmethod
    def get_slug(cls, node: Node) -> str | None:
        title = node.css_first(".category-header-title")
        slug = title.attributes.get("data-slug") if title else None
        return slug.lower().strip() if slug else ""

    @classmethod
    def get_description(cls, node: Node) -> str | None:
        desc = node.css_first(".category-description")
        return desc.text() if desc else None

    @classmethod
    def get_menuitem_nodes(cls, node: Node, id: str) -> list[Node]:
        return node.css(f".menu-item.{id}")
