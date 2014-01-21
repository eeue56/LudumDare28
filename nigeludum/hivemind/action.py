import logging

class Action(object):
    def __init__(self, name, watch=None):
        self.name = name

        if watch is None:
            watch = {}

        self.watch = watch

    def __call__(self, function):
        def func(self_, *args, **kwargs):


            logging.debug("Recording {action} from {player}.".format(action=self.name, player=self_))
            
            for index, name in self.watch.items():
                if len(args) <= index:
                    continue
                logging.debug('{name} is currently {value}'.format(name=name, value=args[index]))

            self_.mind.record(self_, self.name)
            return function(self_, *args, **kwargs)
        return func
