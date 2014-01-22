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
            messages = []

            messages.append("Recording {action} from {player}.".format(action=self.name, player=self_))
            
            for index, name in self.watch.items():
                if name in kwargs:
                    value = kwargs[name]
                elif index < len(args):
                    value = args[index]
                else:
                    continue

                messages.append('{name} is currently {value}'.format(name=name, value=value))

            for name in self.class_watch:
                try:
                    messages.append('{name} is current {value}'.format(name=name, value=self_.__getattribute__(name)))
                except AttributeError:
                    logging.error("No such property as {name}".format(name=name))

            logging.debug('\n'.join(messages))
            self_.mind.record(self_, self.name)
            return function(self_, *args, **kwargs)
        return func
