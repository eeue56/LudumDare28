from json import dumps, loads

from nigeludum.levels import Level
from nigeludum.misc import *
from nigeludum.world_objects import Wall

def generate_objects(file_data, world_width, world_height):

    data = loads(file_data)

    level_dict = {}

    for level_id, level_data in data.iteritems():

        wall_dict = {}
        walls = []
        for wall, wall_data in level_data['walls'].iteritems():
            direction = DIRECTIONS[wall]
            gaps = range(wall_data['gaps']['start'], wall_data['gaps']['end'])
            width = wall_data['width']
            wall_dict[direction] = wall_data['leads_to']

            walls.append(Wall(world_width, world_height, width=width, facing=direction, gaps=gaps))

        color = level_data['color']
        r = color['r']
        g = color['g']
        b = color['b']

        level = Level((r, g, b), wall_dict, world_width, world_height)
        level.add_objects(walls)

        level_dict[int(level_id)] = level

    return level_dict





