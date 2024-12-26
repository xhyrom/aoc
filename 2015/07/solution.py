from abc import abstractmethod
from dataclasses import dataclass
from typing import Any


class Instruction:
    output: str

    @abstractmethod
    def emulate(self, registry: dict[str, int]):
        raise NotImplementedError

    @abstractmethod
    def required(self) -> set[str]:
        raise NotImplementedError

    @staticmethod
    def parse(line: str) -> "Instruction":
        exp, output = line.split(" -> ")

        if " " not in exp:
            return Wire(exp, output)

        if exp.startswith("NOT"):
            return Unary(exp[4:], output, "NOT")

        left, operation, right = exp.split()
        return Gate(left, right, output, operation)

    def member(self, member: str, registry: dict[str, int]) -> int:
        if member.isnumeric():
            return int(member)

        return registry[member]


@dataclass
class Gate(Instruction):
    left: str
    right: str
    output: str
    operation: str

    def emulate(self, registry: dict[str, int]):
        registry[self.output] = (
            self._operation(
                self.member(self.left, registry), self.member(self.right, registry)
            )
            & 0xFFFF
        )

    def required(self) -> set[str]:
        if self.left.isnumeric():
            return {self.right}

        if self.right.isnumeric():
            return {self.left}

        return {self.left, self.right}

    def _operation(self, left: int, right: int) -> int:
        match self.operation:
            case "AND":
                return left & right
            case "OR":
                return left | right
            case "LSHIFT":
                return left << right
            case "RSHIFT":
                return left >> right

        raise ValueError(f"Invalid operation: {self.operation}")


@dataclass
class Wire(Instruction):
    signal: str
    output: str

    def emulate(self, registry: dict[str, int]):
        registry[self.output] = self.member(self.signal, registry) & 0xFFFF

    def required(self) -> set[str]:
        if self.signal.isnumeric():
            return set()

        return {self.signal}


@dataclass
class Unary(Instruction):
    value: str
    output: str
    operation: str

    def emulate(self, registry: dict[str, int]):
        registry[self.output] = (
            self._operation(self.member(self.value, registry)) & 0xFFFF
        )

    def required(self) -> set[str]:
        if self.value.isnumeric():
            return set()

        return {self.value}

    def _operation(self, value: int) -> int:
        return ~value


def emulate(instructions: list[Instruction], registry: dict[str, int]):
    instruction_map = {instr.output: instr for instr in instructions}

    def resolve(output: str):
        if output in registry:
            return

        instruction = instruction_map[output]
        required = instruction.required()
        for req in required:
            if req not in registry:
                resolve(req)

        instruction.emulate(registry)

    for instruction in instructions:
        resolve(instruction.output)


def part_1() -> Any:
    circuit: list[Instruction] = list(
        map(Instruction.parse, open("input.txt").read().splitlines())
    )
    registry = {}

    emulate(circuit, registry)

    return registry["a"]


def part_2() -> Any:
    circuit: list[Instruction] = list(
        map(Instruction.parse, open("input.txt").read().splitlines())
    )
    registry = {}

    emulate(circuit, registry)

    a = registry["a"]
    circuit = list(filter(lambda instr: instr.output != "b", circuit))
    circuit.append(Wire(str(a), "b"))

    registry = {}
    emulate(circuit, registry)

    return registry["a"]
