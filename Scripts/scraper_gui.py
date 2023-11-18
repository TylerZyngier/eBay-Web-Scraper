import scraper_functions
import FileUtilities
import customtkinter as ctk
import subprocess
import os
from tkinter import PhotoImage
from PIL import Image
from os import listdir
from os.path import isfile, join
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')


# Show table of save files, open save file location button


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.op_index = 1

        self.gui()

    def gui(self):
        def scrape_button_function():
            search_string = search_entry.get()

            # If the search term is either empty or only contains spaces, return
            if search_string == '' or search_string.isspace() == True:
                return

            # Clear the search bar after saving the search input
            search_entry.delete(0, 'end')
            search_terms = [search_string]

            # Seperate the search terms and put them in a list
            if search_string.find(',') != -1:
                search_terms = search_string.split(',')

            # Iterate over the search terms and gather data for each

            pages_to_search = ''.join(filter(str.isdigit, page_number_entry.get()))

            if pages_to_search == '':
                pages_to_search = 1

            for entry in search_terms:
                self.display_to_console(f'Scraping Operation ({self.op_index}): {entry}', new_op=True)
                scraper_functions.run_scraper(entry, self, pages_to_search)

        def view_data_files():
            # explorer would choke on forward slashes
            path = f'{FileUtilities.get_dataset_path()}'
            path = os.path.normpath(path)

            if os.path.isdir(path):
                subprocess.run([FILEBROWSER_PATH, path])
            elif os.path.isfile(path):
                subprocess.run([FILEBROWSER_PATH, '/select,', path])

        # GUI Display
        container = ctk.CTkFrame(self, width=50, height=50, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=30, pady=30)

        header = ctk.CTkLabel(container, text='eBay Web Scraper', fg_color='transparent', font=('default', 24, 'bold'))
        header.grid(row=0, column=0, columnspan=4, sticky='ew', pady=(0, 30))

        search_entry = ctk.CTkEntry(container, width=250, placeholder_text='Search...')
        search_entry.grid(row=2, column=0, padx=(0, 10), sticky='ew')
        search_entry.bind('<Return>', command=scrape_button_function)

        vcmd = (self.register(self.callback))

        page_number_entry = ctk.CTkEntry(container, width=30, placeholder_text='1', validate='all', validatecommand=(vcmd, '%P'))
        page_number_entry.grid(row=2, column=1, padx=(0, 10), sticky='ew')

        scrape_button = ctk.CTkButton(container, width=100, text="Scrape Data!", command=scrape_button_function)
        scrape_button.grid(row=2, column=2, sticky='e')

        console_label = ctk.CTkLabel(container, text='Console Ouput:', fg_color='transparent', text_color='gray50', font=('default', 11))
        console_label.grid(row=3, column=0, columnspan=4, sticky='sw', pady=(8, 0))

        image_path = f'{FileUtilities.get_resource_folder()}file_icon.png'
        file_button_image = ctk.CTkImage(light_image=Image.open(image_path), dark_image=Image.open(image_path), size=(20, 20))

        view_data_button = ctk.CTkButton(container, text='', width=30, height=30, image=file_button_image, command=view_data_files, fg_color='gray14', hover_color='gray14')
        view_data_button.grid(row=2, column=3, sticky='e', ipadx=0, ipady=0)

        self.console = ctk.CTkTextbox(container, fg_color='gray20')
        self.console.grid(row=4, column=0, columnspan=4, sticky='nsew')
        self.console.configure(spacing3=5)

        container.grid_rowconfigure(4, weight=2)
        container.grid_columnconfigure(0, weight=1)

    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def create_list_entry(self, item_name):
        list_item = ctk.CTkFrame(self.file_list_frame, width=50, height=20, fg_color='gray20')
        list_item.pack(padx=5, fill='x')

        file_label = ctk.CTkLabel(list_item, text=item_name)
        file_label.pack(padx=5, fill='x', side='left')

        return list_item

    def display_to_console(self, message, new_op=False):
        if new_op:
            self.op_index += 1

            if len(self.console.get("1.0", "end-1c")) == 0:
                message = f'{message}\n'
            else:
                message = f'\n{message}\n'

        else:
            message = f'>   {message}\n'

        self.console.insert('end', message)
        self.console.see('end')
        self.update()


if __name__ == '__main__':
    app = App()

    ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    app.geometry("600x500")
    app.iconbitmap(f'{FileUtilities.get_resource_folder()}scraper_icon_64x64.ico')
    app.title('eBay Web Scraper')
    app.minsize(width=300, height=200)

    app.mainloop()
