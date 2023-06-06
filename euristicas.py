import enum
from typing import Callable, Iterator, Optional, TypeAlias

import math


from board import *
manhattan_tables = {}

Heuristic: TypeAlias = Callable[[Board], int | float]


class Heuristics(enum.Enum):
    MANHATTAN = "Manhattan Distance"
    EUCLIDEAN = "Euclidean Distance"
    HAMMING = "Hamming Distance"


def euclidean_distance(board: Board) -> float:
    h, w = board.shape
    dist = 0.0
    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if BLANK == tile:
                continue
            goal_y, goal_x = get_goal_yx(h, w, tile)
            a, b = abs(y - goal_y), abs(x - goal_x)
            dist += math.sqrt(a**2 + b**2)
    return dist


def hamming_distance(board: Board) -> int:
    h, w = board.shape
    dist = 0
    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if BLANK == tile:
                continue
            goal_y, goal_x = get_goal_yx(h, w, tile)
            if y != goal_y or x != goal_x:
                dist += 1
    return dist


def prepare_manhattan_table(h, w) -> dict[tuple[int, int, int], int]:
    table = {}
    for y in range(h):
        for x in range(w):
            for tile in range(h * w):
                if BLANK == tile:
                    table[(y, x, tile)] = 0
                else:
                    goal_y, goal_x = get_goal_yx(h, w, tile)
                    table[(y, x, tile)] = abs(y - goal_y) + abs(x - goal_x)
    return table


def manhattan_distance(board: Board) -> int:

    h, w = board.shape
    table = manhattan_tables.get((h, w), None)
    if table is None:
        table = prepare_manhattan_table(h, w)
        manhattan_tables[(h, w)] = table

    dist = 0
    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            dist += table[(y, x, tile)]
    return dist
