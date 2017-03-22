from abc import ABCMeta, abstractproperty, abstractmethod
import misc
import affinity as i_affinity
import algorithm as i_algorithm
import backend as i_backend
import operator as i_operator
import protocol as i_protocol


class Set:

    affinity = None

    input = None
    output = None

    def __init__(self, affinity, input, output):
        self.affinity = affinity
        self.input = input
        self.output = output


    def toDatums(self):
        return self.input + self.output  # concat


    @classmethod
    def fromAffinityDatums(self, affinity, datums):
        inputs = datums[:affinity.inputs]
        outputs = datums[affinity.inputs:affinity.outputs]
        return Set(affinity, inputs, outputs)


class Assembly:
    

    def run(self, inputSet, progressFrequency=0, progressCallback=None):
        pass