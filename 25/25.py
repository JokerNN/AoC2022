from utils.inputs import get_input_lines

snafu_dec_map = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2
}
def snafu_to_dec(snafu_num: str) -> int:
    res = 0
    for power, dig in enumerate(reversed(snafu_num)):
        res += snafu_dec_map[dig] * 5 ** power

    return res

def snafu_inc(snafu_num: str) -> str:
    snum = list(reversed(snafu_num))
    for idx, char in enumerate(snum):
        if char == '2':
            snum[idx] = '='
            continue

        if char == '1':
            snum[idx] = '2'
            break

        if char == '0':
            snum[idx] = '1'
            break

        if char == '-':
            snum[idx] = '0'
            break
        if char == '=':
            snum[idx] = '-'
            break

    else:
        snum.append('1')

    return ''.join(reversed(snum))


# print(snafu_inc('212'))
# print(snafu_to_dec('22='))

def dec_to_snafu(dec_num: int) -> str:
    pass

def main():
    snafu_nums = get_input_lines('./input.txt')
    dec_sum = sum(snafu_to_dec(snum) for snum in snafu_nums)
    print(f'Answer 1 decimal: {dec_sum}')
    snum = '12=================='
    snum = '121=2=1==0=10=2-20=='
    while snafu_to_dec(snum) < dec_sum:
        snum = snafu_inc(snum)

    if snafu_to_dec(snum) == dec_sum:
        print(f'Answer 1 snafu: {snum}')
    # print(snafu_to_dec('121=2=1==0=10=2-20=2'))

if __name__ == '__main__':
    main()
