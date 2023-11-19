from selectolax.parser import HTMLParser, Node
from playwright.sync_api import Playwright, sync_playwright, Page

import console
import data_handler


def start_scraper(search_term: str, pages=1) -> None:
    console.log_header(f"Scraping {pages} {'page' if pages == 1 else 'pages'} for {search_term}")

    with sync_playwright() as playwright:
        open_browser(playwright, search_term, pages)
    


def open_browser(playwright: Playwright, search_term: str, pages=1) -> None:
    # Open browser
    console.log("Opening browser...")

    # Set headless=False if you'd like to see the browser navigate itself
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    console.log("Navigating to target page...")
    page.goto("https://www.ebay.com/")
    page.get_by_placeholder("Search for anything").click()
    page.get_by_placeholder("Search for anything").fill(search_term)
    page.get_by_placeholder("Search for anything").press("Enter")
    page.wait_for_selector('div[id="srp-river-main"]')

    # Scrape product info
    current_page_url = page.url
    current_page_number = 1

    # Loop through desired amount of product pages
    while int(current_page_number) <= int(pages):
        # The browser is already on page 1 so no need reload the url
        if current_page_number != 1:
            page.goto(current_page_url)

        # Get the html then parse out the product info
        html = Helpers.get_html(page)
        product_list = Helpers.parse_html(html)

        data_handler.add_to_product_list(product_list, current_page_number)

        console.log(f"Page {current_page_number} complete...")

        # Construct the url for the next product page
        current_page_number = int(current_page_number) + 1
        current_page_url = f"{page.url[:-1]}{current_page_number}"

    data_handler.save_product_info(search_term, pages)

    # Close browser
    context.close()
    browser.close()


class Helpers:
    def get_html(page: Page) -> HTMLParser:
        return HTMLParser(page.content())

    def parse_html(html: HTMLParser) -> list[Node]:
        search_result_container = html.css_first('div[id="srp-river-main"]')
        search_results = search_result_container.css("div.s-item__info")

        return search_results
