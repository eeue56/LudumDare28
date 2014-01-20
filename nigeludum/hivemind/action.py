import logging

class Action(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, function):
        def func(self_, *args, **kwargs):
            logging.debug("Recording {action} from {player}.".format(action=self.name, player=self_))
            logging.debug("|".join(str(arg) for arg in args))
            self_.mind.record(self_, self.name)
            return function(self_, *args, **kwargs)
        return func
