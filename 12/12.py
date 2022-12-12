from dataclasses import dataclass, field
from typing import Dict, Optional, Set
from utils.inputs import get_input_lines

@dataclass(frozen=True)
class Point:
    x: int = 0
    y: int = 0


@dataclass
class Node:
    height: int
    pos: Point
    connections: Dict[Point, int] = field(default_factory=dict)

    def __lt__(self, other: 'Node') -> bool:
        return self.height < other.height


HeightsMap = Dict[Point, Node]

def filter_connections(hmap: HeightsMap, f_point: Point) -> Dict[Point, int]:
    upper = Point(f_point.x - 1, f_point.y)
    lower = Point(f_point.x + 1, f_point.y)
    left = Point(f_point.x, f_point.y - 1)
    right = Point(f_point.x, f_point.y + 1)
    res = {}

    if upper in hmap and hmap[f_point].height - hmap[upper].height <= 1:
        # res[upper] = abs(hmap[upper].height - hmap[f_point].height)
        res[upper] = 1

    if lower in hmap and hmap[f_point].height - hmap[lower].height <= 1:
        # res[lower] = abs(hmap[lower].height - hmap[f_point].height)
        res[lower] = 1

    if left in hmap and hmap[f_point].height - hmap[left].height <= 1:
        # res[left] = abs(hmap[left].height - hmap[f_point].height)
        res[left] = 1

    if right in hmap and hmap[f_point].height - hmap[right].height <= 1:
        # res[right] = abs(hmap[right].height - hmap[f_point].height)
        res[right] = 1

    return res


def main():
    input_lines = get_input_lines('./input.txt')
    start_node: Optional[Node] = None
    end_node: Optional[Node] = None

    buildings: HeightsMap = {}
    for r_idx, row in enumerate(input_lines):
        for c_idx, height in enumerate(row):
            point = Point(r_idx, c_idx)
            node = Node(ord(height), point)
            if height == 'S':
                node = Node(ord('a'), point)
                start_node = node
            elif height == 'E':
                node = Node(ord('z'), point)
                end_node = node

            buildings[Point(r_idx, c_idx)] = node

    if not start_node or not end_node:
        raise Exception('Start or end not found')

    for node in buildings.values():
        node.connections = filter_connections(buildings, node.pos)

    # print(buildings[Point(end_node.pos.x, end_node.pos.y)])

    dists: Dict[Point, float] = {}
    # prev: Dict[Point, Optional[Node]] = {}
    visited: Set[Point] = set()
    q = []

    for node in buildings.values():
        dists[node.pos] = float('inf')

    dists[end_node.pos] = 0

    q.append(end_node)
    while len(q) > 0:
        node: Node = sorted(q, key=lambda n: dists[n.pos])[0]
        q.remove(node)

        if node.pos in visited:
            continue

        visited.add(node.pos)

        for conn, dist in node.connections.items():
            total_distance = dists[node.pos] + dist
            if total_distance < dists[conn]:
                dists[conn] = total_distance

            if conn not in visited:
                q.append(buildings[conn])

    print(f'Answer 1: {dists[start_node.pos]}')

    min_a_dist = float('inf')
    for node in buildings.values():
        if node.height == ord('a') and dists[node.pos] < min_a_dist:
            min_a_dist = dists[node.pos]

    print(f'Answer 2: {min_a_dist}')


if __name__ == '__main__':
    main()
