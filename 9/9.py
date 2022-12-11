from typing import Literal, Set
from dataclasses import dataclass
from utils.inputs import get_input_lines

Direction = Literal['U', 'R', 'D', 'L']


@dataclass(frozen=True)
class Point:
    x: int = 0
    y: int = 0

    def __lt__(self: 'Point', other: 'Point'):
        return self.y < other.y or self.x < other.x


def move_one_step(direction: Direction, start_point: Point) -> Point:
    if direction == 'U':
        return Point(start_point.x, start_point.y - 1)
    if direction == 'R':
        return Point(start_point.x + 1, start_point.y)
    if direction == 'D':
        return Point(start_point.x, start_point.y + 1)
    if direction == 'L':
        return Point(start_point.x - 1, start_point.y)

    raise Exception(f'Unknown direction: {direction}')


def move_tail(head: Point, tail: Point) -> Point:
    if abs(head.x - tail.x) <= 1 and abs(head.y - tail.y) <= 1:
        return tail

    if head.x > tail.x and head.y > tail.y:
        return Point(tail.x + 1, tail.y + 1)

    if head.x > tail.x and head.y < tail.y:
        return Point(tail.x + 1, tail.y - 1)

    if head.x > tail.x and head.y == tail.y:
        return Point(tail.x + 1, tail.y)

    if head.x == tail.x and head.y > tail.y:
        return Point(tail.x, tail.y + 1)

    if head.x == tail.x and head.y < tail.y:
        return Point(tail.x, tail.y - 1)

    if head.x < tail.x and head.y > tail.y:
        return Point(tail.x - 1, tail.y + 1)

    if head.x < tail.x and head.y < tail.y:
        return Point(tail.x - 1, tail.y - 1)

    if head.x < tail.x and head.y == tail.y:
        return Point(tail.x - 1, tail.y)

    raise Exception('What?')


def main():
    instructions = get_input_lines('input.txt')
    head_pos = Point(0, 0)
    tail_pos = Point(0, 0)

    tail_trail: Set[Point] = {tail_pos}

    for instruction in instructions:
        direction: Direction
        direction, _count = instruction.split()
        count: int = int(_count)
        for _ in range(count):
            head_pos = move_one_step(direction, head_pos)
            tail_pos = move_tail(head_pos, tail_pos)
            tail_trail.add(tail_pos)

    print(f'Answer 1: {len(tail_trail)}')

    rope_knots = [Point(0, 0) for _ in range(10)]
    tail_trail = {rope_knots[9]}

    for instruction in instructions:
        direction: Direction
        direction, _count = instruction.split()
        count: int = int(_count)

        for _ in range(count):
            rope_knots[0] = move_one_step(direction, rope_knots[0])

            for idx in range(1, len(rope_knots)):
                rope_knots[idx] = move_tail(
                    rope_knots[idx - 1], rope_knots[idx])

            tail_trail.add(rope_knots[9])

    print(f'Answer 2: {len(tail_trail)}')


if __name__ == '__main__':
    main()
