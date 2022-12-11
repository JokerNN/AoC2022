import os
import sys

mapping = {
    'A': 'X',
    'B': 'Y',
    'C': 'Z'
}

scores_map = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

with open(os.path.join(sys.path[0], "input.txt"), "r", encoding='utf-8') as file:
    rounds = file.read().split('\n')
    score = 0
    for game in rounds:
        their = mapping[game[0]]
        my = game[2]
        score += scores_map[my]
        if my == their:
            score += 3
        elif my == 'X' and their == 'Z' or my == 'Y' and their == 'X' or my == 'Z' and their == 'Y':  # pylint: disable=R0916
            score += 6

    print(f'Ans 1: {score}')

    score = 0
    for game in rounds:
        their = mapping[game[0]]
        outcome = game[2]

        if outcome == 'X':
            if their == 'X':
                score += 3
            elif their == 'Y':
                score += 1
            elif their == 'Z':
                score += 2
        elif outcome == 'Y':
            score += 3
            if their == 'X':
                score += 1
            elif their == 'Y':
                score += 2
            elif their == 'Z':
                score += 3
        else:
            score += 6
            if their == 'X':
                score += 2
            elif their == 'Y':
                score += 3
            elif their == 'Z':
                score += 1

    print(f'Answer 2: {score}')
