from math import lcm
from collections import deque, defaultdict
from typing import DefaultDict, Dict, Set, Deque, Tuple
from utils.inputs import get_input_lines
from utils.geometry import Point


ValleyMap = Dict[Point, str]

vec_map = {
    '^': Point(0, -1),
    '>': Point(1, 0),
    'v': Point(0, 1),
    '<': Point(-1, 0)
}


def main1():
    valley_map: ValleyMap = {}
    lines = get_input_lines('./input.txt')
    blizzards: DefaultDict[str, Set[Point]] = defaultdict(set)
    max_row = len(lines) - 2
    max_col = len(lines[-1]) - 2
    for row_idx, row in enumerate(lines[1:]):
        for col_idx, space in enumerate(row[1:]):
            if space in vec_map:
                blizzards[space].add(Point(col_idx, row_idx))
            valley_map[Point(col_idx, row_idx)] = space

    period = lcm(max_row, max_col)
    start_point = Point(0, -1)
    target_point = Point(max_col - 1, max_row)

    q: Deque[Tuple[int, Point]] = deque([(0, start_point)])
    visited: Set = set()
    answer_found = False
    while q:
        if answer_found:
            break
        minute, pos = q.popleft()

        minute += 1

        for direction in [*vec_map.values(), Point(0, 0)]:
            next_pos = pos + direction

            if next_pos == target_point:
                print(f'Answer 1: {minute}')
                answer_found = True

            if (next_pos not in valley_map or valley_map[next_pos] == '#') and next_pos != start_point:
                continue

            for dir_char, vec in vec_map.items():
                potential_next = Point(
                    (next_pos.x - vec.x * minute) % max_col, (next_pos.y - vec.y * minute) % max_row)
                if potential_next in blizzards[dir_char]:
                    break
            else:
                state_key = (minute % period, next_pos)
                if state_key in visited:
                    continue

                visited.add(state_key)
                q.append((minute, next_pos))


def main2():
    valley_map: ValleyMap = {}
    lines = get_input_lines('./input.txt')
    blizzards: DefaultDict[str, Set[Point]] = defaultdict(set)
    max_row = len(lines) - 2
    max_col = len(lines[-1]) - 2
    for row_idx, row in enumerate(lines[1:]):
        for col_idx, space in enumerate(row[1:]):
            if space in vec_map:
                blizzards[space].add(Point(col_idx, row_idx))
            valley_map[Point(col_idx, row_idx)] = space

    period = lcm(max_row, max_col)
    start_point = Point(0, -1)
    target_point = Point(max_col - 1, max_row)

    q: Deque[Tuple[int, Point, int]] = deque([(0, start_point, 0)])
    visited: Set = set()
    answer_found = False

    goals = [target_point, start_point, target_point]

    while q:
        if answer_found is True:
            break

        minute, pos, step = q.popleft()

        minute += 1

        for direction in [*vec_map.values(), Point(0, 0)]:
            next_pos = pos + direction

            if next_pos == goals[step]:
                if step == 2:
                    print(f'Answer 2: {minute}')
                    answer_found = True
                else:
                    step += 1

            if (next_pos not in valley_map or valley_map[next_pos] == '#') and next_pos not in {start_point, target_point}:
                continue

            hazard = False
            if next_pos not in {start_point, target_point}:
                # check for hazards
                for dir_char, vec in vec_map.items():
                    potential_next = Point(
                        (next_pos.x - vec.x * minute) % max_col, (next_pos.y - vec.y * minute) % max_row)
                    if potential_next in blizzards[dir_char] and potential_next != start_point and potential_next != target_point:
                        hazard = True
                        break

            if not hazard:
                state_key = (minute % period, next_pos, step)

                if state_key in visited:
                    continue

                visited.add(state_key)
                q.append((minute, next_pos, step))


if __name__ == '__main__':
    main1()
    main2()
