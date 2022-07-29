import subprocess
import pickle
import os
import math
from enum import IntEnum
import tkinter as tk
import numpy as np
from PIL.Image import Resampling
from matplotlib import pyplot as plt
from numpy import uint8
from PIL import ImageTk, Image


class MazGui:
    def __init__(self, window):
        self.window = window
        self.window.title("Maze Gen")
        self.window.geometry("600x300")
        self.window.minsize(600, 300)
        for r in range(2):
            for c in range(2):
                tk.Label(self.window, borderwidth=0).grid(row=r, column=c)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=3)
        self.orig1 = Image.open("raw_maze.png")
        self.new1 = self.orig1
        self.img1 = ImageTk.PhotoImage(self.orig1, master=self.window)
        self.frame1 = tk.Label(self.window, image=self.img1)
        self.frame1.grid(row=1, column=0, sticky="NSEW")

        self.window.columnconfigure(1, weight=1)
        self.orig2 = Image.open("processed_maze.png")
        self.new2 = self.orig2
        self.img2 = ImageTk.PhotoImage(self.orig2, master=self.window)
        self.frame2 = tk.Label(self.window, image=self.img2)
        self.frame2.grid(row=1, column=1, sticky="NSEW")

        self.window.rowconfigure(0, weight=1)
        self.generate = tk.Button(
            text="Generate Maze",
            command=self.gen,
            bg="grey",
            fg="black"
        )
        self.generate.grid(row=0, column=1, sticky="NSEW")

        self.window.bind("<Configure>", self.resize_img)

        self.color = 'gray_r'

        self.curr_color = tk.StringVar(self.window)
        self.curr_color.set('gray_r')

        colors = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r',
                  'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r',
                  'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1',
                  'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr',
                  'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu',
                  'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2',
                  'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu',
                  'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn',
                  'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis',
                  'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix',
                  'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r',
                  'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r',
                  'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r',
                  'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r',
                  'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r',
                  'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring',
                  'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r',
                  'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r',
                  'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r']

        dropdown = tk.OptionMenu(self.window, self.curr_color, *colors)
        dropdown.grid(row=0, column=0, sticky="NSEW")

    def resize_img(self, event):
        height = int((self.window.winfo_height()) * (2 / 3))
        width = int((self.window.winfo_width() / 2) * (2 / 3))
        if height > width:
            height = width
        elif width > height:
            width = height

        print("H:", height, "W:", width)
        self.new1 = self.orig1.resize((height, width), Resampling.LANCZOS)
        self.img1 = ImageTk.PhotoImage(self.new1)
        self.frame1.config(image=self.img1)

        self.new2 = self.orig2.resize((height, width), Resampling.LANCZOS)
        self.img2 = ImageTk.PhotoImage(self.new2)
        self.frame2.config(image=self.img2)

    def gen(self):
        self.color = self.curr_color.get()
        prev = os.getcwd()
        os.chdir('.\\rustmaz')
        subprocess.call('cargo run -r')
        os.chdir(prev)
        gen_imgs(self.color)
        self.orig1 = Image.open("raw_maze.png")
        self.orig2 = Image.open("processed_maze.png")
        self.resize_img(event=None)


class Side(IntEnum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3


def gen_imgs(color):
    picklefile = open('./rustmaz/currmaze.mazdat', 'rb')
    marks = pickle.load(picklefile)
    picklefile.close()

    print(marks)
    print(type(marks))

    leng = len(marks)
    size = math.isqrt(leng)
    print(size)
    new_arr = np.reshape(np.array(marks, dtype=uint8), (size, size))

    big_arr = np.full(((size * 2 + 1), (size * 2 + 1)), 0, dtype=uint8)

    for (y, x), value in np.ndenumerate(new_arr):
        bin = "{:04b}".format(new_arr[y][x])
        for index, side in enumerate(bin):
            print(index, "(", side, ")", end=' ')
            big_arr[y * 2 + 1][x * 2 + 1] = 32

            match index:
                case Side.TOP:
                    if big_arr[y * 2][x * 2 + 1] == 0:
                        big_arr[y * 2][x * 2 + 1] = 32 * (1 - (ord(side) - 48))
                case Side.BOTTOM:
                    if big_arr[y * 2 + 2][x * 2 + 1] == 0:
                        big_arr[y * 2 + 2][x * 2 + 1] = 32 * (1 - (ord(side) - 48))
                case Side.LEFT:
                    if big_arr[y * 2 + 1][x * 2] == 0:
                        big_arr[y * 2 + 1][x * 2] = 32 * (1 - (ord(side) - 48))
                case Side.RIGHT:
                    if big_arr[y * 2 + 1][x * 2 + 2] == 0:
                        big_arr[y * 2 + 1][x * 2 + 2] = 32 * (1 - (ord(side) - 48))

        print()

    plt.imshow(new_arr, interpolation='nearest', cmap=color, vmin=0, vmax=15)
    plt.axis('off')
    plt.savefig('raw_maze.png', bbox_inches='tight', pad_inches=0, dpi=300)

    plt.imshow(big_arr, interpolation='nearest', cmap='gray', vmin=0, vmax=32)
    plt.axis('off')
    plt.savefig('processed_maze.png', bbox_inches='tight', pad_inches=0, dpi=300)

    for row in new_arr:
        print(row)


def main():
    gen_imgs('gray_r')
    window = tk.Tk()
    myapp = MazGui(window)
    window.mainloop()


if __name__ == '__main__':
    main()
