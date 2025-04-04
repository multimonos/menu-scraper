from typing import override

from menu_parsing import ItemType


class CsvRow:
    def __init__(self, id: str, type: str, title: str) -> None:
        self.action: str = ""
        self.type: str = type
        self.id: str = id
        self.batch_id: str = ""
        self.title: str = title
        self.description: str = ""
        self.price: float | None = None
        self.custom_name: str = ""
        self.custom_value: str = ""
        self.is_new: bool = False
        self.is_glutenfree: bool = False
        self.is_vegan: bool = False
        self.is_vegetarian: bool = False
        self.is_organic_grape: bool = False

    @override
    def __repr__(self) -> str:
        return f"{self.type.ljust(12)}  {self.id.ljust(15)}  {self.title}"

    def to_list(self) -> list[str]:
        return list(self.to_dict().values())

    def to_dict(self) -> dict[str, str]:
        return {
            "action": self.action,
            "type": self.type,
            "id": self.id,
            "batch_id": self.batch_id,
            "title": self.title,
            "description": self.description,
            "price": str(self.price) if self.price is not None else "",
            "custom_name": self.custom_name,
            "custom_value": self.custom_value,
            "is_new": self.yesno(self.is_new),
            "is_vegan": self.yesno(self.is_vegan),
            "is_glutenfree": self.yesno(self.is_glutenfree),
            "is_vegetarian": self.yesno(self.is_vegetarian),
            "is_organic_grape": self.yesno(self.is_organic_grape),
        }

    @classmethod
    def yesno(cls, v: bool) -> str:
        return "yes" if v == True else "no"

    @classmethod
    def fields(cls) -> list[str]:
        return [
            "action",
            "type",
            "id",
            "batch_id",
            "title",
            "description",
            "price",
            "custom_name",
            "custom_value",
            "is_new",
            "is_vegan",
            "is_glutenfree",
            "is_vegetarian",
            "is_organic_grape",
        ]

    @classmethod
    def spacer(cls):
        return cls("-----", "------", "-----")

    @classmethod
    def location(cls, id: str) -> "CsvRow":
        return cls(id, str(ItemType.Location).replace("ItemType.", ""), id)

    @classmethod
    def page(cls, id: str) -> "CsvRow":
        return cls(id, str(ItemType.Page).replace("ItemType.", ""), id)

    @classmethod
    def item(cls, id: str, type: ItemType, title: str) -> "CsvRow":
        # if type in [ItemType.Option, ItemType.Addon]:
        #     title = "       " + title

        return cls(id, str(type).replace("ItemType.", ""), title)
