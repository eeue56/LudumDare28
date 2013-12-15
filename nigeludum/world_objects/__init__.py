__all__ = ['player', 'world_object', 'wall', 'bomb', 'old_grumper', 'word']

from nigeludum.world_objects.world_object import *

from nigeludum.world_objects.bomb import *
from nigeludum.world_objects.wall import *

from nigeludum.world_objects.word import *

from nigeludum.world_objects.old_grumper import *
from nigeludum.world_objects.player import *

known_objects = {
    'bomb' : Bomb,
    'wall' : Wall,
    'old_grumper' : OldGrumper,
    'word' : Word
}