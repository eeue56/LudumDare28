
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

    def record(self, player, action):
        self.recording.append((player, action))

    def dump(self, class_name):
        with open('data.dat', 'a') as f:
            f.write('{name}\n'.format(name=class_name))

            for recording in self.recording:
                f.write(
                    '{data}\n'.format(
                        data=','.join(map(repr, recording))
                    )
                )
