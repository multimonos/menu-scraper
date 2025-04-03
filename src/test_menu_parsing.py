from socket import has_dualstack_ipv6
from typing import ClassVar
import unittest

from selectolax.parser import HTMLParser

from menu_parsing import (
    is_menuitem,
    menuitem_has_addons,
    menu_location,
    menu_pagename,
    menu_sections,
    menuitem_addon_title,
    menuitem_addons,
    menuitem_has_options,
    menuitem_title,
    section_menuitems,
    menuitem_options,
    section_slug,
    section_subcategories,
    section_title,
)
from dataset import Dataset


class FoodMenuTest(unittest.TestCase):
    html: str = ""
    tree: ClassVar[HTMLParser]

    @classmethod
    def setUpClass(cls):
        with open("./test-data/food.html", "r", encoding="utf-8") as f:
            cls.html = f.read()
            cls.tree = HTMLParser(cls.html)
            cls.data: Dataset = Dataset()

    def test_data_loaded(self):
        self.assertNotEqual(self.html, "")

    def test_tree_created(self):
        self.assertIsInstance(self.tree, HTMLParser)

    """location"""

    def test_menu_location(self):
        self.assertEqual("crowfoot", menu_location(self.tree))

    """menu"""

    def test_get_menu(self):
        self.assertEqual("food", menu_pagename(self.tree))

    """sections"""

    def test_get_sections(self):
        sections = menu_sections(self.tree)
        self.assertEqual(10, len(sections))

    def test_section_title(self):
        sections = menu_sections(self.tree)
        titles: list[str] = []
        for section in sections:
            titles.append(section_title(section))
        self.assertEqual(10, len(titles))
        self.assertListEqual(
            [
                "FEATURES",
                "SUSHI",
                "START + SHARE",
                "BOWLS",
                "GREENS",
                "CASUAL FAVOURITES",
                "BURGERS",
                "MAINS",
                "STEAKS",
                "DESSERTS",
            ],
            titles,
        )

    def test_section_slug(self):
        sections = menu_sections(self.tree)
        slugs: list[str] = []
        for section in sections:
            slugs.append(section_slug(section))
        self.assertEqual(10, len(slugs))
        self.assertListEqual(
            [
                "features",
                "sushi",
                "start-share",
                "bowls",
                "greens",
                "casual-favourites",
                "burgers",
                "mains",
                "steaks",
                "desserts",
            ],
            slugs,
        )

    """subcategories"""

    def test_section_subcategories(self):
        sections = menu_sections(self.tree)
        for section in sections:
            self.assertEqual(0, len(section_subcategories(section)))

    def test_section_menuitems(self):
        sections = menu_sections(self.tree)
        counts: list[int] = []
        for section in sections:
            items = section_menuitems(section)
            counts.append(len(items))

        self.assertListEqual(
            [
                3,  # features
                3,  # sushi
                11,  # start-share
                4,  # bowls
                3,  # greens
                5,  # casual-favourites
                4,  # burgers
                7,  # mains
                8,  # steaks
                6,  # desserts
            ],
            counts,
        )

    """shared menuitem fns"""

    def test_is_menuitem(self):
        self.assertTrue(is_menuitem(Dataset.standard_menuitem()))

    def test_menuitem_title(self):
        pass

    """options"""

    def test_menuitem_has_options(self):
        v = menuitem_has_options(Dataset.option_group())
        self.assertEqual(True, v)

    def test_menuitem_has_options_false(self):
        v = menuitem_has_options(Dataset.standard_menuitem())
        self.assertEqual(False, v)
        v = menuitem_has_options(Dataset.addon_group())
        self.assertEqual(False, v)

    def test_menuitem_options(self):
        v = menuitem_options(Dataset.option_group())
        self.assertEqual(2, len(v))

    def test_menuitem_options_empty(self):
        v = menuitem_options(Dataset.standard_menuitem())
        self.assertEqual(0, len(v))

        v = menuitem_options(Dataset.addon_group())
        self.assertEqual(0, len(v))

    """addons"""

    def test_has_menuitem_addons(self):
        v = menuitem_has_addons(Dataset.addon_group())
        self.assertEqual(True, v)

    def test_has_menuitem_addons_false(self):
        v = menuitem_has_addons(Dataset.option_group())
        self.assertEqual(False, v)
        v = menuitem_has_addons(Dataset.standard_menuitem())
        self.assertEqual(False, v)

    def test_menuitem_addons(self):
        v = menuitem_addons(Dataset.addon_group())
        self.assertEqual(3, len(v))

    def test_menuitem_addons_empty(self):
        v = menuitem_addons(Dataset.standard_menuitem())
        self.assertEqual(0, len(v))

        v = menuitem_addons(Dataset.option_group())
        self.assertEqual(0, len(v))

    def test_menuitem_addon_title(self):
        title = menuitem_addon_title(Dataset.addon_group())
        self.assertEqual("Substitute", title)

    def test_menuitem_addon_title_none(self):
        title = menuitem_addon_title(Dataset.standard_menuitem())
        self.assertEqual(None, title)
        title = menuitem_addon_title(Dataset.option_group())
        self.assertEqual(None, title)


if __name__ == "__main__":
    unittest.main()
