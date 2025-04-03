from enum import Enum
from typing import override
from selectolax.parser import Node


class MenuItemType(Enum):
    Item = "item"
    Option = "option"
    Addon = "addon"
    Wine = "wine"
    OptionGroup = "option-group"
    AddonGroup = "addon-group"


class MenuItem:
    def __init__(self, type: MenuItemType = MenuItemType.Item) -> None:
        self.type: MenuItemType = type
        self.title: str = ""
        self.description: str = ""
        self.prices: list[str] = []
        self.children: list[MenuItem] = []

    @classmethod
    def create(cls, node: Node) -> "MenuItem":
        raise NotImplemented

    @classmethod
    def factory(cls, node: Node) -> "MenuItem":
        """TODO should this be in the MenuItemParser"""

        if not MenuItemParser.is_menuitem(node):
            raise ValueError("node is not a menuitem")

        if MenuItemParser.is_option_group(node):
            return OptionGroupMenuItem.create(node)

        elif MenuItemParser.is_addon_group(node):
            return AddonGroupMenuItem.create(node)

        return MenuItem.create(node)


class MenuItemParser:
    @classmethod
    def is_menuitem(cls, node: Node) -> bool:
        return "menu-item" in str(node.attributes.get("class"))

    @classmethod
    def is_option_group(cls, node: Node) -> bool:
        addon_title = node.css_first(".add-on-title")
        items = node.css(".menu-item.inline")
        return True if len(items) > 0 and not addon_title else False

    @classmethod
    def is_addon_group(cls, node: Node) -> bool:
        title = node.css_first(".add-on-title")
        items = node.css(".menu-item.inline")
        return True if len(items) > 0 and title else False


class WineMenuItem(MenuItem):
    def __init__(self) -> None:
        super().__init__(type=MenuItemType.Wine)

    @override
    @classmethod
    def create(cls, node: Node) -> "WineMenuItem":
        o = WineMenuItem()
        return o


class OptionGroupMenuItem(MenuItem):
    def __init__(self) -> None:
        super().__init__(type=MenuItemType.OptionGroup)

    @override
    @classmethod
    def create(cls, node: Node) -> "OptionGroupMenuItem":
        o = OptionGroupMenuItem()
        return o


class OptionMenuItem(MenuItem):
    def __init__(self) -> None:
        super().__init__(type=MenuItemType.Option)

    @override
    @classmethod
    def create(cls, node: Node) -> "OptionMenuItem":
        o = OptionMenuItem()
        return o


class AddonGroupMenuItem(MenuItem):
    def __init__(self) -> None:
        super().__init__(type=MenuItemType.AddonGroup)

    @override
    @classmethod
    def create(cls, node: Node) -> "AddonGroupMenuItem":
        o = AddonGroupMenuItem()
        return o


class AddonMenuItem(MenuItem):
    def __init__(self) -> None:
        super().__init__(type=MenuItemType.Addon)

    @override
    @classmethod
    def create(cls, node: Node) -> "AddonMenuItem":
        o = AddonMenuItem()
        return o
