from common.metadata import Metadata
from common.runners.naive import run_naive
from common.runners.python import run_python
from common.runners.run import Run
from common.template import Language


def run_day(year: int, day: int, metadata: Metadata) -> list[Run]:
    match metadata.language:
        case Language.PYTHON:
            return run_python(year, day, metadata)
        case _:
            return run_naive(year, day, metadata)
