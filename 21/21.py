from functools import cache
from typing import Dict, Union, List
from utils.inputs import get_input_lines

ops = {
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y
}

monkeys: Dict[str, Union[int, List[str]]] = {}
@cache
def resolve(monkey_name: str) -> int:
    op = monkeys[monkey_name]
    # if monkeys[monkey_name] int:
    if isinstance(op, int):
        return op

    return ops[op[1]](resolve(op[0]), resolve(op[2]))

def main():
    monkey_lines = get_input_lines('./input.txt')
    # monkeys = {}
    for monkey_line in monkey_lines:
        monkey_name, op = monkey_line.split(': ')
        if op.count(' ') < 2:
            op = int(op)
            monkeys[monkey_name] = op
        else:
            op1, sign, op2 = op.split(' ')
            # print(op1, sign, op2)
            monkeys[monkey_name] = [op1, sign, op2]

    print(f'Answer 1: {int(resolve("root"))}')

    if isinstance(monkeys['root'], list):
        monkeys['root'][1] = '-'

    # search around by hand
    start = 3_059_361_892_900
    for i in range(start, start + 10000):
        resolve.cache_clear()
        monkeys['humn'] = i
        res = resolve('root')
        if res == 0:
            print(f'Answer 2: {i}')
            break

if __name__ == '__main__':
    main()
