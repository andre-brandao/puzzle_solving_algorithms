import collections
import heapq
import logging
from states import State, SearchResult
from euristicas import *

log = logging.getLogger(__name__)


class Algorithm(enum.Enum):
    A_ESTRELA = "a*"
    BUSCA_LARGURA = "bfs"
    BUSCA_PROFUNDIDADE = "dfs"
    BUSCA_GULOSA = "greedy"
    DIJKSTRA = "dijkstra"


def get_next_states(state: State) -> list[State]:
    moves = get_valid_moves(state.board, state.blank_pos)
    next_states = []
    for move in moves:
        # construct altered board
        next_board = np.copy(state.board)
        swap_tiles(next_board, state.blank_pos, move)
        # update history
        next_history = state.history.copy()
        next_history.append(move)
        # after moving, the move is now the blank_pos
        next_state = State(next_board, move, next_history)
        next_states.append(next_state)
    return next_states


def a_star(board: Board, **kwargs) -> SearchResult:
    r"""
    Args:
        board: The board
        depth_bound (int): A limit to search depth. Default is :math:`\infty`.
        f_bound (float): A limit on state cost. Default is :math:`\infty`.
        detect_dupes (bool): Duplicate detection (i.e. track visited states).
            Default is ``True``.
        heuristic: A function that maps boards to an estimated cost-to-go.
            Default is :func:`slidingpuzzle.heuristics.linear_conflict_distance`.
        weight (float): A constant multiplier on heuristic evaluation

    Returns:
        A :class:`slidingpuzzle.state.SearchResult` with a solution and statistics
    """
    # args
    depth_bound = kwargs.get("depth_bound", float("inf"))
    f_bound = kwargs.get("f_bound", float("inf"))
    detect_dupes = kwargs.get("detect_dupes", True)
    heuristic = kwargs.get("heuristic", manhattan_distance)
    weight = kwargs.get("weight", 1)

    # initial state
    goal = new_board(*board.shape)
    initial_state = State(np.copy(board), find_blank(board))
    unvisited = [initial_state]
    visited: set[FrozenBoard] = set()

    # stats
    generated, expanded = 0, 0

    while unvisited:
        state = heapq.heappop(unvisited)
        expanded += 1

        # goal check
        if np.array_equal(goal, state.board):
            return SearchResult(
                board, generated, expanded, unvisited, visited, state.history
            )

        # bound
        if len(state.history) > depth_bound or state.f > f_bound:
            continue

        # duplicate detection
        if detect_dupes and visit(visited, state.board):
            continue

        # children
        next_states = get_next_states(state)
        for state in next_states:
            state.g = len(state.history)
            state.f = state.g + weight * heuristic(state.board)
            heapq.heappush(unvisited, state)
        generated += len(next_states)

    # if we are here, no solution was found
    return SearchResult(board, generated, expanded, unvisited, visited, None)


def bfs(board: Board, **kwargs) -> SearchResult:
    r"""
    Breadth-first search

    Args:
        board: The board
        depth_bound (int): A limit to search depth. Default is :math:`\infty`.
        detect_dupes (bool): Duplicate detection (i.e. track visited states).
            Default is ``True``.

    Returns:
        A :class:`slidingpuzzle.state.SearchResult` with a solution and statistics
    """
    # args
    depth_bound = kwargs.get("depth_bound", float("inf"))
    detect_dupes = kwargs.get("detect_dupes", True)

    # initial state
    goal = new_board(*board.shape)
    initial_state = State(np.copy(board), find_blank(board))
    unvisited = collections.deque([initial_state])
    visited: set[FrozenBoard] = set()

    # stats
    generated, expanded = 0, 0

    while unvisited:
        state = unvisited.popleft()
        expanded += 1

        # goal check
        if np.array_equal(goal, state.board):
            return SearchResult(
                board, generated, expanded, unvisited, visited, state.history
            )

        # bound
        if len(state.history) > depth_bound:
            continue

        # duplicate detection
        if detect_dupes and visit(visited, state.board):
            continue

        # children
        next_states = get_next_states(state)
        unvisited.extend(next_states)
        generated += len(next_states)

    # if we are here, no solution was found
    return SearchResult(board, generated, expanded, unvisited, visited, None)


def dfs(board: Board, **kwargs) -> SearchResult:
    r"""
    Depth-first search

    Args:
        board: The board
        depth_bound (int): A limit to search depth. Default is :math:`\infty`.
        detect_dupes (bool): Duplicate detection (i.e. track visited states).
            Default is ``True``.

    Returns:
        A :class:`slidingpuzzle.state.SearchResult` with a solution and statistics
    """
    # args
    depth_bound = kwargs.get("depth_bound", float("inf"))
    detect_dupes = kwargs.get("detect_dupes", True)

    # initial state
    goal = new_board(*board.shape)
    initial_state = State(np.copy(board), find_blank(board))
    unvisited = [initial_state]
    visited: set[FrozenBoard] = set()

    # stats
    generated, expanded = 0, 0

    while unvisited:
        state = unvisited.pop()
        expanded += 1

        # goal check
        if np.array_equal(goal, state.board):
            return SearchResult(
                board, generated, expanded, unvisited, visited, state.history
            )

        # bound
        if len(state.history) > depth_bound:
            continue

        # duplicate detection
        if detect_dupes and visit(visited, state.board):
            continue

        # children
        next_states = get_next_states(state)
        unvisited.extend(next_states)
        generated += len(next_states)

    # if we are here, no solution was found
    return SearchResult(board, generated, expanded, unvisited, visited, None)


