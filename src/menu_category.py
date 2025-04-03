from typing import override
from selectolax.parser import Node
from menu_item import MenuItem, MenuItemParser


class MenuCategory:
    def __init__(self, level: int = 0) -> None:
        self.level: int = level
        self.id: str = ""
        self.title: str = ""
        self.description: str = ""
        self.menuitems: list[MenuItem] = []
        self.categories: list[MenuCategory] = []

    @override
    def __repr__(self) -> str:
        return f"MenuCategory(id={self.id}, level={self.level}, title={self.title}, items={len(self.menuitems)}, categories={len(self.categories)})"


class MenuCategoryParser:
    @classmethod
    def parse(cls, node: Node, level: int = 0) -> list[MenuCategory]:
        if not cls.is_category(node):
            raise ValueError("node is not MenuCategory html")

        categories: list[MenuCategory] = []

        # category
        o = MenuCategory()
        o.id = cls.get_slug(node) or ""
        o.level = level
        o.title = cls.get_title(node) or ""
        o.description = cls.get_description(node) or ""

        categories.append(o)

        # subcategories
        subcategory_nodes = cls.get_subcategory_nodes(node)
        if subcategory_nodes:
            for subcategory_node in subcategory_nodes:
                subcategories = cls.parse(subcategory_node, level=level + 1)
                categories.extend(subcategories)

        # menuitems
        menuitem_nodes = cls.get_menuitem_nodes(node, o.id)

        for menuitem_node in menuitem_nodes:
            item = MenuItemParser.parse(menuitem_node)
            o.menuitems.append(item)
        # for menuitem_node in menuitem_nodes:
        #     print(menuitem_node.html[:30].strip())
        # o.menuitems.append(item)

        return categories

    @staticmethod
    def is_category(node: Node) -> bool:
        return node.tag == "section"

    @staticmethod
    def get_title(node: Node) -> str | None:
        title = node.css_first(".category-header-title")
        return title.text().upper().strip() if title else None

    @staticmethod
    def get_slug(node: Node) -> str | None:
        title = node.css_first(".category-header-title")
        slug = title.attributes.get("data-slug") if title else None
        return slug.lower().strip() if slug else ""

    @staticmethod
    def get_description(node: Node) -> str | None:
        desc = node.css_first(".category-description")
        return desc.text() if desc else None

    @staticmethod
    def get_menuitem_nodes(node: Node, id: str) -> list[Node]:
        nodes: list[Node] = []
        # basic
        menuitems = node.css(f".menu-item.{id}")
        nodes.extend(menuitems)
        # addons
        addons = node.css(".menu-item:has(.add-on-title)")
        nodes.extend(addons)
        return nodes

    @staticmethod
    def get_subcategory_nodes(node: Node) -> list[Node]:
        nodes = node.css("section.sub-categories section")
        return nodes
