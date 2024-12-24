from part_1 import Gate, Operation, gates_wires, get_number


def find_output_wire(
    left: str, right: str, operation: Operation, gates: list[Gate]
) -> str | None:
    for g in gates:
        if g.left == left and g.right == right and g.operation == operation:
            return g.output_wire

        if g.left == right and g.right == left and g.operation == operation:
            return g.output_wire

    return None


def full_adder_logic(
    x: str, y: str, c0: str | None, gates: list[Gate], swapped: list
) -> tuple[str | None, str | None]:
    """
    Full Adder Logic:
    A full adder adds three one-bit numbers (X1, Y1, and carry-in C0) and outputs a sum bit (Z1) and a carry-out bit (C1).
    The logic for a full adder is as follows:
    - X1 XOR Y1 -> M1 (intermediate sum)
    - X1 AND Y1 -> N1 (intermediate carry)
    - C0 AND M1 -> R1 (carry for intermediate sum)
    - C0 XOR M1 -> Z1 (final sum)
    - R1 OR N1 -> C1 (final carry)

    Args:
    - x: input wire x
    - y: input wire y
    - c0: input carry
    - gates: list of gates
    - swapped: list of swapped wires

    Returns:
    - z1: final sum
    - c1: final carry

    References:
    - https://www.geeksforgeeks.org/full-adder/
    - https://www.geeksforgeeks.org/carry-look-ahead-adder/
    - https://en.wikipedia.org/wiki/Adder_(electronics)#Full_adder
    """

    # X1 XOR Y1 -> M1 (intermediate sum)
    m1 = find_output_wire(x, y, Operation.XOR, gates)

    # X1 AND Y1 -> N1 (intermediate carry)
    n1 = find_output_wire(x, y, Operation.AND, gates)

    assert m1 is not None, f"m1 is None for {x}, {y}"
    assert n1 is not None, f"n1 is None for {x}, {y}"

    if c0 is not None:
        # C0 AND M1 -> R1 (carry for intermediate sum)
        r1 = find_output_wire(c0, m1, Operation.AND, gates)
        if not r1:
            n1, m1 = m1, n1
            swapped.append(m1)
            swapped.append(n1)
            r1 = find_output_wire(c0, m1, Operation.AND, gates)

        # C0 XOR M1 -> Z1 (final sum)
        z1 = find_output_wire(c0, m1, Operation.XOR, gates)

        if m1 and m1.startswith("z"):
            m1, z1 = z1, m1
            swapped.append(m1)
            swapped.append(z1)

        if n1 and n1.startswith("z"):
            n1, z1 = z1, n1
            swapped.append(n1)
            swapped.append(z1)

        if r1 and r1.startswith("z"):
            r1, z1 = z1, r1
            swapped.append(r1)
            swapped.append(z1)

        assert r1 is not None, f"r1 is None for {c0}, {m1}"
        assert n1 is not None, f"n1 is None for {c0}, {m1}"

        # R1 OR N1 -> C1 (final carry)
        c1 = find_output_wire(r1, n1, Operation.OR, gates)
    else:
        z1 = m1
        c1 = n1

    return z1, c1


def part_2() -> str:
    wires, gates = gates_wires("input.txt")

    # Populate all wires
    get_number(lambda x: x.startswith("z"), wires, gates)

    c0 = None  # carry
    swapped = []  # list of swapped wires

    bits = len([wire for wire in wires if wire.startswith("x")])
    for i in range(bits):
        n = str(i).zfill(2)
        x = f"x{n}"
        y = f"y{n}"

        z1, c1 = full_adder_logic(x, y, c0, gates, swapped)

        if c1 and c1.startswith("z") and c1 != "z45":
            c1, z1 = z1, c1
            swapped.append(c1)
            swapped.append(z1)

        # update carry
        c0 = c1 if c1 else find_output_wire(x, y, Operation.AND, gates)

    return ",".join(sorted(swapped))
