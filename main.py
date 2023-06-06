from PIL import ImageTk

from board import *
import tkinter as tk

from PIL import Image
from tkinter import *
import PIL.Image
SIZE = 3

# board setup

b = new_board(SIZE, SIZE)
# b = shuffle(b)

root = tk.Tk()


def update_view():
    game_canvas.delete("all")  #
    # Create buttons for each cell and place them in the grid
    index = 1

    for i in range(SIZE):
        for j in range(SIZE):
            if b[i][j] == 0:
                label = tk.Label(game_canvas, text=" ")
                label.grid(row=i, column=j)
            else:
                # print(f'/home/andre/PycharmProjects/puzzleSolvingAlgo/crops/elp_{index}.png')
                fp = open(f'//crops/elp_{index}.png', "rb")
                img = PIL.Image.open(fp)
                photo = ImageTk.PhotoImage(img)
                but = tk.Button(game_canvas, image=photo, width=90, height=90, border=0, borderwidth=0., command=lambda x=i, y=j: button_click(x, y),)
                but.image = photo
                but.grid(row=i, column=j)

            index += 1


def button_click(x, y):
    if (x, y) in get_valid_moves(b):
        swap_tiles(b, (x, y))
        print_board(b)
    update_view()


# canvas
game_canvas = tk.Canvas(root)
game_canvas.pack()

update_view()

root.mainloop()
