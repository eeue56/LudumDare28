from __future__ import division

from collections import defaultdict
from copy import deepcopy as copy

from nigeludum.world_exceptions import *
from nigeludum.misc import *

class World(object):

    def __init__(self, player, level_controller):
        self.player = player

        self.level_controller = level_controller
        self.level_controller.start()

    def add_object(self, *args, **kwargs):
        self.level_controller.current_level.add_object(*args, **kwargs)

    @property
    def floor_color(self):
        return self.level_controller.current_level.color

    @property
    def height(self):
        return self.level_controller.current_level.height

    @property
    def width(self):
        return self.level_controller.current_level.width

    @property
    def object_array(self):
        return self.level_controller.current_level.object_array

    @property
    def objects(self):
        return self.level_controller.current_level.objects

    def remove(self, object_):
        for (x, y, _) in object_.populated_squares:
            self.object_array[y][x] = None
        self.objects.remove(object_)

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
        x, y = MOVEMENTS[direction]
            
        for _ in xrange(distance):
            obj_ = self.object_going_to_collide(object_, x=x, y=y)
            if obj_ is not None:
                raise CollisionException(obj_)
            self._move_object(object_, x=x, y=y)

    def next_level(self):
        self.level_controller.next_level(self.player.facing)

    def clean_up(self):
        copy = [[None for x in xrange(self.width)] for y in xrange(self.height)]

        for object_ in self.objects:
            for (x, y, _) in object_.populated_squares:
                copy[y][x] = object_

        self.level_controller.current_level.object_array = copy

    def draw(self):
        for object_ in self.objects:
            object_.draw()

        self.player.draw()

    def tick(self):
        for object_ in self.objects:
            object_.tick(self)
            

        try:
            self.player.tick(self)
        except OutOfWorldException:
            print 'here, moving to next level!'
            x, y = MOVEMENTS[opposite_direction(self.player.facing)]
            self.player.x += 5 * x
            self.player.y += 5 * y
            self.next_level()
            self.clean_up()

        for object_ in self.objects:
            if object_.health <= 0:
                self.remove(object_)

        if self.player.health <= 0:
            print 'player dead!'

