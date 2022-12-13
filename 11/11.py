import re
from dataclasses import dataclass
from typing import Callable, List, Dict
from utils.inputs import get_input_blob


@dataclass
class Monkey:
    id: int
    items: List[int]
    operation: Callable
    test_modulo: int
    if_true_throw_to: int
    if_false_throw_to: int
    inspected_count: int = 0


def parse_single_monkey(monkey_blob) -> Monkey:
    '''
    Monkey 0:
    Starting items: 79, 98
    Operation: new = old * 19
    Test: divisible by 23
        If true: throw to monkey 2
        If false: throw to monkey 3
    '''
    monkey_id_re = re.compile(r'Monkey (?P<id>(\d+)):')
    operation_re = re.compile(r'\s*Operation: new = old\s*')
    if_true_re = re.compile(r'\s*If true: throw to monkey\s*')
    if_false_re = re.compile(r'\s*If false: throw to monkey\s*')

    lines = monkey_blob.split('\n')
    monkey_id = int(monkey_id_re.match(lines[0]).group('id'))

    _starting_items = lines[1].replace('Starting items: ', '')
    starting_items = [int(i) for i in _starting_items.split(',')]

    operation = operation_re.sub('', lines[2])
    op, factor = operation.split(' ')
    if factor == 'old':
        if op == '*':
            def functor(old):
                return old * old
        elif op == '+':
            def functor(old):
                return old + old
        else:
            raise Exception(f'Unknown operator {op}')
    else:
        factor = int(factor)
        if op == '*':
            def functor(old):
                return old * factor
        elif op == '+':
            def functor(old):
                return old + factor
        else:
            raise Exception(f'Unknown operator {op}')

    test_modulo = int(lines[3].replace('Test: divisible by ', ''))

    if_true_throw_to = int(if_true_re.sub('', lines[4]))
    if_false_throw_to = int(if_false_re.sub('', lines[5]))

    # print(monkey_id)
    # print(starting_items)
    # print(test_modulo)
    # print(repr(functor))
    # print(if_true_throw_to)
    # print(if_false_throw_to)
    return Monkey(
        monkey_id,
        starting_items,
        functor,
        test_modulo,
        if_true_throw_to,
        if_false_throw_to,
    )


def parse_monkeys(input_blob) -> Dict[int, Monkey]:
    monkey_lookup: Dict[int, Monkey] = {}
    monkey_txts = input_blob.split('\n\n')
    for monkey_txt in monkey_txts:
        m = parse_single_monkey(monkey_txt)
        monkey_lookup[m.id] = m

    return monkey_lookup


def main():
    input_txt = get_input_blob('input.txt')
    monkeys_lookup = parse_monkeys(input_txt)
    # print(monkeys_lookup)
    for _ in range(20):
        monkey_id = 0
        while monkey_id in monkeys_lookup:
            monkey = monkeys_lookup[monkey_id]
            while len(monkey.items) > 0:
                item = monkey.items.pop(0)
                monkey.inspected_count += 1
                worry_level: int = 0
                if monkey.operation.__code__.co_argcount == 0:
                    worry_level = monkey.operation()
                else:
                    worry_level = monkey.operation(item)

                worry_level //= 3

                if worry_level % monkey.test_modulo == 0:
                    throw_id = monkey.if_true_throw_to
                else:
                    throw_id = monkey.if_false_throw_to

                monkeys_lookup[throw_id].items.append(worry_level)

            monkey_id += 1

    m0, m1, *_ = sorted(monkeys_lookup.values(),
                        key=lambda m: m.inspected_count, reverse=True)
    print(f'Answer 1: {m0.inspected_count * m1.inspected_count}')

    monkeys_lookup = parse_monkeys(input_txt)
    ALL_MODULO = 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23
    for _ in range(10000):
        if _ % 1000 == 0:
            print(f'Round {_}')

        monkey_id = 0
        while monkey_id in monkeys_lookup:
            monkey = monkeys_lookup[monkey_id]

            while len(monkey.items) > 0:
                item = monkey.items.pop(0)
                monkey.inspected_count += 1
                worry_level: int = 0
                if monkey.operation.__code__.co_argcount == 0:
                    worry_level = monkey.operation()
                else:
                    worry_level = monkey.operation(item)

                worry_level %= ALL_MODULO

                if worry_level % monkey.test_modulo == 0:
                    throw_id = monkey.if_true_throw_to
                else:
                    throw_id = monkey.if_false_throw_to

                monkeys_lookup[throw_id].items.append(worry_level)
            monkey_id += 1

    m0, m1, *_ = sorted(monkeys_lookup.values(),
                        key=lambda m: m.inspected_count, reverse=True)
    print(f'Answer 2: {m0.inspected_count * m1.inspected_count}')


if __name__ == '__main__':
    main()
