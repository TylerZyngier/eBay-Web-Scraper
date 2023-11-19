import os

debug = False


# Return the file path to file explorer's .exe file
def get_file_explorer_path():
    return os.path.join(os.getenv("WINDIR"), "explorer.exe")


# Return the file path to the project/workspace folder
def get_working_path() -> str:
    working_path = f"{os.path.abspath(os.getcwd())}"

    if debug:
        DebugLog("get_working_path", f"Project Working Path: {working_path}")

    return working_path


# Return the file path to the resources folder
def get_resource_path() -> str:
    resource_path = f"{get_working_path()}\\Resources\\"
    resource_path_exists = os.path.exists(resource_path)

    if debug:
        if resource_path_exists:
            DebugLog("get_resource_path", f"Found resource path! ({resource_path})")
        else:
            DebugLog("get_resource_path", f"Resource path not found! ({resource_path})")

    if resource_path_exists == False:
        os.mkdir(resource_path)
        DebugLog("get_resource_path", f"Created resources folder ({resource_path})")

    return resource_path


# Return the file path to the dataset folder
def get_dataset_path():
    dataset_path = f"{get_working_path()}\\Datasets\\"

    if debug:
        DebugLog("get_dataset_path", dataset_path)

    return dataset_path


# Convert a string to an integer
def string_to_int(string) -> int:
    return "".join(filter(str.isdigit, string))


# Verify whether or not a string only includes numbers
def string_is_digit(string):
    if str.isdigit(string) or string == "":
        return True
    else:
        return False


def DebugLog(source_method, message):
    current_file_name = os.path.basename(__file__)
    print(f"{current_file_name} -> {source_method}: {message}")
