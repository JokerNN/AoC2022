import os
import sys
from typing import List

with open(os.path.join(sys.path[0], "input.txt")) as file:
    score: int = 0
    rucksack: str
    rucksacks: List[str] = file.readlines()
    for rucksack in rucksacks:
        midpoint = len(rucksack) // 2
        l, r = rucksack[:midpoint], rucksack[midpoint:]

        union = set(l) & set(r)
        print(union)
        item_id: str = union.pop()
        if item_id == item_id.lower():
            score += ord(item_id) - 96
        else:
            score += ord(item_id) - 38
        # print(f'{item_id}: {score}')

    print(f'Answer 1: {score}')

    score = 0
    for idx in range(0, len(rucksacks), 3):
        group = rucksacks[idx: idx + 3]
        res = set(group[0].strip()) & set(
            group[1].strip()) & set(group[2].strip())

        item_id: str = res.pop()
        if item_id == item_id.lower():
            score += ord(item_id) - 96
        else:
            score += ord(item_id) - 38

    print(f'Answer 2: {score}')
