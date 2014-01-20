
class Mind(object):

    def __init__(self):
        self.action_paths = None
        self._actions = []

    def register_action(self, action):
        self._actions.append(action)


class RecordingMind(Mind):

    def __init__(self, *args, **kwargs):
        Mind.__init__(self, *args, **kwargs)
        self.recording = []

    def record(self, action):
        self.recording.append(action)

