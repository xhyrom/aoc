from enum import Enum
from pathlib import Path
from typing import NamedTuple


class LanguageConfig(NamedTuple):
    name: str
    extension: str
    commands: list[str] | None = None


class Language(Enum):
    PYTHON = LanguageConfig("python", "py")
    CRYSTAL = LanguageConfig("crystal", "cr", ["crystal run {file}"])
    DART = LanguageConfig("dart", "dart", ["dart {file}"])
    GO = LanguageConfig("go", "go", ["go run {file}"])
    JAVA = LanguageConfig("java", "java", ["java {file}"])
    JAVASCRIPT = LanguageConfig(
        "javascript", "js", ["bun {file}", "node {file}", "deno {file}"]
    )
    LUA = LanguageConfig("lua", "lua", ["lua {file}"])
    RUBY = LanguageConfig("ruby", "rb", ["ruby {file}"])
    RUST = LanguageConfig("rust", "rs", ["chmod u+x {file} && {file}"])
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

    @classmethod
    def from_extension(cls, extension: str) -> "Language":
        for lang in cls:
            if lang.extension == extension:
                return lang

        return cls.PYTHON


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
