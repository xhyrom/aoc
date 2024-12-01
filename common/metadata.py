from dataclasses import dataclass, field
from json import dumps, loads
from os import makedirs

from common.file import save_to_day
from common.template import Language


@dataclass
class Metadata:
    language: Language
    files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"language": str(self.language), "files": self.files}


def save_day_metadata(year: int, day: int, metadata: Metadata) -> None:
    """Saves the metadata for the given day and year"""
    makedirs(f"./{year}/{day:02}/__glint__", exist_ok=True)
    save_to_day(
        year,
        day,
        "__glint__/meta.json",
        dumps(metadata.to_dict()),
    )


def read_day_metadata(year: int, day: int) -> Metadata:
    """Reads the metadata for the given day and year"""

    try:
        with open(f"./{year}/{day:02}/__glint__/meta.json") as f:
            obj = loads(f.read())
            lang = Language.from_name(obj["language"])
            del obj["language"]

            return Metadata(lang, **obj)
    except FileNotFoundError:
        return Metadata(Language.PYTHON, ["first.py", "second.py"])
