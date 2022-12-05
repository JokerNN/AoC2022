import os
import sys


def get_input_blob(filename: str) -> str:
    with open(os.path.join(sys.path[0], filename), encoding='utf-8') as file:
        return file.read()

def get_input_lines(filename: str):
    with open(os.path.join(sys.path[0], filename), encoding='utf-8') as file:
        file.readlines()
