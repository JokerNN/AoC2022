import re
from utils.inputs import get_input_blob

inp = get_input_blob('input.txt')

stacks_str, commands_str = inp.split('\n\n')
stacks_split = [list(line) for line in stacks_str.split('\n')]
stacks_linear = list(zip(*stacks_split[::-1]))
stacks_filtered = filter(lambda s: s[0] != ' ', stacks_linear)

stacks = []
for stack in stacks_filtered:
    s = list(stack)
    s = [c for c in s if c != ' ']
    stacks.append(s)

pattern = re.compile(r'move (?P<move_count>\d+) from (?P<from_stack>\d+) to (?P<to_stack>\d+)')
for command in commands_str.strip().split('\n'):
    # print(command)
    m = pattern.match(command)
    if m is None:
        raise Exception()
    move_count = int(m.group('move_count'))
    from_stack = int(m.group('from_stack'))
    to_stack = int(m.group('to_stack'))

    buffer = stacks[from_stack - 1][-move_count:]
    stacks[from_stack - 1][-move_count:] = []
    buffer = buffer[::-1]
    stacks[to_stack - 1].extend(buffer)
    # print(stacks)

tops = ''.join([s[-1] for s in stacks])
print(f'Answer 1: {tops}')


inp = get_input_blob('input.txt')

stacks_str, commands_str = inp.split('\n\n')
stacks_split = [list(line) for line in stacks_str.split('\n')]
stacks_linear = list(zip(*stacks_split[::-1]))
stacks_filtered = filter(lambda s: s[0] != ' ', stacks_linear)

stacks = []
for stack in stacks_filtered:
    s = list(stack)
    s = [c for c in s if c != ' ']
    stacks.append(s)

pattern = re.compile(r'move (?P<move_count>\d+) from (?P<from_stack>\d+) to (?P<to_stack>\d+)')
for command in commands_str.strip().split('\n'):
    # print(command)
    m = pattern.match(command)
    if m is None:
        raise Exception()
    move_count = int(m.group('move_count'))
    from_stack = int(m.group('from_stack'))
    to_stack = int(m.group('to_stack'))

    buffer = stacks[from_stack - 1][-move_count:]
    stacks[from_stack - 1][-move_count:] = []
    stacks[to_stack - 1].extend(buffer)
    # print(stacks)

tops = ''.join([s[-1] for s in stacks])
print(f'Answer 2: {tops}')
