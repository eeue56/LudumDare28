from __future__ import division

from nigeludum.world_objects import WorldObject
from nigeludum.misc import *
from nigeludum.world_exceptions import *

class Bomb(WorldObject):
    def __init__(self, x, y, 
        color=COLOURS['grey'], 
        facing=DIRECTIONS['up'], 
        health=3, 
        scale=1,
        max_scale=3):

        WorldObject.__init__(self, x, y, color, facing, health=3, scale=scale)
        self.center_color = COLOURS['red']
        self.max_scale = max_scale

    def populated_at(self, x, y):
        """ returns a list of tuples containing the coordinates of populated 
            squares, should the square be at this point
        """

        #  ###   2
        #  #n#   1
        #->###   0
        #
        #  012
        self.scale = 2
        populated = []
        populate = lambda i, j, color: populated.append((i + x, j + y, color))

        scaled_x = int(3 * self.scale)
        scaled_y = int(3 * self.scale)


        for i in xrange(1, scaled_x - 1):
            for j in xrange(1, scaled_y - 1):
                populate(i, j, self.center_color)

        for i in xrange(scaled_x):
            populate(i, 0, self.color)
            populate(i, scaled_y - 1, self.color)

        
        for j in xrange(scaled_y):
            populate(0, j, (0, 1, 0))
            populate(scaled_x - 1, j, self.color)
        

        return populated

    def tick(self, world):
        if self.scale < self.max_scale:
            self.scale += 0.1
        else:
            self.health -= 0.25

            if self.health < 1:
                self.scale += 1

        try:
            world.move_in_direction(self, self.facing)
        except CollisionException as e:
            while True:
                self.scale -= 0.2
                try:
                    self.facing = opposite_direction(e.other.facing)
                    world.move_in_direction(self, self.facing)
                    break
                except CollisionException:
                    pass

           
    