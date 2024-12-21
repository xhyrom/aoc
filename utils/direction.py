from enum import Enum
from typing import Tuple


class Direction(Enum):
    NORTH = (0, (0, 1))
    EAST = (90, (1, 0))
    SOUTH = (180, (0, -1))
    WEST = (270, (-1, 0))

    def __init__(self, angle: int, vector: Tuple[int, int]):
        self.angle = angle
        self.vector = vector

    @property
    def opposite(self) -> "Direction":
        return self.rotate(180)

    @property
    def clockwise(self) -> "Direction":
        return self.rotate(90)

    @property
    def counterclockwise(self) -> "Direction":
        return self.rotate(-90)

    def rotate(self, angle: int) -> "Direction":
        new_angle = (self.angle + angle) % 360
        return self.from_angle(new_angle)

    @classmethod
    def from_angle(cls, angle: int) -> "Direction":
        normalized_angle = angle % 360
        for direction in cls:
            if direction.angle == normalized_angle:
                return direction

        raise ValueError(f"No direction for angle {angle}")
