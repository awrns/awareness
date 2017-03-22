from abc import ABCMeta, abstractproperty, abstractmethod
import misc
import affinity as i_affinity
import algorithm as i_algorithm
import backend as i_backend
import operator as i_operator
import protocol as i_protocol


class Item:

    input = None
    output = None
    
    def __init__(self, datums):
        raise NotImplementedError()


    def datumize(self):
        raise NotImplementedError()

    def similarity(self, other):
        raise NotImplementedError()



class Set:

    items = []


    def __init__(self, datums):
        raise NotImplementedError()


    def datumize(self):
        raise NotImplementedError()


    def similarity(self, other):
        pass



class Assembly:
    

    def run(self, inputSetself, inputSet, progressFrequency=0, progressCallback=None):
        raise NotImplementedError()