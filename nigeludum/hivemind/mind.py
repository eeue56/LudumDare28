
class Mind(object):

    def __init__(self):
        self.action_paths = None
        self._actions = []

    def register_action(self, action):
        self._actions.append(action)