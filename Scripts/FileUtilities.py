import os


def get_working_path() -> str:
    return f'{os.path.abspath(os.getcwd())}'


def get_resource_folder() -> str:
    return f"{get_working_path()}\\Resources\\"


def get_dataset_path():
    return f"{get_working_path()}\\Datasets\\"
