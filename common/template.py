from enum import Enum
from pathlib import Path
from typing import NamedTuple


class LanguageConfig(NamedTuple):
    name: str
    extension: str


class Language(Enum):
    PYTHON = LanguageConfig("python", "py")

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self.value.name

    @property
    def extension(self) -> str:
        return self.value.extension

    @classmethod
    def from_name(cls, name: str) -> "Language":
        return cls[name.upper()]


def get_template(language: Language, func_name: str | None = None) -> str:
    template_path = (
        Path(__file__).parent
        / "templates"
        / f"{language}{".alone" if func_name else ""}.tmpl"
    )

    try:
        with open(template_path) as file:
            content = file.read()
            if func_name:
                return content.format(func_name=func_name)
            else:
                return content
    except FileNotFoundError:
        return ""
