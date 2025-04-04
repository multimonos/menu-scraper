import re
from playwright.sync_api import Page, sync_playwright
from constants import HEADLESS, TIMEOUT


def scrape_cmd(site_url: str) -> None:
    print(f"scraping...")
    print(f"site_url: {site_url}")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        menu_urls = scrape_menu_urls(page, site_url)

        # menu_urls = menu_urls[:1] # test one

        print(f"  {len(menu_urls)} urls found")

        for menu_url in menu_urls:
            print(f"{menu_url}")
            pages = scrape_menu_pages(page, menu_url)
            # print(f"  found: {', '.join(pages.keys())}")

            for menu_id, html in pages.items():
                ofile = menu_filepath(menu_url, menu_id)
                with open(ofile, "w") as f:
                    f.write(html)
                    print(f"  {menu_id} -> {ofile}")


def scrape_menu_urls(page: Page, url: str) -> list[str]:
    # init
    menu_urls: list[str] = []

    # goto site
    page.goto(url, wait_until="networkidle")
    page.wait_for_selector("#main-nav-menu", timeout=TIMEOUT)

    # open 'menus'
    page.click("#menu-item-22227")

    # wait for flyout
    page.wait_for_selector(".location-list")

    # iter regions in accordion
    regions = page.locator(".accordion-item")

    for i in range(regions.count()):
        regions.nth(i).click()
        locations = regions.nth(i).locator(".accordion-collapse")
        locations.wait_for(state="visible")
        links = locations.locator("a[data-location]")

        # iter  locations in accordion
        for j in range(links.count()):
            href = links.nth(j).get_attribute("href")
            if href:
                menu_urls.append(href)

    return menu_urls


def scrape_menu_pages(page: Page, menu_url: str) -> dict[str, str]:
    # iter menus
    page.goto(menu_url)
    filter_container = page.locator("#ccc-menu-filters")
    filters = filter_container.locator("[data-filter]")

    menus: dict[str, str] = {}

    # iter menu filters
    for i in range(filters.count()):
        filter_id = filters.nth(i).get_attribute("data-filter")

        if filter_id is None:
            continue

        # open menu
        filters.nth(i).click()
        page.wait_for_selector(f"#ccc-menu-filters .selected[data-filter={filter_id}]")

        # read menu
        menu = page.wait_for_selector(f"#ccc-menu #{filter_id}", timeout=TIMEOUT)
        if menu is None:
            continue

        # save html
        menu = page.locator(f"#ccc-menu #{filter_id}")
        menus[filter_id] = page.content()

    return menus


def menu_filepath(url: str, menu_id: str) -> str:
    url = re.sub(r"https?:\/\/", "", url)
    url = re.sub(r"\W+", "-", url)
    filepath = f"data/{url}-{menu_id}.html"
    return filepath
