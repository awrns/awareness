from abc import ABCMeta, abstractproperty, abstractmethod
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import endpoint as i_endpoint
import protocol as i_protocol


class Ability:
    __metaclass__ = ABCMeta

    @abstractproperty
    def container(self): pass

    @abstractproperty
    def inputs(self): pass

    @abstractproperty
    def outputs(self): pass

    @abstractmethod
    def run(self): pass


class LocalAbility(Ability):

    container = None
    index = 0

    inputs = 0
    outputs = 0

    def __init__(self, container, index, inputs, outputs):
        self.container = container
        self.index = index
        self.inputs = inputs
        self.outputs = outputs


class RemoteAbility(Ability):

    container = None
    index = 0

    inputs = 0
    outputs = 0

    def __init__(self, container, index, inputs, outputs):
        self.container = container
        self.index = index
        self.inputs = inputs
        self.outputs = outputs

    def run(self, input):
        connection = self.container.backend.connect(self.container.address)
        output = self.container.protocol.processData(connection, self.index, input)
        return output

