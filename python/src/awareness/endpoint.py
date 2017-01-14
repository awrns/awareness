from ABC import ABCMeta

class Endpoint:
    __metaclass__ = ABCMeta

class LocalEndpoint(Endpoint): pass

class RemoteEndpoint(Endpoint): pass