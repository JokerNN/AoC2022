import re
from typing import Dict, List, Literal, Tuple
from utils.inputs import get_raw
from utils.geometry import Point


class BoardMap(dict):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

# BoardMap = Dict[Point, str]
Direction = Literal['U', 'R', 'D', 'L']

ins_pattern = re.compile(r'(\d+|[LR])')

dir_vec: Dict[Direction, Point] = {
    'U': Point(0, -1),
    'R': Point(1, 0),
    'D': Point(0, 1),
    'L': Point(-1, 0)
}

def step(board_map: BoardMap, pos: Point, direction: Direction) -> Point:
    vector = dir_vec[direction]
    next_pos = pos + vector
    if next_pos in board_map:
        if board_map[next_pos] != '#':
            return next_pos
        return pos
    else:
        if direction == 'U':
            possible_next = Point(pos.x, board_map.height)
            while possible_next not in board_map:
                possible_next = Point(pos.x, possible_next.y - 1)

            if board_map[possible_next] != '#':
                return possible_next
            else:
                return pos

        elif direction == 'R':
            possible_next = Point(0, pos.y)
            while possible_next not in board_map:
                possible_next = Point(possible_next.x + 1, pos.y)

            if board_map[possible_next] != '#':
                return possible_next
            else:
                return pos

        elif direction == 'D':
            possible_next = Point(pos.x, 0)
            while possible_next not in board_map:
                possible_next = Point(pos.x, possible_next.y + 1)

            if board_map[possible_next] != '#':
                return possible_next
            else:
                return pos
        elif direction == 'L':
            possible_next = Point(board_map.width, pos.y)
            while possible_next not in board_map:
                possible_next = Point(possible_next.x - 1, pos.y)

            if board_map[possible_next] != '#':
                return possible_next
            else:
                return pos

        else:
            raise Exception('Unknown direction')


warps_t = {
    'U': [{
        'condition': lambda p: p.y == 0,
        'transformation': lambda p: Point(4 - abs(8 - p.x), 3),
        'direction': 'D'
    }, {
        'condition': lambda p: p.y == 4 and p.x <= 3,
        'transformation': lambda p: Point(8 + abs(p.x - 4), 0),
        'direction': 'D'
    }, {
        'condition': lambda p: p.y == 4 and p.x >= 4,
        'transformation': lambda p: Point(8, 8 - p.x),
        'direction': 'R'
    }],
    'R': [{
        'condition': lambda p: p.y <= 3,
        'transformation': lambda p: Point(15, 15 - abs(4 - p.x)),
        'direction': 'L'
    }, {
        'condition': lambda p: p.y >= 4 and p.y <= 7,
        'transformation': lambda p: Point(12 + abs(p.y - 7), 8),
        'direction': 'D'
    }, {
        'condition': lambda p: p.y >=8,
        'transformation': lambda p: Point(11, 3 - abs(p.y - 8)),
        'direction': 'L'
    }],
    'D': [{
        'condition': lambda p: p.x >= 8 and p <= 11
    }]
}

warps = {
    'U': [{
        'condition': lambda p: p.y == 0 and p.x >=50 and p.x <= 99,
        'transformation': lambda p: Point(0, p.x + 100),
        'direction': 'R'
    }, {
        'condition': lambda p: p.y == 0 and p.x >=100 and p.x <= 149,
        'transformation': lambda p: Point(p.x - 100, 199),
        'direction': 'U'
    }, {
        'condition': lambda p: p.y == 100 and p.x >= 0 and p.x <= p.x <=49,
        'transformation': lambda p: Point(50, p.x + 50),
        'direction': 'R'
    }],
    'R': [{
        'condition': lambda p: p.x == 49 and p.y >=150 and p.y <= 199,
        'transformation': lambda p: Point(p.y - 100, 149),
        'direction': 'U'
    }, {
        'condition': lambda p: p.x == 99 and p.y >= 100 and p.y <= 149,
        'transformation': lambda p: Point(149, abs(150 - p.y)),
        'direction': 'L'
    }, {
        'condition': lambda p: p.x == 149 and p.y >= 0 and p.y <= 49,
        'transformation': lambda p: Point(99, 149 - p.y),
        'direction': 'L'
    }, {
        'condition': lambda p: p.x == 99 and p.y >= 50 and p.y <= 99,
        'transformation': lambda p: Point(p.y + 50, 49),
        'direction': 'U'
    }],
    'D': [{
        'condition': lambda p: p.y == 199 and p.x <= 49,
        'transformation': lambda p: Point(p.x + 100, 0),
        'direction': 'D'
    }, {
        'condition': lambda p: p.y == 49 and p.x >= 100 and p.y <= 49,
        'transformation': lambda p: Point(99, p.x - 50),
        'direction': 'L'
    }, {
        'condition': lambda p: p.y == 149 and p.x >= 50 and p.x <= 99,
        'transformation': lambda p: Point(49, p.x + 100),
        'direction': 'L'
    }],
    'L': [{
        'condition': lambda p: p.x == 0 and p.y >= 150 and p.y <= 199,
        'transformation': lambda p: Point(p.y - 100, 0),
        'direction': 'D',
    },{
        'condition': lambda p: p.x == 0 and p.y >= 100 and p.y <= 149,
        'transformation': lambda p: Point(50, abs(150 - p.y)),
        'direction': 'R',
    },{
        'condition': lambda p : p.x == 50 and p.y >=0 and p.y <=49,
        'transformation': lambda p: Point(149 - p.y, 0),
        'direction': 'R'
    }, {
        'condition': lambda p: p.x == 50 and p.y >=50 and p.y <= 99,
        'transformation': lambda p: Point(p.y - 50, 100),
        'direction': 'D'
    }]
}

