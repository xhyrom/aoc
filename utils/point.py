from dataclasses import dataclass
from itertools import product
from typing import Generator, Tuple, Union


@dataclass(frozen=True)
class Point:
    coords: Tuple[int, ...]

    def __add__(self, other: "Point") -> "Point":
        """Add two points together"""

        self.__check_dimensions(other)

        return Point(tuple(a + b for a, b in zip(self.coords, other.coords)))

    def __sub__(self, other: "Point") -> "Point":
        """Subtract one point from another"""

        self.__check_dimensions(other)

        return Point(tuple(a - b for a, b in zip(self.coords, other.coords)))

    def __mul__(self, other: Union["Point", int]) -> "Point":
        """Multiply a point by another point or an integer"""

        if isinstance(other, Point):
            self.__check_dimensions(other)
            return Point(tuple(a * b for a, b in zip(self.coords, other.coords)))
        elif isinstance(other, int):
            return Point(tuple(a * other for a in self.coords))
        else:
            raise TypeError("Operand must be of type Point or int")

    def __rmul__(self, other: int) -> "Point":
        """Multiply a point by an integer"""

        return self.__mul__(other)

    def __floordiv__(self, other: Union["Point", int]) -> "Point":
        """Floor divide a point by another point or an integer"""

        if isinstance(other, Point):
            self.__check_dimensions(other)
            return Point(tuple(a // b for a, b in zip(self.coords, other.coords)))
        elif isinstance(other, int):
            return Point(tuple(a // other for a in self.coords))
        else:
            raise TypeError("Operand must be of type Point or int")

    def __abs__(self) -> "Point":
        """Absolute value of a point"""

        return Point(tuple(abs(x) for x in self.coords))

    def __neg__(self) -> "Point":
        """Negate a point"""

        return Point(tuple(-x for x in self.coords))

    def __lt__(self, other: "Point") -> bool:
        """Less than comparison for sorting"""

        return self.coords < other.coords

    def __eq__(self, other: object) -> bool:
        """Equality comparison"""

        if not isinstance(other, Point):
            return NotImplemented

        return self.coords == other.coords

    def invert(self) -> "Point":
        return Point(self.coords[::-1])

    def manhattan_distance(self, other: "Point") -> int:
        """Calculate the Manhattan distance between two points"""

        self.__check_dimensions(other)

        return sum(abs(a - b) for a, b in zip(self.coords, other.coords))

    def euclidean_distance_squared(self, other: "Point") -> int:
        """Calculate the squared Euclidean distance between two points"""

        self.__check_dimensions(other)

        return sum((a - b) ** 2 for a, b in zip(self.coords, other.coords))

    def neighbors(self) -> Generator["Point", None, None]:
        """Return the neighbors of the point"""

        for deltas in product([-1, 0, 1], repeat=self.dimensions()):
            if any(deltas):
                yield Point(tuple(a + b for a, b in zip(self.coords, deltas)))

    def cardinal_neighbors(self) -> Generator["Point", None, None]:
        """Return the cardinal neighbors of the point"""

        for i in range(self.dimensions()):
            for sign in (-1, 1):
                neighbor_coords = list(self.coords)
                neighbor_coords[i] += sign
                yield Point(tuple(neighbor_coords))

    def x(self) -> int:
        """Return the x-coordinate of the point"""

        self.__out_of_bounds(0)

        return self.coords[0]

    def y(self) -> int:
        """Return the y-coordinate of the point"""

        self.__out_of_bounds(1)

        return self.coords[1]

    def z(self) -> int:
        """Return the z-coordinate of the point"""

        self.__out_of_bounds(2)

        return self.coords[2]

    def dimensions(self) -> int:
        """Return the number of dimensions of the point"""

        return len(self.coords)

    def __getitem__(self, index: int) -> int:
        """Get the value at a specific index"""

        return self.coords[index]

    def __iter__(self):
        """Iterate over the coordinates of the point"""

        return iter(self.coords)

    def __str__(self) -> str:
        return f"({', '.join(str(x) for x in self.coords)})"

    def __repr__(self) -> str:
        return f"Point{self.coords}"

    def __out_of_bounds(self, dimension: int) -> None:
        assert (
            dimension >= 0 and dimension < self.dimensions()
        ), f"Point does not have dimension {dimension}"

    def __check_dimensions(self, other: "Point") -> None:
        """Check if two points have the same number of dimensions"""

        assert len(self.coords) == len(
            other.coords
        ), "Points must have the same number of dimensions"

    @classmethod
    def zero(cls, dimensions: int) -> "Point":
        return cls(tuple(0 for _ in range(dimensions)))

    @classmethod
    def from_values(cls, *values: int) -> "Point":
        return cls(tuple(values))
