import misc
import affinity as i_affinity
import algorithm as i_algorithm
import backend as i_backend
import operator as i_operator
import protocol as i_protocol


class ItemApplication():
    INPUT = True
    OUTPUT = False


class Item:

    affinity = None
    application = None
    parameters = None

    def __init__(self, affinity, application, parameters):
        self.affinity = affinity
        self.application = application
        self.parameters = parameters

    def toDatums(self):
        return list(self.parameters)


    @classmethod
    def fromAffinityApplicationDatums(self, affinity, application, datums):
        return Item(affinity, application, tuple(datums))



class Set:

    inputItem = None
    outputItem = None

    def __init__(self, inputItem, outputItem):
        self.inputItem = inputItem
        self.outputItem = outputItem


    def toDatums(self):
        return self.inputItem.toDatums() + self.outputItem.toDatums()  # concat


    @classmethod
    def fromAffinityDatums(self, affinity, datums):

        inputs = datums[:affinity.inputs]
        outputs = datums[affinity.inputs:affinity.outputs]

        inputItem = Item.fromAffinityApplicationDatums(affinity, ItemApplication.INPUT, datums)
        outputItem = Item.fromAffinityApplicationDatums(affinity, ItemApplication.OUTPUT, datums)


        return Set(affinity, inputItem, outputItem)


class Assembly:
    

    def run(self, inputSet, progressFrequency=0, progressCallback=None):
        pass