def greedy(board: Board, **kwargs) -> SearchResult:
    r"""
    Greedy best-first search. This search orders all known states using the provided
    heuristic and greedily chooses the state closest to the goal.

    Args:
        board: The board
        depth_bound (int): A limit to search depth. Default is :math:`\infty`.
        f_bound (float): A limit on state cost. Default is :math:`\infty`.
        detect_dupes (bool): Duplicate detection (i.e. track visited states).
            Default is ``True``.
        heuristic: A function that maps boards to an estimated cost-to-go.
            Default is :func:`slidingpuzzle.heuristics.linear_conflict_distance`.


    """
    # args
    depth_bound = kwargs.get("depth_bound", float("inf"))
    f_bound = kwargs.get("f_bound", float("inf"))
    detect_dupes = kwargs.get("detect_dupes", True)
    heuristic = kwargs.get("heuristic", manhattan_distance)

    # initial state
    goal = new_board(*board.shape)
    initial_state = State(np.copy(board), find_blank(board))
    unvisited = [initial_state]
    visited: set[FrozenBoard] = set()

    # stats
    generated, expanded = 0, 0

    while unvisited:
        state = heapq.heappop(unvisited)
        expanded += 1

        # goal check
        if np.array_equal(goal, state.board):
            return SearchResult(
                board, generated, expanded, unvisited, visited, state.history
            )

        # bound
        if len(state.history) > depth_bound or state.f > f_bound:
            continue

        # duplicate detection
        if detect_dupes and visit(visited, state.board):
            continue

        # children
        next_states = get_next_states(state)
        for state in next_states:
            state.f = heuristic(state.board)
            heapq.heappush(unvisited, state)
        generated += len(next_states)

    # if we are here, no solution was found
    return SearchResult(board, generated, expanded, unvisited, visited, None)

def dijkistra(board: Board, **kwargs) -> SearchResult:
    r"""
    Dijkistra search. This search orders all known states using the provided
    heuristic and greedily chooses the state closest to the goal.

    Args:
        board: The board
        depth_bound (int): A limit to search depth. Default is :math:`\infty`.
        detect_dupes (bool): Duplicate detection (i.e. track visited states).
            Default is ``True``.
        heuristic: A function that maps boards to an estimated cost-to-go.
            Default is :func:`slidingpuzzle.heuristics.linear_conflict_distance`.
    """
    # args
    depth_bound = kwargs.get("depth_bound", float("inf"))
    detect_dupes = kwargs.get("detect_dupes", True)
    heuristic = kwargs.get("heuristic", manhattan_distance)

    # initial state
    goal = new_board(*board.shape)
    initial_state = State(np.copy(board), find_blank(board))
    unvisited = [initial_state]
    visited: set[FrozenBoard] = set()

    # stats
    generated, expanded = 0, 0

    while unvisited:
        state = heapq.heappop(unvisited)
        expanded += 1

        # goal check
        if np.array_equal(goal, state.board):
            return SearchResult(
                board, generated, expanded, unvisited, visited, state.history
            )

        # bound
        if len(state.history) > depth_bound:
            continue

        # duplicate detection
        if detect_dupes and visit(visited, state.board):
            continue

        # children
        next_states = get_next_states(state)
        for state in next_states:
            state.f = heuristic(state.board)
            heapq.heappush(unvisited, state)
        generated += len(next_states)

    # if we are here, no solution was found
    return SearchResult(board, generated, expanded, unvisited, visited, None)


ALGORITHMS_MAP = {
    Algorithm.A_ESTRELA: a_star,
    Algorithm.BUSCA_LARGURA: bfs,
    Algorithm.BUSCA_PROFUNDIDADE: dfs,
    Algorithm.BUSCA_GULOSA: greedy,
    Algorithm.DIJKSTRA: dijkistra,

}


def search(board: Board, alg: Algorithm | str = Algorithm.A_ESTRELA, **kwargs) -> SearchResult:
    print("Iniciando Busca...")



    alg = Algorithm(alg)

    print(f"Algorithm {alg}")

    if alg == Algorithm.BUSCA_GULOSA or alg == Algorithm.A_ESTRELA:
        heuristic = kwargs.get("heuristic", manhattan_distance)
        print(f"Heuristic:  {heuristic.__name__}")

    if not is_solvable(board):
        raise ValueError(f"The provided board is not solvable:\n{board}")
    return ALGORITHMS_MAP[alg](board, **kwargs)