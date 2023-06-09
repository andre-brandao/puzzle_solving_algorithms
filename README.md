# Puzzle solving search algorithms


## Description
This project is a python implementation of the following search algorithms: **A Star, BFS, DFS, and Greedy Search.**

If you are using the A* or Greedy Search algorithms, you can choose between the following heuristics: **Manhattan Distance, Euclidean Distance, and Hamming Distance.**

The algorithms are used to solve the 8-puzzle problem. The 8-puzzle problem is a puzzle invented and popularized by Noyes Palmer Chapman in the 1870s. It is played on a 3-by-3 grid with 8 square blocks labeled 1 through 8 and a blank square. The goal is to rearrange the blocks so that they are in order. The blank square is represented by the number 0. The following is an example of a 8-puzzle problem:

![App Screenshot 1](rdme_images/solver_print.png)

## How search algorithms work

![App Screenshot 2](rdme_images/puzzle_search.jpg)

For each valid move it creates a new board and compares it to the goal board. If the new board is the goal board, the algorithm stops and returns the solution. If the new board is not the goal board, it adds the new board to the queue and continues to the next valid move. The algorithm continues until it finds the goal board or the queue is empty.

## How to use the program

```
git clone https://github.com/andre-brandao/puzzle_solving_algorithms.git

cd puzzle_solving_algorithms

python3 ui.py
```
