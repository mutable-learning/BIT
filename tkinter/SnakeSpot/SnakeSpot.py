# This is a minesweeper clone using snakes

import os
import math
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from itertools import product
from random import sample
from time import sleep


class SnakeSpot(tk.Tk):
    def __init__(self, size=[5, 5]):
        super().__init__()
        self.size = size
        self.tiles = set()
        self.configure_ui()
        self.create_widgets()

    def configure_ui(self):
        self.title(
            "SnakeSpot - Can you spot all the snakes without getting bitten?")
        self.geometry("400x400")
        self.load_images()

        self.style = ttk.Style(self)
        self.style.configure("TLabel", background="lightgreen")
        self.style.configure("TFrame", background="green")

    def create_widgets(self):
        self.backyard = ttk.Frame(self, relief="groove", padding=3)
        self.backyard.pack(expand=1)

        # create the tiles where the snakes are hiding
        for x in range(self.size[0]):
            self.backyard.columnconfigure(x, minsize=25)
            for y in range(self.size[1]):
                self.tile = ttk.Label(
                    self.backyard,
                    relief="raised",
                    anchor="center"
                )
                self.tile.grid(column=x, row=y, sticky=tk.NSEW)
                self.tile.location = (x, y)
                self.tile.bind("<Button-1>", self.cut_grass)
                self.tile.bind("<Button-3>", self.flag_snake)

                # Save the tile location to the set of all tiles
                self.tiles.add(self.tile.location)

        for y in range(self.size[1]):
            self.backyard.rowconfigure(y, minsize=25)

        # Create the random snakes hiding in our backyard
        self.get_snakes()

    def load_images(self):
        path = os.path.dirname(os.path.abspath(__file__)) + "/images"
        img_size = 20

        # Load image for a snake
        snake = Image.open(f"{path}/snake.png")
        snake.thumbnail([img_size, img_size])
        self.snake = ImageTk.PhotoImage(snake)

        # Load image for a flag
        flag = Image.open(f"{path}/flag.png")
        flag.thumbnail([img_size, img_size])
        self.flag = ImageTk.PhotoImage(flag)

    def get_snakes(self):
        # 10% of tiles will have a snake
        number = math.ceil((self.size[0] * self.size[1]) * 0.1)
        self.snakes = set(sample(list(self.tiles), number))

    def cut_grass(self, event):
        if event.widget.location in self.snakes:
            event.widget["image"] = self.snake
            self.update_idletasks()
            print("Oh no. You were bitten by a snake.")
            print("You had better get to the hospital!")
            sleep(3)
            self.quit()
        else:
            self.show_hints(event.widget.location)

    def flag_snake(self, event):
        if event.widget["image"] == "":
            event.widget["image"] = self.flag
        else:
            event.widget["image"] = ""

    def get_hint(self, location):
        tiles = self.get_adjacent_tiles(location)
        return len(tiles & self.snakes)

    def get_adjacent_tiles(self, location):
        x, y = location
        possibles = set(product(range(x-1, x+2), range(y-1, y+2)))
        return possibles & self.tiles

    def show_hints(self, location):
        tiles = self.get_adjacent_tiles(location)
        for t in tiles:
            widgets = self.backyard.grid_slaves(column=t[0], row=t[1])
            if len(widgets) == 0:
                continue
            else:
                widget = widgets[0]
                hint = self.get_hint(widget.location)
                if widget.location == location:
                    widget.grid_forget()
                elif hint == 0:
                    widget.grid_forget()
                    self.show_hints(widget.location)
                else:
                    widget.config(text=hint)


if __name__ == "__main__":
    root = SnakeSpot(size=[10, 12])
    root.mainloop()
