from abc import ABCMeta

class Ability:
    __metaclass__ = ABCMeta

class LocalAbility(Ability): pass

class RemoteAbility(Ability): pass