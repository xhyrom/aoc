from enum import Enum


class RegistryDict(dict):
    def __getitem__(self, key):
        return super().__getitem__(key).value

    def __setitem__(self, key, value):
        if isinstance(value, int):
            super().__getitem__(key).value = value
        else:
            super().__setitem__(key, value)


class RegistryType(Enum):
    A = 4
    B = 5
    C = 6

    def __repr__(self) -> str:
        return f"{self.name}"

    def __str__(self) -> str:
        return self.__repr__()


class Registry:
    value: int

    def __init__(self, line: str) -> None:
        self.value = int(line)

    def __repr__(self) -> str:
        return f"Registry({self.value})"


class Opcode(Enum):
    ADV = 0  # division
    BXL = 1  # bitwise xor
    BST = 2  # modulo 8
    JNZ = 3  # jump
    BXC = 4  # bitwise xor
    OUT = 5  # modulo 8
    BDV = 6  # division
    CDV = 7  # division


def parse(file_name: str) -> tuple[RegistryDict, list[int]]:
    registries = RegistryDict()
    program = []

    with open(file_name) as file:
        for i, line in enumerate(file):
            if i < 3:
                registries[RegistryType(i + 4)] = Registry(line.split(":")[1].strip())

            if i == 4:
                program = list(map(int, line.split(":")[1].strip().split(",")))

    return registries, program


def combo(operand: int, registries: RegistryDict) -> int:
    if operand < 4:
        return operand

    return registries[RegistryType(operand)]


def evaluate(registries, program):
    out = []

    pointer = 0
    while pointer < len(program):
        opcode = Opcode(program[pointer])
        operand = program[pointer + 1]

        match opcode:
            case Opcode.ADV | Opcode.BDV | Opcode.CDV:
                target = None

                match opcode:
                    case Opcode.ADV:
                        target = RegistryType.A
                    case Opcode.BDV:
                        target = RegistryType.B
                    case Opcode.CDV:
                        target = RegistryType.C

                registries[target] = registries[RegistryType.A] >> combo(
                    operand, registries
                )  # same as // 2 ** operand

            case Opcode.BXL:
                registries[RegistryType.B] = registries[RegistryType.B] ^ operand

            case Opcode.BST:
                registries[RegistryType.B] = combo(operand, registries) % 8

            case Opcode.JNZ:
                if registries[RegistryType.A] != 0:
                    pointer = operand
                    continue

            case Opcode.BXC:
                registries[RegistryType.B] = (
                    registries[RegistryType.B] ^ registries[RegistryType.C]
                )

            case Opcode.OUT:
                out.append(combo(operand, registries) % 8)

        pointer += 2

    return out


def part_1() -> str:
    registries, program = parse("input.txt")

    return ",".join(map(str, evaluate(registries, program)))


def part_2() -> int:
    registries, program = parse("input.txt")

    candidates = [0]
    for length in range(1, len(program) + 1):
        out = []

        for num in candidates:
            # try all 3-bit combinations
            for offset in range(2**3):
                a = (2**3) * num + offset
                registries[RegistryType.A] = a

                if evaluate(registries, program) == program[-length:]:
                    out.append(a)

        candidates = out

    return min(candidates)
