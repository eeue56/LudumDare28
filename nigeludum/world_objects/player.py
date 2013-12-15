from __future__ import division

from nigeludum.world_objects import WorldObject, Bomb
from nigeludum.misc import *
from nigeludum.world_exceptions import *

class Player(WorldObject):
    def __init__(self, x, y, color, facing, health=3, scale=1, speed=1):
        WorldObject.__init__(self, x, y, color, facing, health=3, scale=scale)
        self.speed = speed

    def populated_at(self, x, y):
        """ returns a list of tuples containing the coordinates of populated 
            squares, should the square be at this point
        """

        #   ###
        #  #####
        #    #
        #-> ###
        #  01234
        populated = []
        populate = lambda x, y, color: populated.append((x, y, color))

        scaled_x = 5 * self.scale
        scaled_y = 4 * self.scale

        ## TODO: fix y scaling

        # bottom and top lines
        for i in xrange(x + 1, x + scaled_x - 1):
            populate(i, y, self.color)
            populate(i, y + scaled_y - 1, self.color)

        # connector

        middle_x = x + int(scaled_x / 2)
        populate(middle_x, y + 1, (1, 0, 0))

        # arms

        for i in xrange(x, x + scaled_x):
            populate(i, y + 2, self.color)

        return populated

    def place_bomb(self, world):
        i, j = MOVEMENTS[self.facing]
        i *= 5
        j *= 5
        world.add_object(Bomb(self.x + i, self.y + j, facing=self.facing))

    def tick(self, world):
        try:
            world.move_in_direction(self, self.facing, self.speed)
        except CollisionException as e:
            e.other.take_damage(0.05, self)
        except OutOfWorldException:
            raise

    def take_damage(self, damage, other):
        if isinstance(other, Bomb):
            pass
        else:
            self.health -= damage

           
    