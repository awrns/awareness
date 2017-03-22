from abc import ABCMeta, abstractproperty, abstractmethod
import misc
import affinity as i_affinity
import algorithm as i_algorithm
import backend as i_backend
import operator as i_operator
import protocol as i_protocol


class Item:

    parameters = ()
    
    def __init__(self, parameters):
        self.parameters = parameters


    @classmethod
    def fromDatums(self, datums):
        pass


    def toDatums(self):
        pass

    def similarity(self, other):
        pass



class Set:

    inputItems = []
    outputItems = []

    def __init__(self, inputItems, outputItems):
        self.inputItems = inputItems
        self. outputItems = outputItems


    @classmethod
    def fromDatums(self, datums):
        pass


    def toDatums(self):
        pass


    def similarity(self, other):
        pass



class Assembly:
    

    def run(self, inputSet, progressFrequency=0, progressCallback=None):
        pass