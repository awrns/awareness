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
import affinity as i_affinity
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import protocol as i_protocol


class Operator:
    __metaclass__ = ABCMeta

    @abstractproperty
    def host(self):
        raise NotImplementedError()

    @abstractproperty
    def port(self):
        raise NotImplementedError()

    @abstractproperty
    def affinities(self):  # List of LocalAffinity.
        raise NotImplementedError()

    @abstractproperty
    def backend(self):  # Any derivation from i_backend.Backend.
        raise NotImplementedError()

    @abstractproperty
    def protocol(self):  # Any derivation from i_protocol.Protocol.
        raise NotImplementedError()


    @abstractmethod
    def capabilities(self):
        raise NotImplementedError()

    @abstractmethod
    def search(self, propagation_limit, input_set, progress_frequency=0, progress_callback=None):
        raise NotImplementedError()

    @abstractmethod
    def process(self, index, input_stream, progress_frequency=0, progress_callback=None):
        raise NotImplementedError()



class LocalOperator(Operator):

    host = ""
    port = -1
    affinities = []
    backend = None
    protocol = None

    algorithm = None
    assemblies = []  # List of i_assembly.Assembly.
    remote_operators = []  # List of RemoteOperator.


    def __init__(self,
                 host="",
                 port=1600,
                 affinities = [],
                 backend = None,
                 protocol = None,
                 algorithm = None,
                 assemblies = [],
                 remote_operators = []):

        self.host = host
        self.port = port
        self.affinities = affinities
        self.backend = backend() if backend else i_backend.NativeBackend()  # If not passed in, use default
        self.protocol = protocol() if protocol else i_protocol.Protocol0()
        self.algorithm = algorithm() if algorithm else i_algorithm.DefaultAlgorithm()
        self.assemblies = assemblies
        self.remote_operators = remote_operators

        # self.backend.setupLogger()

        # Kickoff the server. Get a listener from self.backend, and give it to self.protocol to use.
        self.backend.threading_async(self.protocol.provide, args=(self.backend.listen(host=host,port=port), self), name='Provide-' + str(port))


    def search(self, propagation_limit, input_set, progress_frequency=0, progress_callback=None):

        # Search both the LocalAffinities here and the RemoteAbilities that the RemoteOperators make available.
        return self.algorithm.search(self.abilities, self.remote_operators, input_set, progress_frequency=progress_frequency, progress_callback=progress_callback)


    def process(self, index, input_stream, progress_frequency=0, progress_callback=None):

        # Hand inputSet to our indexed LocalAffinity.
        return self.affinities[index].run(input_stream, progress_frequency=progress_frequency, progress_callback=progress_callback)


    def capabilities(self):

        # Building a list of tuples.
        capabilities = []

        for each_affinity in self.affinities:
            capabilities.append(each_affinity.profile)

        return capabilities



class RemoteOperator(Operator):

    host = ""
    port = -1
    affinities = []
    backend = None
    protocol = None

    connection = None

    def __init__(self,
                 host,
                 port = 1600,
                 affinities = [],
                 backend = None,
                 protocol = None):

        self.host = host
        self.port = port
        self.affinities = affinities
        self.backend = backend() if backend else i_backend.NativeBackend()  # Set to default if None.
        self.protocol = protocol() if protocol else i_protocol.Protocol0()


        # Do a quick routine to get the Affinity details.
        #if len(self.affinities) == 0:
        #    with self:
        #        self.retrieve_affinities()


    def __enter__(self):
        self.connection = self.backend.connect(self.host, port=self.port)
        return self


    def __exit__(self, type, value, traceback):
        self.connection.close()
        self.connection = None


    def retrieve_affinities(self):
        capabilities = self.protocol.capabilities(self.connection)
        for i in range(len(capabilities)):
            affinity_profile = capabilities[i]
            new_affinity = i_affinity.RemoteAffinity(self, i, affinity_profile)

            self.affinities.append(new_affinity)


    def search(self, propagation_limit, input_set, progress_frequency=0, progress_callback=None):

        return self.protocol.search(self.connection, input_set, progress_frequency=progress_frequency, progress_callback=progress_callback)


    def process(self, index, input_stream, progress_frequency=0, progress_callback=None):

        return self.affinities[index].run(self.connection, input_stream, progress_frequency=progress_frequency, progress_callback=progress_callback)


    def capabilities(self):

        capabilities = []

        for each_affinity in self.affinities:
            capabilities.append(each_affinity.profile)

        return capabilities
