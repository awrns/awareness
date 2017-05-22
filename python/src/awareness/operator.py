#
# This file is part of the Awareness Operator Python implementation.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from abc import ABCMeta, abstractproperty, abstractmethod
import logging
import exception
import misc
import component as i_component
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import protocol as i_protocol


class Operator:
    __metaclass__ = ABCMeta

    def gethost(self): raise NotImplementedError()
    def sethost(self, value): raise NotImplementedError()
    host = abstractproperty(gethost, sethost)

    def getport(self): raise NotImplementedError()
    def setport(self, value): raise NotImplementedError()
    port = abstractproperty(getport, setport)

    def getcomponents(self): raise NotImplementedError()
    def setcomponents(self, value): raise NotImplementedError()
    components = abstractproperty(getcomponents, setcomponents)

    def getbackend(self): raise NotImplementedError()
    def setbackend(self, value): raise NotImplementedError()
    backend = abstractproperty(getbackend, setbackend)

    def setprotocol(self): raise NotImplementedError()
    def getprotocol(self, value): raise NotImplementedError()
    protocol = abstractproperty(getprotocol, setprotocol)


    @abstractmethod
    def capabilities(self):
        raise NotImplementedError()

    @abstractmethod
    def search(self, recursion_limit, input_set, progress_frequency=0, progress_callback=None):
        raise NotImplementedError()

    @abstractmethod
    def process(self, index, input_stream, progress_frequency=0, progress_callback=None):
        raise NotImplementedError()



class LocalOperator(Operator):

    host = ""
    public_host = ""
    port = -1
    components = []
    backend = None
    protocol = None

    algorithm = None

    remote_operators = []  # List of RemoteOperator.


    def __init__(self,
                 public_host,
                 host="",
                 port=1600,
                 components = [],
                 backend = None,
                 protocol = None,
                 algorithm = None,
                 assemblies = [],
                 remote_operators = []):

        self.public_host = public_host
        self.host = host
        self.port = port
        self.components = components
        self.backend = backend() if backend else i_backend.NativeBackend()  # If not passed in, use default
        self.protocol = protocol() if protocol else i_protocol.Protocol0()
        self.algorithm = algorithm() if algorithm else i_algorithm.DefaultAlgorithm()
        self.assemblies = assemblies
        self.remote_operators = remote_operators

        # self.backend.setupLogger()

        # Kickoff the server. Get a listener from self.backend, and give it to self.protocol to use.
        self.provider = self.backend.threading_async(self.protocol.provide, args=(self.backend.listen(host=host,port=port), self), name='Provide-' + str(port))


    def search(self, recursion_limit, input_set, progress_frequency=0, progress_callback=None):

        # Search both the components here and the RemoteAbilities that the RemoteOperators make available.
        return self.algorithm.search(self, self.remote_operators, recursion_limit, input_set, progress_frequency=progress_frequency, progress_callback=progress_callback)


    def process(self, index, input_stream, progress_frequency=0, progress_callback=None):

        # Hand inputSet to our indexed LocalComponent.
        return self.components[index].run(input_stream, progress_frequency=progress_frequency, progress_callback=progress_callback)


    def capabilities(self):

        # Building a list of tuples.
        capabilities = []

        for each_component in self.components:
            capabilities.append((each_component.inputs, each_component.outputs))  # in 2-tuple

        return capabilities



class RemoteOperator(Operator):

    host = ""
    port = -1
    components = []
    backend = None
    protocol = None

    connection = None

    def __init__(self,
                 host,
                 port = 1600,
                 components = [],
                 backend = None,
                 protocol = None):

        self.host = host
        self.port = port
        self.components = components
        self.backend = backend() if backend else i_backend.NativeBackend()  # Set to default if None.
        self.protocol = protocol() if protocol else i_protocol.Protocol0()


        # Do a quick routine to get the Component details.
        #if len(self.components) == 0:
        #    with self:
        #        self.retrieve_components()


    def __enter__(self):
        self.connection = self.backend.connect(self.host, port=self.port)
        return self


    def __exit__(self, type, value, traceback):
        self.connection.close()
        self.connection = None


    def retrieve_components(self):
        capabilities = self.protocol.capabilities(self.connection)
        for i in range(len(capabilities)):
            component_profile = capabilities[i]
            new_component = i_component.RemoteComponent(self, i, *component_profile)  # unpack inputs and outputs from 2-tuple

            self.components.append(new_component)


    def search(self, recursion_limit, input_set, progress_frequency=0, progress_callback=None):

        return self.protocol.search(self.connection, recursion_limit, input_set, progress_frequency=progress_frequency, progress_callback=progress_callback)


    def process(self, index, input_stream, progress_frequency=0, progress_callback=None):

        return self.components[index].run(self.connection, input_stream, progress_frequency=progress_frequency, progress_callback=progress_callback)


    def capabilities(self):

        capabilities = []

        for each_component in self.components:
            capabilities.append((each_component.inputs, each_component.outputs))  # in 2-tuple

        return capabilities
