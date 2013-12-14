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

    def _move(self, old, new, object_):
        for (x, y, _) in old:
            self.object_array[y][x] = None
        for (new_x, new_y, _) in new:
            self.object_array[new_y][new_x] = object_

    def _move_object(self, object_, x=0, y=0):
        self._move(object_.populated_squares, 
            object_.populated_at(object_.x + x, object_.y + y), 
            object_)
        object_.x += x
        object_.y += y

    def colliding_object(self, old_object, populated_next):
        for (x, y, _) in populated_next:
            if y < 0 or y >= self.height or x < 0 or x >= self.width:
                raise OutOfWorldException

            if self.object_array[y][x] is not None and self.object_array[y][x] != old_object:
                return self.object_array[y][x]
        return None

    def object_going_to_collide(self, object_, x=0, y=0):
        projected_points = object_.populated_at(object_.x + x, object_.y + y)
        return self.colliding_object(object_, projected_points)

    def move_in_direction(self, object_, direction, distance=1):
        if distance <= 0 or direction == DIRECTIONS['still']:
            return

        print 'moving!'

        x, y = MOVEMENTS[direction]
            
        for _ in xrange(distance):
            print 'here'
            obj_ = self.object_going_to_collide(object_, x=x, y=y)
            if obj_ is not None:
                raise CollisionException(obj_)
            self._move_object(object_, x=x, y=y)


    def draw(self):
        for object_ in self.objects:
            object_.draw()

        self.player.draw()

    def tick(self):
        for object_ in self.objects:
            object_.tick(self)

        self.player.tick(self)

