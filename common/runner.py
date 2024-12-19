from typing import Literal, Sequence, overload

from common.metadata import Metadata
from common.runners.naive import run_naive
from common.runners.python import run_python
from common.runners.run import BenchRun, Run, SimpleRun
from common.template import Language


@overload
def run_day(
    year: int, day: int, metadata: Metadata, benchmark: Literal[False]
) -> Sequence[SimpleRun]: ...


@overload
def run_day(
    year: int, day: int, metadata: Metadata, benchmark: Literal[True]
) -> Sequence[BenchRun]: ...


def run_day(
    year: int, day: int, metadata: Metadata, benchmark: bool = False
) -> Sequence[Run]:
    match metadata.language:
        case Language.PYTHON:
            return run_python(year, day, metadata, benchmark)
        case _:
            if benchmark:
                raise NotImplementedError(
                    "Benchmarking is not supported for this language"
                )

            return run_naive(year, day, metadata)
