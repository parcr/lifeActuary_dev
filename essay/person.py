class Person(object):
    def __init__(self, name, ssn):
        self.name = name
        self._ssn = ssn

    def __setattr__(self, name, value):
        if name == '_ssn':
            raise AttributeError('Denied.')
        else:
            object.__setattr__(self, name, value)