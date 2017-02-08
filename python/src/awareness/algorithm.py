from abc import ABCMeta, abstractproperty, abstractmethod
import ability as i_ability
import backend as i_backend
import data as i_data
import endpoint as i_endpoint
import protocol as i_protocol


class Algorithm:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def run(self):
        pass


