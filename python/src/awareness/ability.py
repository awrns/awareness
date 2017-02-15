from abc import ABCMeta, abstractproperty, abstractmethod
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import endpoint as i_endpoint
import protocol as i_protocol


class Ability:
    __metaclass__ = ABCMeta

    @abstractproperty
    def endpoint(self):
        raise NotImplementedError()

    @abstractproperty
    def inputs(self):
        raise NotImplementedError()

    @abstractproperty
    def outputs(self):
        raise NotImplementedError()

    @abstractmethod
    def run(self, input):
        raise NotImplementedError()


class LocalAbility(Ability):

    endpoint = None
    index = 0

    inputs = 0
    outputs = 0

    def __init__(self, endpoint, index, inputs, outputs):
        self.endpoint = endpoint
        self.index = index
        self.inputs = inputs
        self.outputs = outputs


class RemoteAbility(Ability):

    endpoint = None
    index = 0

    inputs = 0
    outputs = 0

    def __init__(self, endpoint, index, inputs, outputs):
        self.endpoint = endpoint
        self.index = index
        self.inputs = inputs
        self.outputs = outputs

    def run(self, input):
        connection = self.endpoint.connection if self.endpoint.connection else self.endpoint.backend.connect(self.endpoint.address)

        output = self.endpoint.protocol.processData(connection, self.index, input)

        if not self.endpoint.connection: connection.close()
        return output

