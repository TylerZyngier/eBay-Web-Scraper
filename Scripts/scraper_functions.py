from selectolax.parser import HTMLParser, Node
from playwright.sync_api import Playwright, sync_playwright, Page
from dataclasses import dataclass, asdict
import customtkinter as ctk
import json
import os

import FileUtilities
import scraper_gui


@dataclass
class Stats():
    search_term: str | None
    results: str | None
    pages: str | None
    average_price: float | None
    lowest_price: float | None
    highest_price: float | None


@dataclass
class Product():
    name: str | None
    price: str | None
    discount: str | None
    page_number: int | None


class BrowserInteraction:
    gui_instance = None

    def run_browser(playwright: Playwright, search_term: str, pages=1) -> None:
        # Open browser
        console_message("Operating browser...")
        browser = playwright.chromium.launch(headless=True)  # Set headless=False if you'd like to see the browser navigate itself
        context = browser.new_context()
        page = context.new_page()

        # Navigate to target page
        console_message("Searching for products...")
        page.goto("https://www.ebay.com/")
        page.get_by_placeholder("Search for anything").click()
        page.get_by_placeholder("Search for anything").fill(search_term)
        page.get_by_placeholder("Search for anything").press("Enter")
        page.wait_for_selector('div[id="srp-river-main"]')

        base_page_url = page.url
        current_page_url = base_page_url

        current_page_number = 1

        # PLEASE FIX THIS SHIT IM TOO TIRED STOP STAYING UP SO LATE YOU ARE GOING TO BURN OUT

        # Loop through all the desired webpages and get the html from each
        while current_page_number < pages:

            if current_page_number != 1:
                page.goto(current_page_url)

            html = BrowserInteraction.get_html(page)
            search_results = BrowserInteraction.parse_html(html)

            DataHandling.add_results_to_data(search_results, current_page_number)

            # current_page_number = int(current_page_number) + 1
            # current_page_url = f'{base_page_url[:-1]}{current_page_number}'

        DataHandling.save_product_info(search_term, current_page_number)

        console_message(f'Retrieved info from {DataHandling.stats.results} results accross {current_page_number} pages!')

        # Close browser
        context.close()
        browser.close()

    def get_html(page: Page) -> HTMLParser:
        return HTMLParser(page.content())

    def parse_html(html: HTMLParser) -> list[Node]:
        search_result_container = html.css_first('div[id="srp-river-main"]')
        search_results = search_result_container.css('div.s-item__info')

        return search_results


class DataHandling:
    products = []
    stats = Stats

    def add_results_to_data(search_results, page_number) -> None:
        # Save products to list
        for result in search_results:
            product = Product(
                name=DataHandling.get_text(result, 'span[role=heading]'),
                price=DataHandling.get_text(result, 'span[class=s-item__price]'),
                discount=DataHandling.get_text(result, 'span[class="s-item__discount s-item__discount"]'),
                page_number=page_number
            )

            DataHandling.products.append(asdict(product))

    def save_product_info(search_term, page_number):
        # Save Stats
        DataHandling.stats = Stats(
            search_term=search_term,
            results=len(DataHandling.products),
            pages=page_number,
            lowest_price=None,
            highest_price=None,
            average_price=None,
        )

        # Save stats and products to json file
        DataHandling.save_data_to_json(asdict(DataHandling.stats), DataHandling.products, search_term=search_term)

        # Clear class variables
        DataHandling.products.clear()

    # Extracts the text from the specified html tags
    def get_text(result: Node, identifier: str) -> str | None:
        result = result.css_first(f'{identifier}')

        if result == None:
            return None
        else:
            return result.text()

    def save_data_to_json(*args, search_term) -> None:
        file_name = search_term
        file_location = FileUtilities.get_dataset_path()

        file_path = DataHandling.get_file_path(file_location, file_name)

        with open(file_path, 'w', encoding="utf-8") as f:
            save_data = []

            for arg in args:
                save_data.append(arg)

            json.dump(save_data, f, ensure_ascii=False, indent=4)

        console_message("Products saved to Json file.")

    def get_file_path(file_location: str, file_name: str) -> str:
        index = 1
        file_path = f'{file_location}{file_name}-{index}.json'
        while os.path.exists(file_path):
            index += 1
            file_path = f'{file_location}{file_name}-{index}.json'

        return file_path


def console_message(message: str) -> None:
    if BrowserInteraction.gui_instance == None:
        print(message)
    else:
        scraper_gui.App.display_to_console(BrowserInteraction.gui_instance, message)


def run_scraper(search_term, gui_instance=None, pages=1):
    BrowserInteraction.gui_instance = gui_instance

    with sync_playwright() as playwright:
        BrowserInteraction.run_browser(playwright, search_term, pages)


if __name__ == '__main__':
    BrowserInteraction.gui_instance = False
    run_scraper('Running shoes', pages=2)
