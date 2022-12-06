import sys

sys.path.append('../AOC2022')

from utils.inputs import get_input_lines


def main():
    signal = get_input_lines('input.txt')[0]
    for idx in range(len(signal)):
        package = signal[idx: idx + 4]
        if len(set(package)) == 4:
            print(f'Answer 1: {idx + 4}')
            break

    for idx in range(len(signal)):
        package = signal[idx: idx + 14]
        if len(set(package)) == 14:
            print(f'Answer 2: {idx + 14}')
            return




if __name__ == '__main__':
    main()
