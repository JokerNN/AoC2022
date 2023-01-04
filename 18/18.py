from dataclasses import dataclass
from collections import deque
from typing import Deque, Set, Tuple
from utils.inputs import get_input_lines

@dataclass(frozen=True)
class Point3:
    x: int
    y: int
    z: int

    def __add__(self: 'Point3', other: 'Point3'):
        return Point3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

Space3D = Set[Point3]

neighbours3 = [
    Point3( 0,  0,  1),
    Point3( 0,  1,  0),
    Point3( 1,  0,  0),
    Point3( 0,  0, -1),
    Point3( 0, -1,  0),
    Point3(-1,  0,  0)
]

def bfs(p: Point3, boulders: Space3D, max_x, max_y, max_z) -> Tuple[bool, Space3D]:
    q: Deque[Point3] = deque([p])
    reached_edge: bool = False
    empty_space: Space3D = {p}
    while q:
        cur_point = q.popleft()
        for neighbour in neighbours3:
            candidate = cur_point + neighbour
            if candidate in boulders or candidate in empty_space:
                continue

            if candidate.x < 0 or candidate.y < 0 or candidate.z < 0:
                reached_edge = True
                continue

            if candidate.x > max_x or candidate.y > max_y or candidate.z > max_z:
                reached_edge = True
                continue

            empty_space.add(candidate)
            q.append(candidate)

    return reached_edge, empty_space


def main():
    lines = get_input_lines('./input.txt')
    boulder_space: Set[Point3] = set()

    max_x = 0
    max_y = 0
    max_z = 0

    for boulder_line in lines:
        boulder = Point3(*(int(d) for d in boulder_line.split(',')))
        boulder_space.add(boulder)

        max_x = max(max_x, boulder.x)
        max_y = max(max_y, boulder.y)
        max_z = max(max_z, boulder.z)

    count = 0
    for boulder in boulder_space:
        for neighbour in neighbours3:
            n_boulder = boulder + neighbour
            if n_boulder not in boulder_space:
                count += 1


    print(f'Answer 1: {count}')

    outer_space: Space3D = set()
    inner_space: Space3D = set()
    for x in range(max_x):
        for y in range(max_y):
            for z in range(max_z):
                test_point = Point3(x, y, z)
                if test_point in boulder_space or test_point in outer_space or test_point in inner_space:
                    continue

                reached_edge, result_space = bfs(test_point, boulder_space, max_x, max_y, max_z)

                if reached_edge:
                    outer_space |= result_space
                else:
                    inner_space |= result_space

    if len(inner_space) == 0:
        raise Exception("Didn't find air pocket")

    count = 0
    for boulder in boulder_space:
        for neighbour in neighbours3:
            n_boulder = boulder + neighbour
            if n_boulder not in boulder_space and n_boulder not in inner_space:
                count += 1

    print(f'Answer 2: {count}')

if __name__ == '__main__':
    main()
