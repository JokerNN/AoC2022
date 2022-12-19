from collections import defaultdict
from typing import DefaultDict, List
from utils.inputs import get_input_lines
from utils.geometry import Point

CaveMap = DefaultDict[Point, str]

def generate_points(start: Point, end: Point) -> List[Point]:
    res = []
    if start.x == end.x:
        sy, ey = sorted((start.y, end.y))
        for y in range(sy, ey + 1):
            res.append(Point(start.x, y))
    elif start.y == end.y:
        sx, ex = sorted((start.x, end.x))
        for x in range(sx, ex + 1):
            res.append(Point(x, start.y))
    else:
        raise Exception('nonpossible')

    return res

def draw_line(cave_map: CaveMap, points: List[Point]) -> None:
    for idx in range(len(points) - 1):
        start = points[idx]
        end = points[idx + 1]
        inbetween_points = generate_points(start, end)
        for p in inbetween_points:
            cave_map[p] = '#'

def simulate_single_sand(cave_map: CaveMap, bottom: int) -> bool:
    sand_position = Point(500, 0)
    while True:
        if sand_position.y >= bottom:
            return True

        next_pos = Point(sand_position.x, sand_position.y + 1)
        if cave_map[next_pos] == '.':
            sand_position = next_pos
            continue

        next_pos = Point(sand_position.x - 1, sand_position.y + 1)
        if cave_map[next_pos] == '.':
            sand_position = next_pos
            continue

        next_pos = Point(sand_position.x + 1, sand_position.y + 1)
        if cave_map[next_pos] == '.':
            sand_position = next_pos
            continue

        cave_map[sand_position] = '#'
        return False


def simulate_single_sand_2(cave_map: CaveMap, bottom: int) -> Point:
    sand_position = Point(500, 0)

    while True:
        if sand_position.y + 1 == bottom:
            cave_map[sand_position] = '#'
            return sand_position

        next_pos = Point(sand_position.x, sand_position.y + 1)
        if cave_map[next_pos] == '.':
            sand_position = next_pos
            continue

        next_pos = Point(sand_position.x - 1, sand_position.y + 1)
        if cave_map[next_pos] == '.':
            sand_position = next_pos
            continue

        next_pos = Point(sand_position.x + 1, sand_position.y + 1)
        if cave_map[next_pos] == '.':
            sand_position = next_pos
            continue

        cave_map[sand_position] = '#'
        return sand_position



def main_1():
    cave_map: CaveMap = defaultdict(lambda: '.')
    inp_lines = get_input_lines('./input.txt')
    max_y = -1
    for line in inp_lines:
        _points = line.split(' -> ')
        points = []
        for _p in _points:
            _p = _p.split(',')
            p = Point(int(_p[0]), int(_p[1]))
            points.append(p)
            max_y = max(p.y, max_y)

        draw_line(cave_map, points)

    # print(max_y)
    c = 0
    while simulate_single_sand(cave_map, max_y + 2) is False:
        c += 1

    print(f'Answer 1: {c}')

def main_2():
    cave_map: CaveMap = defaultdict(lambda: '.')
    inp_lines = get_input_lines('./input.txt')
    max_y = -1
    for line in inp_lines:
        _points = line.split(' -> ')
        points = []
        for _p in _points:
            _p = _p.split(',')
            p = Point(int(_p[0]), int(_p[1]))
            points.append(p)
            max_y = max(p.y, max_y)

        draw_line(cave_map, points)

    # print(max_y)
    c = 0
    while True:
        landed_at = simulate_single_sand_2(cave_map, max_y + 2)
        c += 1
        # print(landed_at)
        if landed_at == Point(500, 0):
            break

    print(f'Answer 2: {c}')

if __name__ == '__main__':
    main_1()
    main_2()
