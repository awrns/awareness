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
import exception
import misc
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import operator as i_operator
import protocol as i_protocol


class Affinity:
    __metaclass__ = ABCMeta

    @abstractproperty
    def operator(self):
        raise NotImplementedError()

    @abstractproperty
    def index(self):
        raise NotImplementedError()


    @abstractproperty
    def profile(self):
        raise NotImplementedError()


    @abstractmethod
    def run(self, inputStream, progressFrequency=0, progressCallback=None):
        raise NotImplementedError()


class LocalAffinity(Affinity):

    operator = None
    index = 0

    def __init__(self,
                 operator,
                 index):  # profile is defined in children of LocalAffinity

        self.operator = operator
        self.index = index


class RemoteAffinity(Affinity):

    operator = None
    index = 0

    profile = ()


    def __init__(self,
                 operator,
                 index,
                 profile):

        self.operator = operator
        self.index = index
        self.profile = profile


    def run(self, connection, inputStream, progressFrequency=0, progressCallback=None):

        output = self.operator.protocol.process(connection, self.index, inputStream, progressFrequency=progressFrequency, progressCallback=progressCallback)

        return output

