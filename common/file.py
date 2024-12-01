from os import makedirs
from os.path import exists


def save_to_day(
    year: int, day: int, file_name: str, file_content: str, overwrite: bool = True
) -> None:
    """Saves the file content to the given day and year"""
    file_path = f"./{year}/{day:02}/{file_name}"

    if not overwrite and exists(file_path):
        return

    with open(file_path, "w") as f:
        f.write(file_content)


def create_day(year: int, day: int) -> None:
    """Creates a new day folder for the given year and day"""
    makedirs(f"./{year}/{day:02}", exist_ok=True)
