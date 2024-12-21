import unittest

from grid import Grid
from point import Point


class TestGrid2D(unittest.TestCase):
    def setUp(self):
        self.grid = Grid[int](dimensions=2)
        self.point1 = Point((1, 1))
        self.point2 = Point((2, 2))
        self.grid.add_point(self.point1, 5)
        self.grid.add_point(self.point2, 10)

    def test_add_point(self):
        self.assertEqual(self.grid.get_value(self.point1), 5)
        self.assertEqual(self.grid.get_value(self.point2), 10)

    def test_find_point(self):
        self.assertEqual(self.grid.find_point(5), self.point1)
        self.assertEqual(self.grid.find_point(10), self.point2)
        self.assertIsNone(self.grid.find_point(15))

    def test_find_points(self):
        points = list(self.grid.find_points(5))
        self.assertEqual(points, [self.point1])
        points = list(self.grid.find_points(10))
        self.assertEqual(points, [self.point2])
        points = list(self.grid.find_points(15))
        self.assertEqual(points, [])

    def test_set_value(self):
        self.grid.set_value(self.point1, 15)
        self.assertEqual(self.grid.get_value(self.point1), 15)

    def test_neighbors(self):
        neighbors = self.grid.neighbors(self.point1)
        expected_neighbors = [
            Point((0, 0)),
            Point((0, 1)),
            Point((0, 2)),
            Point((1, 0)),
            Point((1, 2)),
            Point((2, 0)),
            Point((2, 1)),
            Point((2, 2)),
        ]

        self.assertEqual(sorted(neighbors), sorted(expected_neighbors))

    def test_cardinal_neighbors(self):
        neighbors = list(self.grid.cardinal_neighbors(self.point1))
        expected_neighbors = [
            Point((0, 1)),
            Point((1, 0)),
            Point((1, 2)),
            Point((2, 1)),
        ]

        self.assertEqual(sorted(neighbors), sorted(expected_neighbors))

    def test_size(self):
        self.assertEqual(self.grid.size, 2)

    def test_shape(self):
        self.assertEqual(self.grid.shape, (2, 2))

    def test_center(self):
        self.assertEqual(self.grid.center, Point((1, 1)))

    def test_bounds(self):
        self.assertEqual(self.grid.bounds, (Point((1, 1)), Point((2, 2))))

    def test_is_inside(self):
        self.assertTrue(self.grid.is_inside(Point((1, 1))))
        self.assertTrue(self.grid.is_inside(Point((2, 2))))
        self.assertFalse(self.grid.is_inside(Point((0, 0))))
        self.assertFalse(self.grid.is_inside(Point((3, 3))))

    def test_manhattan_distance(self):
        self.assertEqual(self.grid.manhattan_distance(Point((0, 0)), Point((3, 4))), 7)

    def test_euclidean_distance(self):
        self.assertAlmostEqual(
            self.grid.euclidean_distance(Point((0, 0)), Point((3, 4))), 5.0
        )


class TestGrid3D(unittest.TestCase):
    def setUp(self):
        self.grid = Grid[int](dimensions=3)
        self.point1 = Point((1, 1, 1))
        self.point2 = Point((2, 2, 2))
        self.grid.add_point(self.point1, 5)
        self.grid.add_point(self.point2, 10)

    def test_add_point(self):
        self.assertEqual(self.grid.get_value(self.point1), 5)
        self.assertEqual(self.grid.get_value(self.point2), 10)

    def test_find_point(self):
        self.assertEqual(self.grid.find_point(5), self.point1)
        self.assertEqual(self.grid.find_point(10), self.point2)
        self.assertIsNone(self.grid.find_point(15))

    def test_find_points(self):
        points = list(self.grid.find_points(5))
        self.assertEqual(points, [self.point1])
        points = list(self.grid.find_points(10))
        self.assertEqual(points, [self.point2])
        points = list(self.grid.find_points(15))
        self.assertEqual(points, [])

    def test_set_value(self):
        self.grid.set_value(self.point1, 15)
        self.assertEqual(self.grid.get_value(self.point1), 15)

    def test_neighbors(self):
        neighbors = self.grid.neighbors(self.point1)
        expected_neighbors = [
            Point((0, 0, 0)),
            Point((0, 0, 1)),
            Point((0, 0, 2)),
            Point((0, 1, 0)),
            Point((0, 1, 1)),
            Point((0, 1, 2)),
            Point((0, 2, 0)),
            Point((0, 2, 1)),
            Point((0, 2, 2)),
            Point((1, 0, 0)),
            Point((1, 0, 1)),
            Point((1, 0, 2)),
            Point((1, 1, 0)),
            Point((1, 1, 2)),
            Point((1, 2, 0)),
            Point((1, 2, 1)),
            Point((1, 2, 2)),
            Point((2, 0, 0)),
            Point((2, 0, 1)),
            Point((2, 0, 2)),
            Point((2, 1, 0)),
            Point((2, 1, 1)),
            Point((2, 1, 2)),
            Point((2, 2, 0)),
            Point((2, 2, 1)),
            Point((2, 2, 2)),
        ]

        self.assertEqual(sorted(neighbors), sorted(expected_neighbors))

    def test_cardinal_neighbors(self):
        neighbors = list(self.grid.cardinal_neighbors(self.point1))
        expected_neighbors = [
            Point((0, 1, 1)),
            Point((1, 0, 1)),
            Point((1, 1, 0)),
            Point((1, 1, 2)),
            Point((1, 2, 1)),
            Point((2, 1, 1)),
        ]

        self.assertEqual(sorted(neighbors), sorted(expected_neighbors))

    def test_size(self):
        self.assertEqual(self.grid.size, 2)

    def test_shape(self):
        self.assertEqual(self.grid.shape, (2, 2, 2))

    def test_center(self):
        self.assertEqual(self.grid.center, Point((1, 1, 1)))

    def test_bounds(self):
        self.assertEqual(self.grid.bounds, (Point((1, 1, 1)), Point((2, 2, 2))))

    def test_is_inside(self):
        self.assertTrue(self.grid.is_inside(Point((1, 1, 1))))
        self.assertTrue(self.grid.is_inside(Point((2, 2, 2))))
        self.assertFalse(self.grid.is_inside(Point((0, 0, 0))))
        self.assertFalse(self.grid.is_inside(Point((3, 3, 3))))

    def test_manhattan_distance(self):
        self.assertEqual(
            self.grid.manhattan_distance(Point((0, 0, 0)), Point((3, 4, 5))), 12
        )

    def test_euclidean_distance(self):
        self.assertAlmostEqual(
            self.grid.euclidean_distance(Point((0, 0, 0)), Point((3, 4, 5))),
            7.0710678118654755,
        )


if __name__ == "__main__":
    unittest.main()
