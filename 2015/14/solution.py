"""
Day 14: Reindeer Olympics

This problem simulates a reindeer racing competition where each reindeer follows
a fixed pattern of movement and rest periods. Each reindeer has unique characteristics
that define its racing strategy - flying at a constant speed for a set duration before
requiring a mandatory rest period, creating a cyclical pattern of motion and recovery.

Key approach:
1. Efficient distance calculation using cycle mathematics:
   - Break movement into complete cycles and partial cycle
   - Calculate complete cycles using floor division
   - Handle remaining time as partial cycle

2. Two distinct scoring mechanisms:
   - Part 1: Pure distance race
     * Calculate final position for each reindeer
     * Find maximum distance covered
   - Part 2: Leading position points
     * Simulate race second by second
     * Award points to leader(s) at each timestamp
     * Track cumulative scores

Distance calculation formula:
distance(t) = nc * v * e + min(t - nc*(e+r), e) * v

where:
   - t = time duration
   - nc = floor(t / (e+r)) = number of complete cycles
   - v = velocity
   - e = endurance
   - r = rest time
   - (e+r) = total cycle length

The formula breaks down the movement into:

1. Complete cycles: nc * v * e
   - Each cycle has a flying phase (e seconds) and rest phase (r seconds)
   - During flying phase, reindeer covers v*e distance
   - nc cycles means this distance is repeated nc times

2. Partial cycle: min(t - nc*(e+r), e) * v
   - After complete cycles, we have t - nc*(e+r) seconds left
   - If this remainder is greater than endurance (e),
     reindeer can only fly for e seconds
   - If remainder is less than e, reindeer flies for all remaining time

Time complexity:
- Part 1: O(n) where n = number of reindeer
- Part 2: O(t*n) where t = time duration, n = number of reindeer

Space complexity: O(n) for storing reindeer list and scores array
"""

from dataclasses import dataclass
from math import floor


@dataclass
class Reindeer:
    velocity: int
    endurance: int
    rest: int

    def distance(self, duration: int) -> int:
        total = self.endurance + self.rest
        nc = floor(duration / total)

        return (
            nc * self.velocity * self.endurance
            + min(duration - nc * (total), self.endurance) * self.velocity
        )


def reindeers() -> list[Reindeer]:
    reindeers = []

    for line in open("input.txt").read().splitlines():
        _, _, _, velocity, _, _, endurance, _, _, _, _, _, _, rest, _ = line.split()
        velocity = int(velocity)
        endurance = int(endurance)
        rest = int(rest)

        reindeers.append(Reindeer(velocity, endurance, rest))

    return reindeers


def part_1() -> int:
    result = 0

    for reindeer in reindeers():
        result = max(result, reindeer.distance(2503))

    return result


def part_2() -> int:
    r = reindeers()

    scores = [0] * len(r)

    for second in range(1, 2504):
        positions = [reindeer.distance(second) for reindeer in r]

        max_dist = max(positions)
        for i, pos in enumerate(positions):
            if pos == max_dist:
                scores[i] += 1

    return max(scores)
