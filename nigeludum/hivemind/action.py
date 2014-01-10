
class Action(object):
    def __init__(self, action):
        self._action = action

    def run(self, *args, **kwargs):
        self._action(*args, **kwargs)