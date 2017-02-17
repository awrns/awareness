from abc import ABCMeta, abstractproperty, abstractmethod
import multiprocessing
import socket
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
    def connect(self, host, port):
        raise NotImplementedError()

    @abstractmethod
    def listen(self, host='', port=1024, use_ipv6=False, backlog=5):
        raise NotImplementedError()


class NativeBackend(Backend):

    def async(self, function, args, callback):

        pool = multiprocessing.Pool(processes=1)
        pool.apply_async(function, [args], callback)

    def connect(self, host, port=1024):
        return socket.create_connection((host, port))

    def listen(self, host='', port=1024, use_ipv6=False, backlog=5):
        type = socket.AF_INET6 if use_ipv6 else socket.AF_INET

        listener = socket.socket(type, socket.SOCK_STREAM)
        listener.bind((host, port))
        listener.listen(backlog)

        return listener
