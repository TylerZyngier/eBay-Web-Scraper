from selectolax.parser import Node
from dataclasses import dataclass, asdict

import console
import utils
import json
import os


@dataclass
class Stats:
    search_term: str | None
    results: str | None
    pages: str | None
    average_price: float | None
    lowest_price: float | None
    highest_price: float | None


@dataclass
class Product:
    name: str | None
    price: str | None
    discount: str | None
    page_number: int | None


products = []
stats = Stats

def add_to_product_list(product_list: list[Node], page_number: int) -> None:
    # Save products to list
    for product_info in product_list:
        product = Product(
            name=get_text(product_info, "span[role=heading]"),
            price=get_text(product_info, "span[class=s-item__price]"),
            discount=get_text(product_info, 'span[class="s-item__discount s-item__discount"]'),
            page_number=page_number,
        )

        products.append(asdict(product))

# Once all the product results are added to a list, save the list to a json file
def save_product_info(search_term, page_number):
    # Save Stats
    stats = Stats(
        search_term=search_term,
        results=len(products),
        pages=page_number,
        lowest_price=None,
        highest_price=None,
        average_price=None,
    )

    # Save stats and products to json file
    save_data_to_json(asdict(stats), products, search_term=search_term)

    # Clear class variables
    products.clear()

    console.log(f"Saved data from {stats.results} results across {stats.pages} {'page' if stats.pages == 1 else 'pages'}")


# Extracts the text from within the specified html tags
def get_text(result: Node, identifier: str) -> str | None:
    result = result.css_first(f"{identifier}")

    if result == None:
        return None
    else:
        return result.text()


def save_data_to_json(*args, search_term) -> None:
    file_name = search_term
    file_location = utils.get_dataset_path()

    file_path = get_file_path(file_location, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        save_data = []

        for arg in args:
            save_data.append(arg)

        json.dump(save_data, f, ensure_ascii=False, indent=4)

    # console_log("Products saved to Json file.")


def get_file_path(file_location: str, file_name: str) -> str:
    index = 1
    file_path = f"{file_location}{file_name}-{index}.json"
    while os.path.exists(file_path):
        index += 1
        file_path = f"{file_location}{file_name}-{index}.json"

    return file_path
