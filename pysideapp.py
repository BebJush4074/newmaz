# TODO - Checkout Streamlit and Abstra

import math
import os
import pickle
import subprocess
import sys
import rustmaz
from enum import IntEnum

import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui
from matplotlib import pyplot as plt
from numpy import uint8

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

class Side(IntEnum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3


def gen_imgs(color):
    marks = rustmaz.startup()
    # marks = pickle.load(picklefile)
    # picklefile.close()

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

    plt.imshow(new_arr, interpolation='nearest', cmap=color, vmin=0, vmax=15, aspect='equal')
    plt.axis('off')
    plt.savefig('raw_maze.png', bbox_inches='tight', pad_inches=0, dpi=300)

    plt.imshow(big_arr, interpolation='nearest', cmap='gray', vmin=0, vmax=32, aspect='equal')
    plt.axis('off')
    plt.savefig('processed_maze.png', bbox_inches='tight', pad_inches=0, dpi=300)

    for row in new_arr:
        print(row)


class MyApp(QtWidgets.QWidget):
    def __init__(self):
        self.threadpool = QtCore.QThreadPool
        self.color = 'gray_r'
        super().__init__()

        self.setMinimumSize(400, 300)

        self.setWindowTitle("Maze Generator!")

        self.icon = QtGui.QIcon()
        self.icon.addFile("char_m.png")
        self.setWindowIcon(self.icon)

        self.colorbox = QtWidgets.QComboBox()
        self.colorbox.addItems(colors)
        self.colorbox.setCurrentText("gray_r")

        self.gen_button = QtWidgets.QPushButton()
        self.gen_button.setText("Generate Maze")

        if self.height() > self.width():
            im_size = self.width() / 2
        elif self.width() > self.height():
            im_size = self.height() * (4 / 6)
        else:
            im_size = self.height()

        self.raw_im = QtGui.QPixmap("raw_maze.png")
        self.raw_holder = QtWidgets.QLabel(self)
        self.raw_holder.setPixmap(self.raw_im.scaled(im_size, im_size))

        self.proc_im = QtGui.QPixmap("processed_maze.png")
        self.proc_holder = QtWidgets.QLabel(self)
        self.proc_holder.setPixmap(self.proc_im.scaled(im_size, im_size))

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.colorbox, 0, 0)
        self.layout.addWidget(self.gen_button, 0, 1)
        self.layout.addWidget(self.raw_holder, 1, 0)
        self.layout.addWidget(self.proc_holder, 1, 1)

        self.colorbox.currentTextChanged.connect(self.update_color)
        self.gen_button.clicked.connect(self.gen)

    def update_color(self, s):
        self.color = s
        print(s)

    def gen(self):
        prev = os.getcwd()

        gen_imgs(self.color)
        if self.height() > self.width():
            im_size = self.width() / 2
        elif self.width() > self.height():
            im_size = self.height() * (2 / 3)
        else:
            im_size = self.height()
        self.raw_im = QtGui.QPixmap("raw_maze.png")
        self.raw_holder.setPixmap(self.raw_im.scaled(im_size, im_size))

        self.proc_im = QtGui.QPixmap("processed_maze.png")
        self.proc_holder.setPixmap(self.proc_im.scaled(im_size, im_size))

    def resizeEvent(self, event):
        if self.height() > self.width():
            im_size = self.width() / 2
        elif self.width() > self.height():
            im_size = self.height() * (2 / 3)
        else:
            im_size = self.height()
        self.raw_im = QtGui.QPixmap("raw_maze.png")
        self.raw_holder.setPixmap(self.raw_im.scaled(im_size, im_size))

        self.proc_im = QtGui.QPixmap("processed_maze.png")
        self.proc_holder.setPixmap(self.proc_im.scaled(im_size, im_size))


def main():
    prev = os.getcwd()
    # gen_imgs('gray_r')
    app = QtWidgets.QApplication([])

    window = MyApp()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
