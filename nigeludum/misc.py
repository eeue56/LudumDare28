from __future__ import division

import OpenGL.GL as gl

from random import randint

COLOURS = { 
    'black' : (0, 0, 0),
    'other-grey' : (0.25, 0.25, 0.25),
    'grey' : (0.4, 0.4, 0.4),
    'red' :  (255, 0, 0),
    'white' : (1, 1, 1)
}

DIRECTIONS = {
    'still' : 0,
    'up' : 1,
    'down' : -1,
    'right' : 20,
    'left' : -20,
    'up-left' : -19,
    'up-right' : 21,
    'down-left' : -21,
    'down-right' : 19
}

MOVEMENTS = {
    DIRECTIONS['still'] : (0, 0),
    DIRECTIONS['up'] : (0, 1),
    DIRECTIONS['down'] : (0, -1),
    DIRECTIONS['left'] : (-1, 0),
    DIRECTIONS['right'] : (1, 0),
    DIRECTIONS['up'] + DIRECTIONS['left'] : (-1, 1),
    DIRECTIONS['up'] + DIRECTIONS['right'] : (1, 1),
    DIRECTIONS['down'] + DIRECTIONS['left'] : (-1, -1),
    DIRECTIONS['down'] + DIRECTIONS['right'] : (1, -1)
}

def random_color():
    return tuple(y / 255 for y in (randint(0, 255), randint(0, 255), randint(0, 255)))

def draw_square(x, y, x_size=1, y_size=1):
    gl.glRectf(x, y, x + x_size, y + y_size)