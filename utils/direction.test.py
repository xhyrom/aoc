from direction import Direction


def test_opposite():
    assert Direction.NORTH.opposite == Direction.SOUTH
    assert Direction.EAST.opposite == Direction.WEST
    assert Direction.SOUTH.opposite == Direction.NORTH
    assert Direction.WEST.opposite == Direction.EAST


def test_clockwise():
    assert Direction.NORTH.clockwise == Direction.EAST
    assert Direction.EAST.clockwise == Direction.SOUTH
    assert Direction.SOUTH.clockwise == Direction.WEST
    assert Direction.WEST.clockwise == Direction.NORTH


def test_counterclockwise():
    assert Direction.NORTH.counterclockwise == Direction.WEST
    assert Direction.WEST.counterclockwise == Direction.SOUTH
    assert Direction.SOUTH.counterclockwise == Direction.EAST
    assert Direction.EAST.counterclockwise == Direction.NORTH


def test_rotate():
    assert Direction.NORTH.rotate(90) == Direction.EAST
    assert Direction.NORTH.rotate(180) == Direction.SOUTH
    assert Direction.NORTH.rotate(270) == Direction.WEST
    assert Direction.NORTH.rotate(360) == Direction.NORTH
    assert Direction.NORTH.rotate(-90) == Direction.WEST
    assert Direction.NORTH.rotate(-180) == Direction.SOUTH
    assert Direction.NORTH.rotate(-270) == Direction.EAST
    assert Direction.NORTH.rotate(-360) == Direction.NORTH


def test_from_angle():
    assert Direction.from_angle(0) == Direction.NORTH
    assert Direction.from_angle(90) == Direction.EAST
    assert Direction.from_angle(180) == Direction.SOUTH
    assert Direction.from_angle(270) == Direction.WEST
    assert Direction.from_angle(360) == Direction.NORTH
    assert Direction.from_angle(-90) == Direction.WEST
    assert Direction.from_angle(450) == Direction.EAST


def test_invalid_angle():
    try:
        Direction.from_angle(45)
    except ValueError as e:
        assert str(e) == "No direction for angle 45"
    else:
        assert False, "Expected ValueError for angle 45"


if __name__ == "__main__":
    test_opposite()
    test_clockwise()
    test_counterclockwise()
    test_rotate()
    test_from_angle()
    test_invalid_angle()
    print("All tests passed!")
