from menu import Menu
from menu_category import MenuCategory
from menu_item import MenuItem, MenuItemType


class MenuPrinter:
    @classmethod
    def print(cls, menu: Menu) -> None:
        print("---")
        print("location:", menu.location)
        print("page:", menu.page)
        print("---")
        for category in menu.categories:
            cls.print_category(category)
        print("---")

    @classmethod
    def print_category(cls, category: MenuCategory):
        print(category.level, category.title)
        print(" ", len(category.menuitems))

        # categories
        if len(category.categories):
            for subcategory in category.categories:
                cls.print_category(subcategory)

        # menuitems
        i = 1
        for item in category.menuitems:
            print(" ", str(i).ljust(2), cls.fmt_menuitem(item))
            i += 1
            j = 0
            for child in item.children:
                print("    ", str(j).ljust(2), cls.fmt_menuitem(child))
                j += 1

    @classmethod
    def fmt_menuitem(cls, item: MenuItem) -> str:
        return "".join(
            [
                cls.short_type(item.type).ljust(12),
                "  ",
                item.title,
                "  $[",
                "|".join(item.prices),
                "]",
            ]
        )

    @staticmethod
    def short_type(x: MenuItemType) -> str:
        return str(x).replace("MenuItemType.", "")
