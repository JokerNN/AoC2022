inp = None

with open('d:/AoC2022/1/input.txt') as blob:
    inp = blob.read()
    elf_inputs = inp.split('\n\n')
    elfs = []
    for elf_input in elf_inputs:
        elfs.append(sum(int(n) for n in elf_input.split('\n')))

    print(max(elfs))
    elfs.sort()
    print(sum(elfs[-3:]))
