from dataclasses import dataclass, field
from typing import (
    Callable,
    Dict,
    Generator,
    Generic,
    List,
    Optional,
    Tuple,
    TypeVar,
    cast,
)

from utils.point import Point

T = TypeVar("T")


@dataclass
class Grid(Generic[T]):
    dimensions: int
    points: Dict[Tuple[int, ...], T] = field(default_factory=dict)

    _min_point: Optional[Point] = field(init=False, default=None)
    _max_point: Optional[Point] = field(init=False, default=None)
    _bounds_dirty: bool = field(default=True, init=False, repr=False)

    def add_point(self, point: Point, value: T) -> None:
        """Add a point to the grid with a value"""
        self.__check_dimensions(point)

        self.points[point.coords] = value
        self._bounds_dirty = True

    def find_point(self, value: T) -> Optional[Point]:
        """Find the first point with a specific value"""

        for coords, val in self.points.items():
            if val == value:
                return Point(coords)

    def find_points(self, value: T) -> Generator[Point, None, None]:
        """Find all points with a specific value"""

        for coords, val in self.points.items():
            if val == value:
                yield Point(coords)

    def get_value(self, point: Point) -> Optional[T]:
        """Get the value at a specific point"""
        self.__check_dimensions(point)

        return self.points.get(point.coords)

    def set_value(self, point: Point, value: T) -> None:
        """Set the value at a specific point"""
        self.__check_dimensions(point)

        self.points[point.coords] = value
        self._bounds_dirty = True

    def neighbors(self, point: Point) -> List[Point]:
        """Get all neighbors of a point (including diagonals)"""
        self.__check_dimensions(point)

        return list(point.neighbors())

    def cardinal_neighbors(self, point: Point) -> Generator[Point, None, None]:
        """Get the cardinal neighbors of a point"""
        self.__check_dimensions(point)

        return point.cardinal_neighbors()

    def __check_dimensions(self, point: Point) -> None:
        """Check if a point has the correct number of dimensions"""
        assert (
            point.dimensions() == self.dimensions
        ), "Point dimensions do not match grid dimensions"

    @property
    def size(self) -> int:
        """Return the number of points in the grid"""
        return len(self.points)

    @property
    def shape(self) -> Tuple[int, ...]:
        """
        Return the shape of the grid as a tuple of dimensions.

        This is an expensive operation and should be used sparingly.
        """

        if not self.points:
            return tuple(0 for _ in range(self.dimensions))

        min_coords = [
            min(coords[i] for coords in self.points) for i in range(self.dimensions)
        ]

        max_coords = [
            max(coords[i] for coords in self.points) for i in range(self.dimensions)
        ]

        return tuple(max_coords[i] - min_coords[i] + 1 for i in range(self.dimensions))

    @property
    def center(self) -> Point:
        """
        Return the center point of the grid

        This is an expensive operation and should be used sparingly.
        """

        if not self.points:
            return Point.zero(self.dimensions)

        min_coords = [
            min(coords[i] for coords in self.points) for i in range(self.dimensions)
        ]

        max_coords = [
            max(coords[i] for coords in self.points) for i in range(self.dimensions)
        ]

        center_coords = tuple(
            (min_coords[i] + max_coords[i]) // 2 for i in range(self.dimensions)
        )

        return Point(center_coords)

    def bounds(self) -> Tuple[Point, Point]:
        """
        Return the bounding box of the grid as a tuple of two points (min and max)

        This is an expensive operation and should be used sparingly.
        """

        if not self.points:
            return (Point.zero(self.dimensions), Point.zero(self.dimensions))

        if not self._bounds_dirty and self._min_point and self._max_point:
            return (self._min_point, self._max_point)

        min_coords = tuple(
            min(coords[i] for coords in self.points) for i in range(self.dimensions)
        )
        max_coords = tuple(
            max(coords[i] for coords in self.points) for i in range(self.dimensions)
        )

        self._min_point = Point(min_coords)
        self._max_point = Point(max_coords)
        self._bounds_dirty = False

        return (Point(min_coords), Point(max_coords))

    def is_inside(self, point: Point) -> bool:
        """Check if a point is inside the grid bounds"""
        self.__check_dimensions(point)

        min_point, max_point = self.bounds()

        if self.dimensions == 2:
            return (
                min_point.x() <= point.x() <= max_point.x()
                and min_point.y() <= point.y() <= max_point.y()
            )

        return all(
            min_point[i] <= point[i] <= max_point[i] for i in range(self.dimensions)
        )

    def manhattan_distance(self, point1: Point, point2: Point) -> int:
        """Calculate the Manhattan distance between two points"""
        self.__check_dimensions(point1)
        self.__check_dimensions(point2)

        return point1.manhattan_distance(point2)

    def euclidean_distance(self, point1: Point, point2: Point) -> float:
        """Calculate the Euclidean distance between two points"""
        self.__check_dimensions(point1)
        self.__check_dimensions(point2)

        return point1.euclidean_distance_squared(point2) ** 0.5

    @classmethod
    def from_string(cls, string: str, value_map: Callable[[str], T]) -> "Grid[T]":
        """Create a  2d grid from a string representation"""

        lines = string.strip().split("\n")

        grid = cls(2)

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                point = Point.from_values(x, y)
                value = value_map(char)
                grid.add_point(point, value)

        return grid

    @classmethod
    def from_list(
        cls, values: List[str], remapper: Optional[Callable[[str], T]] = None
    ) -> "Grid[T]":
        """Create a 2d grid from a list of lists"""

        grid = cls(2)

        for y, line in enumerate(values):
            for x, value in enumerate(line):
                point = Point.from_values(x, y)
                grid.add_point(point, remapper(value) if remapper else cast(T, value))

        return grid

    def __str__(self) -> str:
        if not self.points:
            return ""

        min_point, max_point = self.bounds()
        min_coords = min_point.coords
        max_coords = max_point.coords

        def generate_slices(dim: int, prefix: Tuple[int, ...]) -> str:
            if dim == 2:
                grid_str = []
                for y in range(min_coords[-2], max_coords[-2] + 1):
                    row = []
                    for x in range(min_coords[-1], max_coords[-1] + 1):
                        point = prefix + (x, y)
                        if point in self.points:
                            row.append(str(self.points[point]))
                        else:
                            row.append(" ")
                    grid_str.append("".join(row))
                return "\n".join(grid_str)
            else:
                slices = []
                for i in range(min_coords[-dim], max_coords[-dim] + 1):
                    slice_str = generate_slices(dim - 1, prefix + (i,))
                    slices.append(
                        f"Dimension {self.dimensions - dim + 1} = {i}\n{slice_str}"
                    )
                return "\n\n".join(slices)

        return generate_slices(self.dimensions, ())
