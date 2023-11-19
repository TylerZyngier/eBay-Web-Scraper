import gui


def initialize_console():   
    global __console
    __console = gui.app.console

def log_header(message):
    if first_in_console() == False:
        message = f'\n{message}'
    __log(f"{message}")

def log(message):
    __log(f">  {message}")

def __log(message):
    __console.insert("end", f"{message}\n")  # Put message at end of console
    __console.see("end")  # Scroll to bottom of console
    __console.update()  # Update GUI

    print(message)

def first_in_console():
    return True if len(__console.get('0.0', 'end-1c')) == 0 else False