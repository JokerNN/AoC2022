from typing import DefaultDict, Dict, List, Tuple
from collections import defaultdict
from utils.inputs import get_input_lines
from utils.geometry import Point

ElvesMap = DefaultDict[Point, str]

def get_orthos(vec: Point) -> List[Point]:
    if vec.x == 0:
        return [Point(-1, vec.y), Point(1, vec.y)]
    
    if vec.y == 0:
        return [Point(vec.x, -1), Point(vec.x, 1)]

    raise Exception('Unknown vector for orthos')


ALL_ADJ = [
    Point( 0, -1),
    Point( 1, -1),
    Point( 1,  0),
    Point( 1,  1),
    Point( 0,  1),
    Point(-1,  1),
    Point(-1,  0),
    Point(-1, -1)
]

def find_boundaries(elves_map: ElvesMap) -> Tuple[Point, Point]:
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = -float('inf'), -float('inf')
    for pos, space in elves_map.items():
        if space == '#':
            min_x = min(pos.x, min_x)
            min_y = min(pos.y, min_y)
            max_x = max(pos.x, max_x)
            max_y = max(pos.y, max_y)

    return (Point(int(min_x), int(min_y)), Point(int(max_x), int(max_y)))


def game_round(elves_map: ElvesMap, moves_priority: List[Point]) -> bool:
    elf_moved = False
    move_proposals: DefaultDict[Point, List[Point]] = defaultdict(list)
    for pos, space in list(elves_map.items()):
        if space == '#':
            if all(elves_map[pos + n] == '.' for n in ALL_ADJ):
                continue
            for move in moves_priority:
                neighbors = [*get_orthos(move), move]
                if all(elves_map[pos + n] == '.' for n in neighbors):
                    move_proposals[pos+move].append(pos)
                    break

    for target, elfs in move_proposals.items():
        if len(elfs) == 1:
            elf_moved = True
            elves_map[target] = '#'
            elves_map[elfs[0]] = '.'

    return elf_moved
    # for y in range(-10, 10):
    #     l = ''
    #     for x in range(-10, 10):
    #         l += elves_map[Point(x, y)]
    #     print(l)
    # print(' ')


def main():
    elves_map: ElvesMap = defaultdict(lambda: '.')
    lines = get_input_lines('./input.txt')
    elf_count = 0
    for r_idx, row in enumerate(lines):
        for c_idx, cell in enumerate(row):
            elves_map[Point(c_idx, r_idx)] = cell
            if cell == '#':
                elf_count += 1

    moves_queue: List[Point] = [
        Point(0, -1),
        Point(0, 1),
        Point(-1, 0),
        Point(1, 0),
    ]
    for _ in range(10):
        game_round(elves_map, moves_queue)
        moves_queue.append(moves_queue[0])
        del moves_queue[0]

    tl, br = find_boundaries(elves_map)
    answer1 = (br.x - tl.x + 1) * (br.y - tl.y + 1) - elf_count
    print(f'Answer 1: {answer1}')

    for round_count in range(10, 999_999_999):
        res = game_round(elves_map, moves_queue)
        if res is False:
            print(f'Answer 2: {round_count + 1}')
            break
        moves_queue.append(moves_queue[0])
        del moves_queue[0]



if __name__ == '__main__':
    main()
