from abc import ABCMeta, abstractproperty, abstractmethod
import multiprocessing
import threading
import socket
import misc
import affinity as i_affinity
import algorithm as i_algorithm
import data as i_data
import operator as i_operator
import protocol as i_protocol


class Backend:
    __metaclass__ = ABCMeta

    @abstractmethod
    def threadingAsync(self, function, args=(), kwargs={}, callback=None):
        raise NotImplementedError()

    @abstractmethod
    def connect(self, host, port=1600):
        raise NotImplementedError()

    @abstractmethod
    def listen(self, host='', port=1600, use_ipv6=False, backlog=5):
        raise NotImplementedError()



class NativeBackend(Backend):


    def threadingAsync(self, function, args=(), kwargs={}, callback=None):
        if not callback: callback = lambda *args,**kwargs:None

        def wrapWithCallback(): callback(function)

        thread = threading.Thread(target=wrapWithCallback(), args=args, kwargs=kwargs)
        thread.start()


    def connect(self, host, port=1600):
        return socket.create_connection((host, port))


    def listen(self, host='', port=1600, use_ipv6=False, backlog=5):
        type = socket.AF_INET6 if use_ipv6 else socket.AF_INET

        listener = socket.socket(type, socket.SOCK_STREAM)
        listener.bind((host, port))
        listener.listen(backlog)

        return listener
