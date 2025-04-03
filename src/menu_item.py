from enum import Enum
from typing import override
from selectolax.parser import Node
import re


class MenuItemType(Enum):
    Simple = "simple"
    Option = "option"
    Addon = "addon"
    Wine = "wine"
    OptionGroup = "option-group"
    AddonGroup = "addon-group"


class MenuItem:
    def __init__(self) -> None:
        self.id: str = ""
        self.type: MenuItemType = MenuItemType.Simple
        self.title: str = ""
        self.description: str = ""
        self.prices: list[str] = []
        self.children: list[MenuItem] = []


class MenuItemParser:
    @classmethod
    def parse(cls, node: Node) -> MenuItem:
        # parser choice
        parser = SimpleItemParser()

        if cls.is_wine_item(node):
            parser = WineItemParser()

        elif cls.is_addon_group(node):
            parser = AddonGroupParser()

        elif cls.is_option_group(node):
            parser = OptionGroupParser()

        # hydrate
        item = parser.create(node)

        return item

    @staticmethod
    def is_menuitem(node: Node) -> bool:
        return "menu-item" in str(node.attributes.get("class"))

    @staticmethod
    def is_option_group(node: Node) -> bool:
        addon_title = node.css_first(".add-on-title")
        items = node.css(".menu-item.inline")
        return True if len(items) > 0 and not addon_title else False

    @staticmethod
    def is_addon_group(node: Node) -> bool:
        title = node.css_first(".add-on-title")
        items = node.css(".menu-item.inline")
        return True if len(items) > 0 and title else False

    @staticmethod
    def is_wine_item(node: Node) -> bool:
        pricing_model = node.css(".price-per-size")
        return len(pricing_model) > 0


class BaseMenuItemParser:
    def create(self, node: Node) -> MenuItem:
        item = MenuItem()
        item.type = self.get_type()
        item.id = self.get_id(node) or ""
        item.title = self.get_title(node) or ""
        item.prices = self.clean_prices(self.get_prices(node))
        item.children = self.get_children(node) or []
        return item

    def get_type(self) -> MenuItemType:
        return MenuItemType.Simple

    def get_id(self, node: Node) -> str | None:
        return str(node.attributes.get("data-id")) if node else None

    def get_title(self, node: Node) -> str | None:
        n = node.css_first(".item-header-label-title")
        return n.text().strip().lower().title() if n else None

    def get_prices(self, node: Node) -> list[str]:
        nodes = node.css(".price")
        # print("HTML", node.html)
        return [n.text() for n in nodes]

    def get_children(self, node: Node) -> list[MenuItem]:
        return []

    def clean_prices(self, prices: list[str]) -> list[str]:
        fracmap = {"¼": 0.25, "½": 0.5, "¾": 0.75}
        nprices: list[str] = []
        for price in prices:
            price = price.strip()
            price = re.sub(r"[\+]", "", price)
            match = re.match(r"(\d+)?([¼½¾])?", price)

            if match:
                whole = float(match.group(1)) if match.group(1) else 0.0
                frac = fracmap.get(match.group(2), 0.0)
                num = whole + frac
                nprices.append(f"{num:.2f}")
            else:
                print("UNMATCHED", price)
                nprices.append(price)
        return nprices


class SimpleItemParser(BaseMenuItemParser):
    @override
    def get_type(self) -> MenuItemType:
        return MenuItemType.Simple

    @override
    def get_prices(self, node: Node) -> list[str]:
        return [
            re.sub(r"\s+", "", n.text().strip())
            for n in node.css(".item-header .price")
        ]


class OptionGroupParser(BaseMenuItemParser):
    @override
    def get_type(self) -> MenuItemType:
        return MenuItemType.OptionGroup

    @override
    def get_prices(self, node: Node) -> list[str]:
        return ["0.00"]

    @override
    def get_children(self, node: Node) -> list[MenuItem]:
        nodes = node.css(".menu-items .menu-item.inline")

        options: list[MenuItem] = []

        for n in nodes:
            parser = OptionItemParser()
            option = parser.create(n)
            print(option.type, option.prices)
            options.append(option)

        return options


class OptionItemParser(BaseMenuItemParser):
    @override
    def get_type(self) -> MenuItemType:
        return MenuItemType.Option

    @override
    def get_title(self, node: Node) -> str | None:
        n = node.css_first("strong")
        return n.text().strip().lower().title() if n else None

    @override
    def get_prices(self, node: Node) -> list[str]:
        return [re.sub(r"[\s\+]+", "", n.text().strip()) for n in node.css(".price")]


class AddonGroupParser(BaseMenuItemParser):
    @override
    def get_type(self) -> MenuItemType:
        return MenuItemType.AddonGroup

    @override
    def get_title(self, node: Node) -> str | None:
        n = node.css_first(".add-on-title")
        return n.text().strip() if n else None

    @override
    def get_prices(self, node: Node) -> list[str]:
        return ["0.00"]

    @override
    def get_children(self, node: Node) -> list[MenuItem]:
        nodes = node.css(".menu-item.inline")

        options: list[MenuItem] = []

        for n in nodes:
            parser = AddonItemParser()
            option = parser.create(n)
            options.append(option)

        return options


class AddonItemParser(BaseMenuItemParser):
    @override
    def get_type(self) -> MenuItemType:
        return MenuItemType.Addon

    @override
    def get_title(self, node: Node) -> str | None:
        n = node.css_first(".inline")
        price = node.css_first(".price")
        return (
            n.text().replace(price.text(), "").strip().lower() if n and price else None
        )


class WineItemParser(BaseMenuItemParser):
    @override
    def get_type(self) -> MenuItemType:
        return MenuItemType.Wine

    @override
    def get_prices(self, node: Node) -> list[str]:
        prices = [n.text().strip() for n in node.css(".item-header > .price-per-size")]
        prices.reverse()
        return prices
