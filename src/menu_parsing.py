from enum import Enum
from selectolax.parser import HTMLParser, Node


class ItemType(Enum):
    Location = "location"
    Page = "page"
    Category = "category"
    Subcategory = "subcategory"
    # Menu Items
    Item = "item"
    Wine = "wine"
    Addon = "addon"
    AddonGroup = "addon-group"
    Option = "option"
    OptionGroup = "option-group"


"""location fns"""


def menu_location(tree: HTMLParser) -> str:
    node = tree.css_first("[data-location]")
    return str(node.attributes.get("data-location")) if node else ""


def menu_pagename(tree: HTMLParser) -> str:
    node = tree.css_first("#ccc-menu-filters .filter.selected")
    return str(node.attributes.get("data-filter")) if node else ""


"""section fns"""


def menu_sections(parser: HTMLParser) -> list[Node]:
    nodes: list[Node] = parser.css("#ccc-menu div > section:not(.sub-categories)")
    return nodes


def section_title(node: Node) -> str | None:
    title = node.css_first(".category-header-title")
    return title.text().upper().strip() if title else None


def section_slug(node: Node) -> str:
    title = node.css_first(".category-header-title")
    slug = title.attributes.get("data-slug") if title else None
    return slug.lower().strip() if slug else ""


def section_menuitems(section: Node) -> list[Node]:
    nodes = section.css(".container .menu-item:not(.inline)")
    # discard empty items
    menuitems = [node for node in nodes if node.text().strip() != ""]
    return menuitems


def section_subcategories(node: Node) -> list[Node]:
    nodes = node.css("section.sub-categories section")
    return nodes


"""menuitem ( generic ) fns"""


def is_menuitem(node: Node) -> bool:
    return "menu-item" in str(node.attributes.get("class"))


def menuitem_id(node: Node) -> str:
    if not "menu-item" in str(node.attributes.get("class")):
        raise ValueError("invalid menu item node")
    return str(node.attributes.get("data-id")) if node else "None"


def menuitem_type(node: Node) -> ItemType:
    """error"""
    if not "menu-item" in str(node.attributes.get("class")):
        raise ValueError("invalid menu item node")

    """classify"""
    if node.css(".bottle"):
        return ItemType.Wine

    elif node.css(".add-on-title") and node.css(".menu-item"):
        return ItemType.AddonGroup

    elif node.css("strong") and "inline" in str(node.attributes.get("class")):
        return ItemType.Option

    elif "inline" in str(node.attributes.get("class")):
        return ItemType.Addon

    return ItemType.Item


def menuitem_title(type: ItemType, item: Node) -> str:
    title = None

    if ItemType.Item == type:
        # .menu-item .item-header .item-header-label .item-header-label-title_inner
        node = item.css_first(".item-header-label-title")
        if node:
            title = node.text().strip().lower().title()

    elif ItemType.OptionGroup == type:
        # .menu-item .item-header .item-header-label .item-header-label-title_inner
        node = item.css_first(".item-header-label-title_inner")
        if node:
            title = node.text().strip().lower().title()

    elif ItemType.Option == type:
        node = item.css_first("strong")
        if node:
            title = node.text().strip().lower()

    elif ItemType.AddonGroup == type:
        node = item.css_first(".add-on-title")
        if node:
            title = node.text().lower().title().strip()

    elif ItemType.Addon == type:
        node = item.css_first(".inline")
        price = node.css_first(".price")
        if node and price:
            title = node.text().replace(price.text(), "").strip().lower()

    elif ItemType.Wine == type:
        node = item.css_first(".item-header-label-title_inner")
        if node:
            title = node.text().strip().lower().title()

    if title is None:
        print("unknown-title:", item.text())
        return "<title>"

    return title


"""addon fns"""


def menuitem_has_addons(node: Node) -> bool:
    title = node.css_first(".add-on-title")
    items = node.css(".menu-item.inline")
    return True if len(items) > 0 and title else False


def menuitem_addon_title(node: Node) -> str | None:
    # optional
    title = node.css_first(".add-on-title")
    return title.text() if title else None


def menuitem_addons(node: Node) -> list[Node]:
    if menuitem_has_addons(node):
        return node.css(".menu-item.inline")
    return []


"""option fns"""


def menuitem_has_options(node: Node) -> bool:
    addon_title = node.css_first(".add-on-title")
    items = node.css(".menu-item.inline")
    return True if len(items) > 0 and not addon_title else False


def menuitem_options(node: Node) -> list[Node]:
    addon_title = menuitem_addon_title(node)

    if addon_title is None:
        nodes = node.css(".menu-items .menu-item.inline")
        return nodes

    return []


def menuitem_carousels():
    pass
