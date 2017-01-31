from abc import ABCMeta, abstractproperty, abstractmethod
import ability as i_ability
import algorithm as i_algorithm
import data as i_data
import endpoint as i_endpoint
import protocol as i_protocol


class Backend:

    @abstractmethod
    def async(self):
        pass

    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def receive(self):
        pass


class NativeBackend(Backend):

    pass