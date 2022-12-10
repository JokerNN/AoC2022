from typing import DefaultDict
from collections import defaultdict
from utils.inputs import get_input_lines


def main():
    instructions = get_input_lines('input.txt')
#     instructions = '''noop
# addx 3
# addx -5'''.split('\n')
    x = 1
    cycles: DefaultDict[int, int] = defaultdict(lambda: 1)
    cycle_cnt = 1
    for instruction in instructions:
        if instruction == 'noop':
            cycle_cnt += 1
            cycles[cycle_cnt] = x
            continue

        _, value = instruction.split()
        value = int(value)
        cycles[cycle_cnt + 1] = x
        cycle_cnt += 2
        x += value
        cycles[cycle_cnt] = x

    answer_steps = [20, 60, 100, 140, 180, 220]
    answer = sum(idx * cycles[idx] for idx in answer_steps)
    print(f'Answer 1: {answer}')

    crt = []
    for cycle in range(1, 241):
        drawing_pixel = cycle % 40 - 1
        if abs(cycles[cycle] - drawing_pixel) <= 1:
            crt.append('#')
        else:
            crt.append('.')

    print('Answer 2:')
    for idx in range(0, 241, 40):
        print(''.join(crt[idx: idx + 39]))


if __name__ == '__main__':
    main()
