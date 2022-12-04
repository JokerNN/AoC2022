import os
import sys
from typing import Generator, List, Tuple


def generate_pairs(pairs_input: List[str]) -> Generator[Tuple[Tuple[int, int], Tuple[int, int]], None, None]:
    for pair in pairs_input:
        range1, range2 = pair.split(',')
        l1, r1 = (int(n) for n in range1.split('-'))
        l2, r2 = (int(n) for n in range2.split('-'))
        yield sorted(((l1, r1), (l2, r2)))


with open(os.path.join(sys.path[0], "input.txt")) as file:
    pairs: List[str] = file.read().split('\n')
    overlap_count = 0
    for pair in generate_pairs(pairs):
        (l1, r1), (l2, r2) = pair
        if l1 <= l2 and r1 >= r2 or l2 <= l1 and r2 >= r1:
            overlap_count += 1

    print(f'Answer 1: {overlap_count}')

    overlap_count = 0
    for pair in generate_pairs(pairs):
        (l1, r1), (l2, r2) = pair
        if l1 == l2 or r1 == r2:
            overlap_count += 1
        elif l2 <= r1:
            overlap_count += 1

    print(f'Answer 2: {overlap_count}')
