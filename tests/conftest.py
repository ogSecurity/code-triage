import os


def folder_exits(folder: str) -> bool:
    """Check if a folder exists

    :param folder: Path to the folder to check
    :return: True if the folder exists, False otherwise
    """
    return os.path.exists(folder)


def folder_empty(folder: str) -> bool:
    """Check if a folder is empty

    :param folder: Path to the folder to check
    :return: True if the folder is empty, False otherwise
    """
    return len(os.listdir(folder)) == 0
