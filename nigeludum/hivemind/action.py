
class Action(object):
    def __init__(self, name, mind):
        self.name = name
        self.mind = mind

    def __call__(self, function):
        def func(*args, **kwargs):
            return function(*args, **kwargs)
        return func
