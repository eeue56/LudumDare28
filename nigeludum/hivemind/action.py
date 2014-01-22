import logging

class Action(object):
    def __init__(self, name, watch=None, class_watch=None):
        self.name = name

        if watch is None:
            watch = {}

        if class_watch is None:
            class_watch = []

        self.watch = watch
        self.class_watch = class_watch

    def __call__(self, function):
        def func(self_, *args, **kwargs):


            logging.debug("Recording {action} from {player}.".format(action=self.name, player=self_))
            
            for index, name in self.watch.items():
                if len(args) <= index:
                    continue
                logging.debug('{name} is currently {value}'.format(name=name, value=args[index]))

            for name in self.class_watch:
                try:
                    logging.debug("\n\n\n\n\n")
                    logging.debug('{name} is current {value}'.format(name=name, value=self_.__getattribute__(name)))
                    logging.debug("\n\n\n\n\n")
                except AttributeError:
                    pass

            self_.mind.record(self_, self.name)
            return function(self_, *args, **kwargs)
        return func
