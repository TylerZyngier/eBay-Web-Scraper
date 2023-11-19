:: Run these groups seperately
python.exe -m pip install --upgrade pip
python -m venv .venv
.\.venv\scripts\activate.bat

:: Make sure you run these within your virutal environment terminal 
:: unless you'd like to install these packages to your system
pip install selectolax
pip install dataclasses
pip install packaging
pip install customtkinter
pip install playwright
pip install subprocess
pip install pillow

playwright install