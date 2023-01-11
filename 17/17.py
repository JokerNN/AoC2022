from collections import defaultdict
from dataclasses import dataclass
import math
from typing import Set
from utils.inputs import get_input_lines
from utils.geometry import Point

shapes = [
    {Point(0, -1), Point(1, -1), Point(2, -1), Point(3, -1)},               # -
    {Point(1, -1), Point(0, -2), Point(1, -2),
     Point(2, -2), Point(1, -3)},  # +
    {Point(0, -1), Point(1, -1), Point(2, -1),
     Point(2, -2), Point(2, -3)},  # mirrored L,
    {Point(0, -1), Point(0, -2), Point(0, -3), Point(0, -4)},               # |
    {Point(0, -1), Point(1, -1), Point(0, -2),
     Point(1, -2)}                # square 2x2
]


dirs = {
    '>': Point(1, 0),
    '<': Point(-1, 0),
    'v': Point(0, 1)
}


@dataclass
class State:
    chamber: Set[Point]
    wind_idx: int = 0
    shape_idx: int = 0
    top_idx: int = 0




state = State(chamber={Point(-2, 0), Point(-1, 0), Point(0, 0),
              Point(1, 0), Point(2, 0), Point(3, 0), Point(4, 0)})


def visualize_chamber(chamber, shape, min_y):
    lines = []
    y = 0

    while y >= min_y:
        line = []
        found = False
        shape_touched = False
        for x in range(-2, 5):
            if Point(x, y) in chamber:
                line += '#'
            elif Point(x, y) in shape:
                line += '@'
            else:
                line += '.'

        lines.append(''.join(line))
        y -= 1

    return '\n'.join(lines[::-1]) + '\n'



def fall_shape(winds):
    shape_set = shapes[state.shape_idx % len(shapes)]
    state.shape_idx += 1
    cur_shape_pos = {p + Point(0, state.top_idx - 3) for p in shape_set}
    while True:
        # jet push
        wind_dir = winds[state.wind_idx % len(winds)]
        state.wind_idx += 1
        wind = dirs[wind_dir]
        new_shape_pos = {p + wind for p in cur_shape_pos}

        if min(p.x for p in new_shape_pos) >= -2 and max(p.x for p in new_shape_pos) <= 4 and len(new_shape_pos & state.chamber) == 0:
            cur_shape_pos = new_shape_pos

        # print(visualize_chamber(state.chamber, cur_shape_pos, state.top_idx - 6))

        # down movement
        new_shape_pos = {p + dirs['v'] for p in cur_shape_pos}
        if len(new_shape_pos & state.chamber) != 0:
            state.chamber |= cur_shape_pos
            state.top_idx = min(min(p.y for p in cur_shape_pos), state.top_idx)
            break
        else:
            cur_shape_pos = new_shape_pos
            # print(visualize_chamber(state.chamber, cur_shape_pos, state.top_idx - 6))

def trim():
    new_chamber = set()
    for y in range(state.top_idx, state.top_idx + 40):
        for x in range(-2, 5):
            new_p = Point(x, y)
            if new_p in state.chamber:
                new_chamber.add(new_p)

    state.chamber = new_chamber


def top_hull(chamber):
    res = []
    for x in range(-1, 5):
        res.append(min(p.y for p in chamber if p.x == x))

    res = [i - res[0] for i in res]
    return tuple(res)


def main1():
    winds = get_input_lines('./input_tst.txt')[0]
    for _ in range(2022):
        fall_shape(winds)

    print(f'Answer 1: {-state.top_idx}')

def main2():
    winds = get_input_lines('./input.txt')[0]
    seen = defaultdict(list)

    # for step in range(10000):
    #     if step % 10000 == 0:
    #         print(step / 10000000000)
    #         trim()

    #     fall_shape(winds)
    #     hull = top_hull(state.chamber)
    #     state_key = (hull, state.shape_idx % len(shapes), state.wind_idx % len(winds))

    #     if state_key in seen:
    #         print(state_key)
    #         print(seen[state_key], step)
    #         print(f'Period: {step - seen[state_key][0]}')
    #         break

    #     seen[state_key].append(step)

    # print(state.top_idx)
    init_steps = 244
    period = 1745
    for _ in range(init_steps):
        fall_shape(winds)

    init_height = -state.top_idx
    periodic_height = 3095 - 382
    rest_steps = (1_000_000_000_000 - init_steps) % period
    total_height = ((1_000_000_000_000 - init_steps) // period) * periodic_height
    for _ in range(rest_steps):
        fall_shape(winds)
    
    print(total_height - state.top_idx)



if __name__ == '__main__':
    main1()
    state = State(chamber={Point(-2, 0), Point(-1, 0), Point(0, 0),
              Point(1, 0), Point(2, 0), Point(3, 0), Point(4, 0)})
    main2()
