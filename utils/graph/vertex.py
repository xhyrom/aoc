from dataclasses import dataclass
from typing import Generic, TypeVar

from utils.point import Point

T = TypeVar("T")


@dataclass
class Vertex(Generic[T]):
    position: Point
    value: T

    def __str__(self) -> str:
        return f"Vertex({self.position}, {self.value})"

    def __repr__(self) -> str:
        return str(self)
