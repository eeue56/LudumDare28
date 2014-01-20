
class Action(object):
    def __init__(self, name, action):
        self.name = name
        self._action = action

    def run(self, *args, **kwargs):
        self._action(*args, **kwargs)