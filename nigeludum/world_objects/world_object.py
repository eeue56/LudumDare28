from __future__ import division

import OpenGL.GL as gl

from nigeludum.misc import into_sections, draw_square


class WorldObject(object):

    def __init__(self, x, y, color, facing, scale=1, damagable=True, moveable=True):
        self.x = x
        self.y = y
        self.color = color
        self.scale = scale
        self.damagable = damagable
        self.moveable = moveable
        self.facing = facing

        self._square_cache = {}
        self._section_cache = {}

    def tick(self, world):
        pass

    def draw(self):
        """ draw method used to draw all the populated squares 
            by this object - uses clever caching and sections to improve 
            draw speed """

        if (self.x, self.y, self.facing) not in self._section_cache:
            self._section_cache[(self.x, self.y, self.facing)] = into_sections(self.populated_squares)

        gl.glPushMatrix()

        for section in self._section_cache[(self.x, self.y, self.facing)]:
            (x, y, width, height, color) = section
            r, g, b = color
            gl.glColor3f(r, g, b)
            draw_square(x, y, width, height)
            
        gl.glPopMatrix() 

    def take_damage(self, other):
        pass

    def populated_at(self, x, y):
        """ returns a list of tuples containing the coordinates of populated 
            squares, should the square be at this point
        """
        return [(x, y, self.color)]

    @property
    def populated_squares(self):
        """ returns the populated squares for the current object 
            clever caching method """
        if (self.x, self.y, self.facing) not in self._square_cache:
            self._square_cache[(self.x, self.y, self.facing)] = self.populated_at(self.x, self.y)
        return self._square_cache[(self.x, self.y, self.facing)]

    def closest_point(self, x, y):
        """ returns the coordinates which are part of this object and
            closest to x, y """
        x2nd = x ** 2
        y2nd = y ** 2
        euclid = lambda i, j: (x2nd - (i ** 2)) + (y2nd - (j ** 2))

        small_score = 9000001
        smallest = None

        for (x, y) in self.populated_squares:
            score = euclid(x, y)
            if score < small_score:
                smallest = (x, y)
                small_score = score
        return smallest


