import pickle
import math
from enum import IntEnum
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from numpy import uint8


class Side(IntEnum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3


def main():
    picklefile = open('./rustmaz/data.txt', 'rb')
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

    plt.imshow(new_arr, interpolation='nearest', cmap='twilight_shifted', vmin=0, vmax=15)
    plt.axis('off')
    plt.savefig('raw_maze.png', bbox_inches='tight', pad_inches=0)

    plt.imshow(big_arr, interpolation='nearest', cmap='twilight_shifted', vmin=0, vmax=32)
    plt.axis('off')
    plt.savefig('processed_maze.png', bbox_inches='tight', pad_inches=0)

    for row in new_arr:
        print(row)


if __name__ == '__main__':
    main()
