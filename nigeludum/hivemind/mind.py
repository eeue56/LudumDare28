import logging

class Mind(object):

    def __init__(self):
        self.action_paths = None
        self._actions = {}

    def register_action(self, action, type):
        if type not in self._actions:
            self._actions[type] = []
        logging.error("Storing {action} as {type}".format(action=action, type=type))
        self._actions[type].append(action)

    def next_move(self, behavior):
        if behavior in self._actions:
            return self._actions[behavior][0]
        return lambda *a, **kw: None 


class RecordingMind(Mind):

    def __init__(self, *args, **kwargs):
        Mind.__init__(self, *args, **kwargs)
        self.recording = []

    def record(self, player, action):
        self.recording.append((player, action))

    def dump(self, class_name):
        with open('data.dat', 'a') as f:
            f.write('{name}\n'.format(name=class_name))

            for (player, action) in self.recording:
                f.write("----------\n")
                f.write(repr(player) + '\n')

                # fast, simple, and hacky.
                # TODO: unhackify
                for key, value in player.__dict__.iteritems():
                    if key[0] == '_':
                        continue
                    f.write('{key},{value}\n'.format(key=key, value=value))
                f.write(repr(action) + '\n')
                f.write("----------\n")
