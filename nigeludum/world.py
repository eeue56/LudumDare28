from __future__ import division

from collections import defaultdict
from copy import deepcopy as copy

from nigeludum.world_exceptions import *
from nigeludum.misc import *

class World(object):

    def __init__(self, player, height=100, width=100):
        self.player = player
        self.height = height
        self.width = width

        self.objects = []
        self.object_array = [[None for x in xrange(width)] for y in xrange(height)]

    def add_object(self, object_):
        for (x, y) in object_.populated_squares:
            try:
                self.object_array[y][x] = object_
            except IndexError:
                raise OutOfWorldException
        self.objects.append(object_)

    def add_objects(self, objects):
        for object_ in objects:
            self.add_object(object_)

    def draw(self):
        for object_ in self.objects:
            object_.draw()

        self.player.draw()

    def tick(self):
        for object_ in self.objects:
            object_.tick(self)

        self.player.tick(self)
