from dataclasses import dataclass
from enum import Enum
from typing import Callable


class Operation(Enum):
    AND = 1
    OR = 2
    XOR = 3

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


@dataclass
class Gate:
    left: str
    right: str
    output_wire: str
    operation: Operation

    def perform_operation(self, wires: dict[str, int]) -> int:
        left, right = wires.get(self.left), wires.get(self.right)
        if left is None:
            return -1

        if right is None:
            return -2

        if self.operation == Operation.AND:
            return left & right
        elif self.operation == Operation.OR:
            return left | right
        elif self.operation == Operation.XOR:
            return left ^ right
        else:
            raise ValueError(f"Invalid operation: {self.operation}")


def find_value(value: str, wires: dict[str, int], gates: list[Gate]) -> int:
    if value.isdigit():
        return int(value)

    for g in gates:
        if g.output_wire == value:
            result = g.perform_operation(wires)
            if result == -1:
                left_value = find_value(g.left, wires, gates)
                wires[g.left] = left_value
                return find_value(value, wires, gates)

            elif result == -2:
                right_value = find_value(g.right, wires, gates)
                wires[g.right] = right_value
                return find_value(value, wires, gates)

            return result

    return -1


def gates_wires(file_name: str) -> tuple[dict[str, int], list[Gate]]:
    wires, g = open(file_name).read().split("\n\n")
    wires = {w.split(":")[0]: int(w.split(":")[1]) for w in wires.strip().split("\n")}
    gates = []
    for gate in [wire for wire in g.strip().split("\n")]:
        left, operation, right, _, output_wire = gate.split(" ")
        gates.append(Gate(left, right, output_wire, Operation[operation.upper()]))

    return wires, gates


def get_number(
    filt: Callable[[str], bool], wires: dict[str, int], gates: list[Gate]
) -> int:
    for gate in gates:
        result = gate.perform_operation(wires)
        if result == -1 or result == -2:
            result = find_value(gate.output_wire, wires, gates)
            if result == -1 or result == -2:
                assert False, f"Should never happen: {result}"

        wires[gate.output_wire] = result

    num = 0

    for key in sorted(filter(filt, wires.keys()), reverse=True):
        num = (num << 1) | wires[key]

    return num


def part_1() -> int:
    wires, gates = gates_wires("input.txt")
    return get_number(lambda x: x.startswith("z"), wires, gates)
