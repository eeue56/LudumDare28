from __future__ import division

from nigeludum.world_objects import WorldObject
from nigeludum.misc import *

class Bomb(WorldObject):
    def __init__(self, x, y, color=COLOURS['grey'], facing=DIRECTIONS['up'], health=3, scale=1):
        WorldObject.__init__(self, x, y, color, facing, health=3, scale=scale)
        self.center_color = COLOURS['red']

    def populated_at(self, x, y):
        """ returns a list of tuples containing the coordinates of populated 
            squares, should the square be at this point
        """

        #  ###   2
        #  #n#   1
        #->###   0
        #
        #  012
        populated = []
        populate = lambda i, j, color: populated.append((i + x, j + y, color))

        scaled_x = 3 * self.scale
        scaled_y = 3 * self.scale


        for i in xrange(1, scaled_x - 1):
            for j in xrange(1, scaled_y - 1):
                populate(i, j, self.center_color)

        for i in xrange(scaled_x):
            populate(i, 0, self.color)
            populate(i, scaled_y - 1, self.color)

        
        for j in xrange(scaled_y):
            populate(0, j, self.color)
            populate(scaled_x - 1, j, self.color)
        

        return populated

    def tick(self, world):
        pass
           
    