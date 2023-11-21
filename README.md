# eBay Web Scraper
Allows you to enter search term(s) and recieve a dataset of product info scraped from eBay.
I use this to build datasets to practice data science/market analysis

This is a personal project to practice webscraping and software development.

## Usage
After getting everything setup and installing 
Datasets are stored as .json files in the Datasets folder.
Run the main.py file to start the GUI scraper.

### Python Packages
- Selectolax
- Packaging
- CustomTkinter
- Playwright
- Pillow

### Setup (Windows)
1. Clone this repo in your preferred working directory
  ```
  git clone https://github.com/TylerZyngier/eBay-Web-Scraper.git
  ```
3. Update python and create a virtual environment
  ```
  python.exe -m pip install --upgrade pip
  python -m venv .venv
  .\.venv\scripts\activate.bat
  ```
4. Install packages
  ```
  pip install selectolax
  pip install packaging
  pip install customtkinter
  pip install playwright
  pip install pillow
  
  playwright install
  ```

Be aware, there are probably many bugs and some things aren't implemented yet. I need some more time for that @~@

![image](https://user-images.githubusercontent.com/60865749/284098566-698cd474-dd98-401d-be7d-8e1390684fbb.png)
