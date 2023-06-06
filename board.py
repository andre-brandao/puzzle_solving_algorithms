import itertools
import random
import sys
from typing import Iterable, Iterator, Optional, TypeAlias

import numpy as np
import numpy.typing as npt

grid_size = 4
BLANK = 0
Board: TypeAlias = npt.NDArray
FrozenBoard: TypeAlias = tuple[tuple[int, ...], ...]


def new_board(h: int, w: int) -> Board:
    board = np.arange(1, 1 + h * w, ).reshape(h, w)
    board[-1, -1] = BLANK
    return board


def copy_board(board: Board) -> FrozenBoard:
    return tuple(tuple(int(col) for col in row) for row in board)


def print_board(board: Board, file=sys.stdout) -> None:
    board_size = len(board) * len(board[0])
    # the longest str we need to print is the largest tile number
    max_width = len(str(board_size - 1))
    for row in board:
        for tile in row:
            if tile == BLANK:
                print(" " * max_width, end=" ", file=file)
            else:
                print(str(tile).rjust(max_width), end=" ", file=file)
        print(file=file)


def get_goal_y(h: int, w: int, tile: int) -> int:
    if BLANK == tile:
        return h - 1
    return (tile - 1) // w


def get_goal_x(h: int, w: int, tile: int) -> int:
    if BLANK == tile:
        return w - 1
    return (tile - 1) % w


def get_goal_yx(h: int, w: int, tile: int) -> tuple[int, int]:
    return get_goal_y(h, w, tile), get_goal_x(h, w, tile)


def find_tile(board: Board | FrozenBoard, tile: int) -> tuple[int, int]:
    if isinstance(board, np.ndarray):
        y, x = np.where(board == tile)
        return y[0], x[0]
    for y, row in enumerate(board):
        for x in range(len(row)):
            if board[y][x] == tile:
                return y, x
    raise ValueError(f'There is no tile "{tile}" on the board.')


def find_blank(board: Board | FrozenBoard) -> tuple[int, int]:
    return find_tile(board, BLANK)


def get_valid_moves(
        board: Board | FrozenBoard,
        blank_pos: Optional[tuple[int, int]] = None,
) -> list[tuple[int, int]]:
    if blank_pos is None:
        blank_pos = find_blank(board)
    y, x = blank_pos
    moves = []
    for dy, dx in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        if 0 <= y + dy < len(board) and 0 <= x + dx < len(board[0]):
            moves.append((y + dy, x + dx))
    return moves


def swap_tiles(
        board: Board,
        tile1: tuple[int, int] | int,
        tile2: Optional[tuple[int, int] | int] = None,
) -> Board:
    r"""
    Mutates the board by swapping a pair of tiles.
    """
    if isinstance(tile1, int) or isinstance(tile1, np.integer):
        tile1 = find_tile(board, tile1)
    if isinstance(tile2, int) or isinstance(tile2, np.integer):
        tile2 = find_tile(board, tile2)
    elif tile2 is None:
        tile2 = find_blank(board)

    y1, x1 = tile1
    y2, x2 = tile2
    board[y1, x1], board[y2, x2] = board[y2, x2], board[y1, x1]

    return board


def count_inversions(board: Board) -> int:
    _, w = board.shape
    board_size = np.prod(board.shape)
    inversions = 0
    for i in range(board_size):
        t1 = board[i // w, i % w]
        if t1 == BLANK:
            continue
        for j in range(i + 1, board_size):
            t2 = board[j // w, j % w]
            if t2 == BLANK:
                continue
            if t2 < t1:
                inversions += 1
    return inversions


def is_solvable(board: Board) -> bool:
    r"""
    Determines if it is possible to solve this board.

    Note:
        The algorithm counts `inversions`_ to determine solvability.
        The "standard" algorithm has been modified here to support
        non-square board sizes.

    Args:
        board: The puzzle board.

    Returns:
        bool: True if the board is solvable, False otherwise.
    """
    inversions = count_inversions(board)
    h, w = board.shape
    if w % 2 == 0:
        y, _ = find_blank(board)
        if h % 2 == 0:
            if (inversions + y) % 2 != 0:
                return True
        else:
            if (inversions + y) % 2 == 0:
                return True
    elif inversions % 2 == 0:
        return True


def visit(visited: set[FrozenBoard], board: Board) -> bool:
    r"""
    Helper to check if this state already exists. Otherwise, record it.
    Returns True if we have already been here, False otherwise.

    Args:
        visited: Set of boards already seen.
        board: The current board.

    Returns:
        True if we've been here before.
    """
    frozen_board = copy_board(board)
    if frozen_board in visited:
        return True
    visited.add(frozen_board)
    return False


def shuffle(board: Board) -> Board:
    h, w = board.shape
    while True:
        for y in range(h):
            for x in range(w):
                pos1 = y, x
                pos2 = random.randrange(h), random.randrange(w)
                swap_tiles(board, pos1, pos2)
        if is_solvable(board):
            return board

def solution_as_tiles(board: Board, solution: Iterable[tuple[int, int]]) -> list[int]:
    r"""
    Converts a list of (y, x)-coords indicating moves into tile numbers,
    given a starting board configuration.

    Args:
        board: The initial board we will apply moves to (does not alter board).
        solution: A list of move coordinates in (y, x) form.

    Returns:
        A list of ints, which indicate a sequence of tile numbers to move.
    """
    board = np.copy(board)
    tiles = []
    blank_pos = find_blank(board)
    for move in solution:
        y, x = move
        tiles.append(int(board[y][x]))
        swap_tiles(board, blank_pos, move)
        blank_pos = move
    return tiles
