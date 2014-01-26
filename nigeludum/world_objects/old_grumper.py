from __future__ import division

from nigeludum.world_objects import WorldObject, Bomb
from nigeludum.misc import *
from nigeludum.world_exceptions import *

class OldGrumper(WorldObject):
    def __init__(self, 
        x, 
        y, 
        color, 
        facing, 
        health=3, 
        scale=1,
        speed=1,
        *args,
        **kwargs):
        WorldObject.__init__(self, x, y, color, facing, health=3, scale=scale, *args, **kwargs)

    def populated_at(self, x, y):
        """ returns a list of tuples containing the coordinates of populated 
            squares, should the square be at this point
        """

        #   #
        #  ###
        #   #
        #-># #
        #  01234
        populated = []
        populate = lambda i, j, color: populated.append((x + i, y + j, color))

        scaled_x = 5 * self.scale
        scaled_y = 4 * self.scale

        middle_x = int(scaled_x / 2)
        middle_y = int(scaled_y / 2)

        ## TODO: fix y scaling

        # bottom and top lines
        for i in xrange(scaled_x):
            populate(i, 0, self.color)

            populate(i, scaled_y - 2, (0.5, 1, 0))

        # connector

        populate(middle_x, 1, (1, 0, 0))
        populate(middle_x, scaled_y - 1, (1, 0, 0))
        

        return populated

    def take_damage(self, damage, other):
        if other is self:
            return
        WorldObject.take_damage(self, damage, other)

    def deal_damage(self, other):
        other.take_damage(0.1, self)

    def tick(self, world):
        try:
            self.facing = world.direction_to_object(self, world.player)
            self.move(world, self.facing, 1)
        except CollisionException as e:
            e.other.take_damage(0.2, self)
        except OutOfWorldException:
            pass

           
    