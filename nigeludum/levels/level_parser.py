from json import dumps, loads

from nigeludum.levels import Level
from nigeludum.misc import *
from nigeludum.world_objects import Wall, known_objects

def _color_dict_to_tuple(color):
    return color.values()

def generate_objects(file_data):

    data = loads(file_data)

    level_dict = {}

    for level_id, level_data in data.iteritems():
        world_width = level_data['width']
        world_height = level_data['height']

        wall_dict = {}
        walls = []
        for wall, wall_data in level_data['walls'].iteritems():
            direction = DIRECTIONS[wall]
            gaps = range(wall_data['gaps']['start'], wall_data['gaps']['end'])
            width = wall_data['width']
            wall_dict[direction] = wall_data['leads_to']

            walls.append(Wall(world_width, world_height, width=width, facing=direction, gaps=gaps))

        color = _color_dict_to_tuple(level_data['color'])

        level = Level(color, wall_dict, world_width, world_height)
        level.add_objects(walls)

        level_dict[int(level_id)] = level

        for object_, object_data in level_data['fixed'].iteritems():
            if object_ in known_objects:
                if 'color' in object_data:
                    object_data['color'] = _color_dict_to_tuple(object_data['color'])
                level.add_object(known_objects[object_](**object_data))

    return level_dict