def step2(board_map: BoardMap, pos: Point, direction: Direction) -> Tuple[Point, Direction]:
    vector = dir_vec[direction]
    next_pos = pos + vector
    if next_pos in board_map:
        if board_map[next_pos] != '#':
            return next_pos, direction
        return pos, direction
    else:
        warps_dir = warps[direction]
        for warp in warps_dir:
            if warp['condition'] (pos):
                next_pos = warp['transformation'](pos)
                next_dir = warp['direction']
                print(f'Transitioning from: {direction}, {pos} to {next_dir}, {next_pos}')
                if board_map[next_pos] != '#':
                    return next_pos, next_dir
                else:
                    return pos, direction
        raise Exception(f'Unknown warp: {pos}, {direction}')


left_turn: Dict[Direction, Direction] = {
    'U': 'L',
    'R': 'U',
    'D': 'R',
    'L': 'D'
}

right_turn: Dict[Direction, Direction] = {
    'U': 'R',
    'R': 'D',
    'D': 'L',
    'L': 'U'
}

turn_score: Dict[Direction, int] = {
    'U': 3,
    'R': 0,
    'D': 1,
    'L': 2
}

def rotate(cur_dir: Direction, dir_to: Direction) -> Direction:
    if dir_to == 'L':
        return left_turn[cur_dir]
    if dir_to == 'R':
        return right_turn[cur_dir]

    raise Exception('Unknown direction')


def main():
    _board_map = get_raw('./input.txt').split('\n')

    instructions = _board_map[-1]
    del _board_map[-1: -3: -1]
    max_x, max_y = 0, 0
    board_map: BoardMap = BoardMap(0, 0)
    for row_idx, row in enumerate(_board_map):
        for col_idx, space in enumerate(row):
            if space != ' ':
                board_map[Point(col_idx, row_idx)] = space
                max_x = max(col_idx, max_x)
                max_y = max(row_idx, max_y)

    board_map.width = max_x
    board_map.height = max_y

    first_space = _board_map[0].find('.')
    pos = Point(first_space, 0)
    cur_dir: Direction = 'R'

    for ins_match in ins_pattern.finditer(instructions):
        ins = ins_match.group(0)
        if ins == 'L':
            cur_dir = rotate(cur_dir, 'L')
        elif ins == 'R':
            cur_dir = rotate(cur_dir, 'R')
        else:
            ins = int(ins)
            for _ in range(ins):
                pos = step(board_map, pos, cur_dir)

    res = (pos.x + 1) * 4 + (pos.y + 1) * 1000 + turn_score[cur_dir]
    print(f'Answer 1: {res}')


def main2():
    _board_map = get_raw('./input.txt').split('\n')

    instructions = _board_map[-1]
    del _board_map[-1: -3: -1]
    max_x, max_y = 0, 0
    board_map: BoardMap = BoardMap(0, 0)
    for row_idx, row in enumerate(_board_map):
        for col_idx, space in enumerate(row):
            if space != ' ':
                board_map[Point(col_idx, row_idx)] = space
                max_x = max(col_idx, max_x)
                max_y = max(row_idx, max_y)

    board_map.width = max_x
    board_map.height = max_y

    first_space = _board_map[0].find('.')
    pos = Point(first_space, 0)
    cur_dir: Direction = 'R'

    for ins_match in ins_pattern.finditer(instructions):
        ins = ins_match.group(0)
        if ins == 'L':
            cur_dir = rotate(cur_dir, 'L')
        elif ins == 'R':
            cur_dir = rotate(cur_dir, 'R')
        else:
            ins = int(ins)
            for _ in range(ins):
                pos, cur_dir = step2(board_map, pos, cur_dir)

    res = (pos.x + 1) * 4 + (pos.y + 1) * 1000 + turn_score[cur_dir]
    print(f'Answer 2: {res}')


if __name__ == '__main__':
    main()
    main2()
