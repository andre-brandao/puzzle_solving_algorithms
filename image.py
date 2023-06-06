import os

from PIL import Image
from itertools import product

dir_out= "//crops"

def crop_image_into_grid(image_path, num_rows, num_columns):

    # Load the image
    image = Image.open(image_path)

    # Get the size of the image
    width, height = image.size

    # Calculate the size of each cell
    cell_width = width // num_columns
    cell_height = height // num_rows

    cropped_images = []
    index = 1
    for i in range(num_rows):
        for j in range(num_columns):
            # Crop the image for the current cell
            out = os.path.join(dir_out, f'cris2_{index}.png')

            left = j * cell_width
            top = i * cell_height
            right = (j + 1) * cell_width
            bottom = (i + 1) * cell_height
            image.crop((left, top, right, bottom)).save(out)


            index += 1

    return cropped_images

#tile(filename="elephant.png", dir_in="/home/andre/PycharmProjects/puzzleSolvingAlgo", dir_out="/home/andre/PycharmProjects/puzzleSolvingAlgo/crops", d=290)

crop_image_into_grid(image_path="//cris2.jpg", num_rows=3, num_columns=3)