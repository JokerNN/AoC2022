from typing import Set, Tuple
from utils.inputs import get_input_lines

TALLEST_TREE = 9


def main():
    _rows = get_input_lines('input.txt')
    rows = [[int(n) for n in row] for row in _rows]

    visible_trees: Set[Tuple[int, int]] = set()

    for row_idx, row in enumerate(rows):
        max_height = -float('inf')
        for col_idx, tree in enumerate(row):
            tree = int(tree)
            if tree > max_height:
                max_height = tree
                visible_trees.add((row_idx, col_idx))
            if max_height >= TALLEST_TREE:
                break

    for row_idx, row in enumerate(rows):
        max_height = -float('inf')
        for col_idx, tree in reversed(list(enumerate(row))):
            tree = int(tree)
            if tree > max_height:
                max_height = tree
                visible_trees.add((row_idx, col_idx))
            if max_height >= TALLEST_TREE:
                break

    for col_idx in range(len(rows[0])):
        max_height = -float('inf')
        for row_idx, row in enumerate(rows):
            tree = int(rows[row_idx][col_idx])
            if tree > max_height:
                max_height = tree
                visible_trees.add((row_idx, col_idx))
            if max_height >= TALLEST_TREE:
                break

    for col_idx in range(len(rows[0])):
        max_height = -float('inf')
        for row_idx, row in reversed(list(enumerate(rows))):
            tree = int(rows[row_idx][col_idx])
            if tree > max_height:
                max_height = tree
                visible_trees.add((row_idx, col_idx))
            if max_height >= TALLEST_TREE:
                break

    print(f'Answer 1: {len(visible_trees)}')

    best_tree = -float('inf')
    for row_idx, row in enumerate(rows):
        for col_idx, tree in enumerate(row):
            top_view, bottom_view, right_view, left_view = (0, 0, 0, 0)
            for r_idx in range(row_idx + 1, len(row)):
                bottom_view += 1
                if rows[r_idx][col_idx] >= tree:
                    break

            for r_idx in range(row_idx - 1, -1, -1):
                top_view += 1
                if rows[r_idx][col_idx] >= tree:
                    break

            for c_idx in range(col_idx - 1, -1, -1):
                left_view += 1
                if row[c_idx] >= tree:
                    break

            for c_idx in range(col_idx + 1, len(rows[0])):
                right_view += 1
                if row[c_idx] >= tree:
                    break

            best_tree = max(top_view * right_view *
                            bottom_view * left_view, best_tree)

    print(f'Answer 2: {best_tree}')


if __name__ == '__main__':
    main()
