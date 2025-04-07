from menu import Menu
from menu_category import MenuCategory
from menu_item import MenuItem, MenuItemType
import json


class ImpexRow:
    def __init__(
        self,
        menu: str = "",
        page: str = "",
        action: str = "",
        type: str = "",
        item_id: str = "",
        batch_id: str = "",
        title: str = "",
        description: str = "",
        prices: str = "",
        image_ids: str = "",
        # attrs
        is_new: str = "",
        is_glutensmart: str = "",
        is_organic: str = "",
        is_vegan: str = "",
        is_vegetarian: str = "",
        custom: str = "",
    ) -> None:
        self.data: dict[str, str] = {}
        self.data["menu"] = menu
        self.data["page"] = page
        self.data["action"] = action
        self.data["type"] = type
        self.data["item_id"] = item_id
        self.data["batch_id"] = batch_id
        self.data["title"] = title
        self.data["description"] = description
        self.data["prices"] = prices
        self.data["image_ids"] = image_ids
        self.data["custom"] = custom
        # at.datatrs
        self.data["is_new"] = is_new
        self.data["is_glutensmart"] = is_glutensmart
        self.data["is_organic"] = is_organic
        self.data["is_vegan"] = is_vegan
        self.data["is_vegetarian"] = is_vegetarian

    def __getitem__(self, key: str):
        return self.data[key]


class ImpexMenuTransformer:
    fields: list[str] = [
        "action",
        "menu",
        "page",
        "batch_id",
        "type",
        "item_id",
        "title",
        "prices",
        "image_ids",
        # attrs
        "is_new",
        "is_glutensmart",
        "is_organic",
        "is_vegan",
        "is_vegetarian",
        "custom",
        "description",
    ]

    @staticmethod
    def header_rows(menu: Menu) -> list[str]:
        return []
        return [
            f"menu,{menu.id}",
            f"page,{menu.page}",
        ]

    @classmethod
    def transform(cls, menu: Menu) -> list[ImpexRow]:
        l: list[ImpexRow] = []

        # list
        # menu = ImpexRow(type="menu", item_id=menu.id)
        # page = ImpexRow(type="page", item_id=menu.page)
        # l.extend([menu, page])

        for category in menu.categories:
            rows = cls.transform_category(menu, category)
            l.extend(rows)

        # items
        return l

    @classmethod
    def transform_category(cls, menu: Menu, category: MenuCategory) -> list[ImpexRow]:
        rows: list[ImpexRow] = []

        # category
        impex_category = ImpexRow(
            menu=menu.id,
            page=menu.page,
            type=f"category-{category.level}",
            title=Format.title(category.title),
            description=Format.html(category.description),
            prices=Format.csv("|", category.price_options),
        )
        rows.append(impex_category)

        # subcategories
        for subcategory in category.categories:
            impex_subcategories = cls.transform_category(menu, subcategory)
            rows.extend(impex_subcategories)

        # menuitems
        for item in category.menuitems:
            rows.append(cls.transform_menuitem(menu, item))

            for child in item.children:
                rows.append(cls.transform_menuitem(menu, child))

        return rows

    @classmethod
    def transform_menuitem(cls, menu: Menu, item: MenuItem) -> ImpexRow:
        return ImpexRow(
            menu=menu.id,
            page=menu.page,
            type=Format.item_type(item.type),
            item_id=item.id,
            title=item.title,
            prices=Format.csv("|", item.prices),
            image_ids=Format.csv("|", item.image_ids),
            is_new=Format.yesno(item.is_new),
            is_glutensmart=Format.yesno(item.is_glutensmart),
            is_organic=Format.yesno(item.is_organic),
            is_vegan=Format.yesno(item.is_vegan),
            is_vegetarian=Format.yesno(item.is_vegetarian),
            description=Format.html(item.description),
        )


class Format:
    @staticmethod
    def yesno(v: bool) -> str:
        return "yes" if v else "no"

    @staticmethod
    def item_type(v: str | MenuItemType) -> str:
        return str(v).replace("MenuItemType.", "").lower().replace("group", "-group")

    @staticmethod
    def csv(delim: str, v: list[str]) -> str:
        return delim.join(v)

    @staticmethod
    def title(v: str) -> str:
        return v.strip()

    @staticmethod
    def html(v: str) -> str:
        return v.strip().replace("\n", "<br/>")

    @staticmethod
    def category_price_options(v: list[str]) -> str:
        if not v:
            return ""
        return json.dumps({"price_options": Format.csv(",", v)})
