from abc import ABCMeta, abstractproperty, abstractmethod
import multiprocessing
import ability as i_ability
import algorithm as i_algorithm
import data as i_data
import endpoint as i_endpoint
import protocol as i_protocol


class Backend:
    __metaclass__ = ABCMeta

    @abstractmethod
    def async(self, function, args, callback):
        raise NotImplementedError()

    @abstractmethod
    def connect(self, address):
        raise NotImplementedError()

    @abstractmethod
    def listen(self, address, port):
        raise NotImplementedError()


class NativeBackend(Backend):

    def async(self, function, args, callback):
        pool = multiprocessing.Pool(processes=1)
        pool.apply_async(function, args, callback)
