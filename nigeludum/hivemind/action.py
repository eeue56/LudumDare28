import logging

class Action(object):
    def __init__(self, name, arguments_to_watch=None):
        self.name = name

        if arguments_to_watch is None:
            arguments_to_watch = {}

        self.arguments_to_watch = arguments_to_watch

    def __call__(self, function):
        def func(self_, *args, **kwargs):


            logging.debug("Recording {action} from {player}.".format(action=self.name, player=self_))
            
            for index, name in self.arguments_to_watch.items():
                logging.debug('{name} is currently {value}'.format(name=name, value=args[index]))

            self_.mind.record(self_, self.name)
            return function(self_, *args, **kwargs)
        return func
