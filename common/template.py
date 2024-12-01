from enum import Enum
from pathlib import Path
from typing import NamedTuple


class LanguageConfig(NamedTuple):
    name: str
    extension: str
    commands: list[str] | None = None


class Language(Enum):
    PYTHON = LanguageConfig("python", "py")
    JAVASCRIPT = LanguageConfig(
        "javascript", "js", ["bun {file}", "node {file}", "deno {file}"]
    )
    TYPESCRIPT = LanguageConfig(
        "typescript",
        "ts",
        ["bun {file}", "node --experimental-strip-types {file}", "deno {file}"],
    )

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self.value.name

    @property
    def extension(self) -> str:
        return self.value.extension

    @property
    def commands(self) -> list[str] | None:
        return self.value.commands

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
            content = file.read().strip()
            if func_name:
                return content.replace("{func_name}", func_name)
            else:
                return content
    except FileNotFoundError:
        return ""
