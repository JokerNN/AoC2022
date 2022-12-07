from typing import Dict, List, Literal, Optional
from utils.inputs import get_input_lines

lines = get_input_lines('input.txt')


class FSEntry:
    def __init__(
        self: 'FSEntry',
        name: str,
        _type: Literal['dir', 'file'],
        parent: Optional['FSEntry'],
        size: int
    ) -> None:
        self.name = name
        self.type: Literal['dir', 'file'] = _type
        self.size = size
        self.parent: FSEntry

        if parent:
            self.parent = parent
        else:
            self.parent = self

        self.children : Optional[List[FSEntry]]

        if self.type == 'dir':
            self.children = []
        elif self.type == 'file':
            self.children = None
        else:
            raise Exception('Unknown file system type')


    def add_child(self, child: 'FSEntry'):
        if self.children is not None:
            self.children.append(child)
        else:
            raise Exception

    def find_child(self: 'FSEntry', child_name: str) -> 'FSEntry':
        if self.children is None:
            raise Exception
        for child in self.children:
            if child.name == child_name:
                return child
        raise Exception

    def __repr__(self: 'FSEntry'):
        if self.type == 'dir':
            return f'{self.name}: {repr(self.children)}'

        return f'{self.name}: {self.size}'


def main():
    fs_root = FSEntry('/', 'dir', None, 0)
    cur_dir = fs_root

    for line in lines[1:]:
        line = line.strip()

        if line.startswith('$ cd'):
            if line.startswith('$ cd ..'):
                cur_dir = cur_dir.parent
            else:
                cd_name = line.replace('$ cd ', '')
                cur_dir = cur_dir.find_child(cd_name)
        elif line.startswith('$ ls'):
            pass
        elif line.startswith('dir'):
            dir_name = line.replace('dir ', '')
            cur_dir.add_child(FSEntry(dir_name, 'dir', cur_dir, 0))
        else:
            [filesize, filename] = line.split()
            filesize = int(filesize)
            cur_dir.add_child(FSEntry(filename, 'file', cur_dir, filesize))


    sizes:Dict[str, int] = {}

    def calc_sizes(fs_node: FSEntry, name: str) -> int:
        if fs_node.children is None:
            raise Exception

        size = 0

        for child in fs_node.children:
            if child.type == 'dir':
                size += calc_sizes(child, name + '/' + child.name)
            elif child.type == 'file':
                size += child.size
        sizes[name] = size
        return size

    ans1 = 0
    calc_sizes(fs_root, '')
    for size in sizes.values():
        if size <= 100000:
            ans1 += size

    print(f'Answer 1: {ans1}')


    space_to_free = 30000000 - (70000000 - sizes[''])
    # print(sizes[''])
    # print(space_to_free)
    min_diff = float('inf')
    min_dir = ''
    for name, size in sizes.items():
        if space_to_free < size:
            if size - space_to_free < min_diff:
                min_diff = size - space_to_free
                min_dir = name

    print(f'Answer 2: {sizes[min_dir]}')


if __name__ == '__main__':
    main()
