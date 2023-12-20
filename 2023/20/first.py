from enum import Enum
from collections import deque

file = open("./input.txt").readlines()


class ModuleType(Enum):
    FLIP_FLOP = "%"
    CONJUCTION = "&"
    BROADCASTER = "broadcaster"


class PulseType(Enum):
    LOW = 0
    HIGH = 1


class Module:
    def __init__(self, line: str):
        name, destinations = line.split("->")
        name = name.strip()

        if name == "broadcaster":
            self.type = ModuleType.BROADCASTER
            self.name = name
        else:
            self.type = ModuleType(name[0])
            self.name = name[1:]

        self.destinations = [x.strip() for x in destinations.split(",")]
        self.memory = False if self.type == ModuleType.FLIP_FLOP else {}

    def __repr__(self) -> str:
        return (
            self.name
            + "{type="
            + self.type.name
            + " ("
            + self.type.value
            + "), destinations="
            + str(self.destinations)
            + ", memory="
            + str(self.memory)
            + "}"
        )


modules = {}
broadcast_targets = []

for line in file:
    module = Module(line)

    modules[module.name] = module

for name, module in modules.items():
    for destination in module.destinations:
        if (
            destination in modules
            and modules[destination].type == ModuleType.CONJUCTION
        ):
            modules[destination].memory[name] = PulseType.LOW

low_pulses = 0
high_pulses = 0

for _ in range(1000):
    low_pulses += 1

    queue = deque(
        [("broadcaster", x, PulseType.LOW) for x in modules["broadcaster"].destinations]
    )

    while queue:
        source, destination, pulse = queue.popleft()

        if pulse == PulseType.LOW:
            low_pulses += 1
        else:
            high_pulses += 1

        if destination not in modules:
            continue

        module = modules[destination]

        if module.type == ModuleType.FLIP_FLOP:
            if pulse == PulseType.LOW:
                module.memory = module.memory == False
                outgoing_pulse = PulseType.HIGH if module.memory else PulseType.LOW
                for dest in module.destinations:
                    queue.append((module.name, dest, outgoing_pulse))

        else:
            module.memory[source] = pulse
            outgoing_pulse = (
                PulseType.LOW
                if all(pulse == PulseType.HIGH for pulse in module.memory.values())
                else PulseType.HIGH
            )
            for dest in module.destinations:
                queue.append((module.name, dest, outgoing_pulse))

print(low_pulses * high_pulses)
