from __future__ import division

## TODO: refactor with __init__.py
from nigeludum.world_objects.world_object import WorldObject

class Player(WorldObject):
    def __init__(self, x, y, color, facing, scale=1):
        WorldObject.__init__(self, x, y, color, facing, scale)

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
        populate = lambda x, y: populated.append((x, y))

        scaled_x = 5 * self.scale
        scaled_y = 4 * self.scale

        ## TODO: fix y scaling

        # bottom and top lines
        for i in xrange(x + 1, x + scaled_x - 1):
            populate(i, y)
            populate(i, y + scaled_y - 1)

        # connector

        middle_x = x + int(scaled_x / 2)
        populate(middle_x, 1)

        # arms

        for i in xrange(x, x + scaled_x):
            populate(i, 2)

        return populated