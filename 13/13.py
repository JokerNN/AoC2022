from typing import List, Optional, Union
from utils.inputs import get_input_blob

RecList = Union[List['RecList'], int]

def cmp(l: RecList, r: RecList) -> Optional[bool]:
    if isinstance(l, int) and isinstance(r, int):
        if l == r:
            return None
        return l < r

    if isinstance(l, int):
        return cmp ([l], r)

    if isinstance(r, int):
        return cmp(l, [r])

    for idx in range(min(len(l), len(r))):
        cmp_res = cmp(l[idx], r[idx])
        if cmp_res is None:
            continue

        return cmp_res

    if len(l) > len(r):
        return False
    if len(l) < len(r):
        return True

    return None

def main():
    inp = get_input_blob('./input.txt')
    idx = 1
    total = 0
    for pair in inp.split('\n\n'):
        l, r = pair.split()
        left_list = eval(l) # pylint: disable=eval-used
        right_list = eval(r) # pylint: disable=eval-used

        res = cmp(left_list, right_list)
        # print(f'Comparing: {left_list} and {right_list}: {res}')
        if res:
            total += idx
        idx += 1


    print(f'Answer 1: {total}')
    lists = []

    for line in inp.split('\n'):
        if line == '':
            continue
        lists.append(eval(line)) # pylint: disable=eval-used


    less_than_2 = 1
    less_than_6 = 2

    for l in lists:
        if cmp(l, [[2]]) is True:
            less_than_2 += 1
            less_than_6 += 1
        elif cmp(l, [[6]]) is True:
            less_than_6 += 1

    print(f'Answer 2: {less_than_2 * less_than_6}')


if __name__ =='__main__':
    main()
