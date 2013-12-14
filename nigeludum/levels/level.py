from nigeludum.world_exceptions import *


class Level(object):

    def __init__(self, color, walls, width, height, objects=None):
        self.color = color
        self.walls = walls
        self.width = width
        self.height = height

        if objects is None:
            objects = []

        self.objects = []

        self.object_array = [[None for x in xrange(width)] for y in xrange(height)]

        self.add_objects(objects)

    def add_object(self, object_):
        for (x, y, _) in object_.populated_squares:
            try:
                self.object_array[y][x] = object_
            except IndexError:
                raise OutOfWorldException
        self.objects.append(object_)

    def add_objects(self, objects):
        for object_ in objects:
            self.add_object(object_)

