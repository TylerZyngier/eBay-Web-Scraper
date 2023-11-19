from PIL import Image
import customtkinter as ctk
import subprocess
import os

import console
import scraper
import utils

operation_index = 0


def start_gui():
    root = ctk.CTk()

    root.geometry("600x500")
    root.minsize(width=300, height=200)
    root.title("eBay Web Scraper")
    root.iconbitmap(f"{utils.get_resource_path()}scraper_icon.ico")

    global app
    app = GUI(root)

    console.initialize_console()

    root.mainloop()


# GUI Display
class GUI(ctk.CTk):
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.setup_ui()
        self.layout_ui()

    def setup_ui(self):
        self.container_frame = ctk.CTkFrame(
            self.root, width=50, height=50, fg_color="transparent"
        )

        # Search Controls
        self.header = ctk.CTkLabel(
            self.container_frame,
            text="eBay Web Scraper",
            fg_color="transparent",
            font=("default", 24, "bold"),
        )

        self.search_term_input = ctk.CTkEntry(
            self.container_frame, width=250, placeholder_text="Search..."
        )

        self.page_number_input = ctk.CTkEntry(
            self.container_frame,
            width=30,
            placeholder_text="1",
            validate="all",
            validatecommand=(self.root.register(utils.string_is_digit), "%P"),
        )

        self.scrape_button = ctk.CTkButton(
            self.container_frame,
            width=100,
            text="Scrape Data!",
            command=lambda: EventHandlers.start_scraping(
                utils.string_to_int(self.page_number_input.get()),
                self.search_term_input,
            ),
        )

        # Console
        self.console_label = ctk.CTkLabel(
            self.container_frame,
            text="Ouput Console:",
            fg_color="transparent",
            text_color="gray50",
            font=("default", 11),
        )

        self.open_file_explorer_button = ctk.CTkButton(
            self.container_frame,
            text="",
            width=30,
            height=30,
            image=EventHandlers.get_file_button_icon(),
            command=EventHandlers.open_dataset_file_explorer,
            fg_color="gray14",
            hover_color="gray14",
        )

    def layout_ui(self):
        # Main container frame
        self.container_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Search controls layout
        self.header.grid(row=0, column=0, columnspan=4, pady=(0, 30), sticky="ew")
        self.search_term_input.grid(row=2, column=0, padx=(0, 10), sticky="ew")
        self.search_term_input.bind(
            "<Return>",
            command=EventHandlers.start_scraping(
                utils.string_to_int(self.page_number_input.get()),
                self.search_term_input,
            ),
        )
        self.page_number_input.grid(row=2, column=1, padx=(0, 10), sticky="ew")
        self.scrape_button.grid(row=2, column=2, sticky="e")

        # Console layout
        self.console_label.grid(row=3, column=0, columnspan=4, pady=(8, 0), sticky="sw")
        self.open_file_explorer_button.grid(row=2, column=3, sticky="e")
        self.console = ctk.CTkTextbox(self.container_frame, fg_color="gray20")
        self.console.grid(row=4, column=0, columnspan=4, sticky="nsew")
        self.console.configure(spacing3=5)  # Console text line spacing

        # Grid configuration
        self.container_frame.grid_rowconfigure(4, weight=2)
        self.container_frame.grid_columnconfigure(0, weight=1)


class EventHandlers:
    # Open file explorer to the dataset folder
    def open_dataset_file_explorer():
        path = f"{utils.get_dataset_path()}"
        path = os.path.normpath(path)

        subprocess.run([utils.get_file_explorer_path(), path])

    def get_file_button_icon() -> ctk.CTkImage:
        icon_path = f"{utils.get_resource_path()}file_icon.png"

        if os.path.exists(icon_path):
            file_button_image = ctk.CTkImage(
                light_image=Image.open(icon_path),
                dark_image=Image.open(icon_path),
                size=(20, 20),
            )

            return file_button_image
        else:
            print(
                "Can't find file button icon in resource folder, perhaps its missing or incorrectly named?"
            )

            return None

    def start_scraping(page_amount: int, search_term_input: ctk.CTkEntry):
        search_string = search_term_input.get()
        search_terms = [search_string]

        # Clear the search bar after saving the search term input string
        search_term_input.delete(0, "end")

        # If the search term is either empty or only contains spaces, return
        if search_string == "" or search_string.isspace() == True:
            return

        # Seperate the search terms (where there is a comma) and put them in a list
        if search_string.find(",") != -1:
            search_terms = search_string.split(",")

        if page_amount == "":
            page_amount = 1

        for term in search_terms:
            # console_log(
            #     f"Scraping Operation ({operation_index}): {term}", header=True
            # )
            print("Started scraping operation")
            scraper.start_scraper(term, page_amount)
