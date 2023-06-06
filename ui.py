import time

from board import *
from algoritmos import *
from euristicas import *
import tkinter as tk
from enum import Enum

import numpy as np

from tkinter import *
from PIL import Image, ImageTk
from tkinter import *
import PIL.Image

SIZE = 3

# board setup

b = new_board(SIZE, SIZE)
b - shuffle(b)

root = tk.Tk()


def update_config_view():
    # remove all widgets from header

    for widget in header.winfo_children():
        widget.destroy()

    to_solve = ""
    # reset board button
    reset_button = tk.Button(header, text="RESET", width=5, height=1, command=reset_board)
    reset_button.grid(row=0, column=0)

    # shuffle button
    shuffle_button = tk.Button(header, text="SHUFFLE", width=5, height=1, command=shuffle_board)
    shuffle_button.grid(row=1, column=0)

    # algo dropdown
    algo_dropdown = tk.OptionMenu(header, selected_algo, *Algorithm.__members__.keys(), command=select_algo)
    algo_dropdown.config(width=10)
    algo_dropdown.grid(row=0, column=1)

    # if algo is astar or greedy
    if algo == Algorithm.A_ESTRELA or algo == Algorithm.BUSCA_GULOSA:
        # heuristic dropdown

        heuristic_dropdown = tk.OptionMenu(header, selected_heuristic, *HEURISTICS_MAP.keys(),
                                           command=select_heuristic)
        heuristic_dropdown.config(width=10)
        heuristic_dropdown.grid(row=1, column=1)

    if algo is not None:
        # solve button
        solve_button = tk.Button(header, text="SOLVE", width=5, height=1, command=solve)
        solve_button.grid(row=0, column=2)


        if resultados is not None:
            # next step button
            to_solve = len(resultados.solution)
            next_step_button = tk.Button(header, text="NEXT STEP", width=5, height=1, command=next_step)
            next_step_button.grid(row=1, column=2)
        # solution size label
        # solution_size_label = tk.Label(header, text="Solution size: " + str(len(resultados[solution_index])))
        # solution_size_label.grid(row=1, column=2)
    lab = tk.Label(header, text=f"S: {to_solve}")
    lab.grid(row=0, column=3)
    lab = tk.Label(header, text=f"M: {moves}")
    lab.grid(row=1, column=3)




def initialize_img_dict():
    dict = {}
    for i in range(1, SIZE * SIZE):
        fp = open(f'/home/andre/PycharmProjects/puzzleSolvingAlgo/crops/elp_{i}.png', "rb")
        img = PIL.Image.open(fp)

        dict[i] = img

    return dict


images = initialize_img_dict()


def update_view():
    # Remove all widgets from game_canvas
    for widget in game_canvas.winfo_children():
        widget.destroy()

    # Create buttons for each cell and place them in the grid
    index = 1
    print('------------------')
    for i in range(SIZE):
        for j in range(SIZE):
            if b[i][j] == 0:
                # red tile
                but = tk.Label(game_canvas, text="x", border=0, borderwidth=0.)
                but.grid(row=i, column=j)

            else:
                # image tile
                photo = ImageTk.PhotoImage(images[b[i][j]])
                but = tk.Button(game_canvas, image=photo, width=95, height=95, border=0, borderwidth=0.,
                                command=lambda x=i, y=j: button_click(x, y), )
                but.image = photo

                but.grid(row=i, column=j)
            index += 1


def button_click(x, y):
    global moves
    if (x, y) in get_valid_moves(b):
        swap_tiles(b, (x, y))
        print_board(b)
    update_view()
    moves += 1
    update_config_view()


def select_algo(event):
    global algo
    selected_value = selected_algo.get()
    algo = Algorithm[selected_value]
    print(algo)
    update_config_view()


HEURISTICS_MAP = {
    "MANHATTAN": manhattan_distance,
    "EUCLIDEAN": euclidean_distance,
    "HAMMING": hamming_distance,
}


def select_heuristic(event):
    global heuristic
    selected_value = selected_heuristic.get()
    heuristic = HEURISTICS_MAP[selected_value]
    print(selected_value)
    print(heuristic)


def solve():
    global resultados
    global solution_index
    print("searching")
    resultados = search(b, algo, heuristic=heuristic)
    solution_index = 0
    print(resultados.solution)
    update_config_view()



def next_step():
    global resultados
    global solution_index

    if solution_index >= len(resultados.solution):
        return

    x, y = resultados.solution[solution_index]
    button_click(x, y)

    solution_index += 1


def reset_board():
    global b
    global resultados
    global solution_index
    global moves
    b = new_board(SIZE, SIZE)
    resultados = None
    solution_index = None
    moves = 0
    update_view()


def shuffle_board():
    global b
    reset_board()
    b = shuffle(b)
    update_view()


moves = 0

solution_index = 0
resultados = None

algo = None
heuristic = None

# title
root.title("8 Puzzle da Super Cris")

# header
header = tk.Canvas(root)

selected_algo = tk.StringVar(header)
selected_heuristic = tk.StringVar(header)

header.pack()

# canvas
game_canvas = tk.Canvas(root)
game_canvas.pack()

update_view()
update_config_view()

root.mainloop()
