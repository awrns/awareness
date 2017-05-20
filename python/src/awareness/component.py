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


class Component:
    __metaclass__ = ABCMeta

    def getoperator(self): raise NotImplementedError()
    def setoperator(self, value): raise NotImplementedError()
    operator = abstractproperty(getoperator, setoperator)

    def getindex(self): raise NotImplementedError()
    def setindex(self, value): raise NotImplementedError()
    index = abstractproperty(getindex, setindex)


    def getinputs(self): raise NotImplementedError()
    def setinputs(self, values): raise NotImplementedError()
    inputs = abstractproperty(getindex, setindex)


    def getoutputs(self): raise NotImplementedError()
    def setoutputs(self, value): raise NotImplementedError()
    outputs = abstractproperty(getoutputs, setoutputs)


    @abstractmethod
    def run(self, input_stream, progress_frequency=0, progress_callback=None):
        raise NotImplementedError()


class LocalComponent(Component):

    operator = None
    index = 0

    def __init__(self,
                 operator,
                 index):  # profile is defined in children of LocalComponent

        self.operator = operator
        self.index = index


class RemoteComponent(Component):

    operator = None
    index = 0

    inputs = -1
    outputs = -1


    def __init__(self,
                 operator,
                 index,
                 inputs,
                 outputs):

        self.operator = operator
        self.index = index
        self.inputs = inputs
        self.outputs = outputs


    def run(self, connection, input_stream, progress_frequency=0, progress_callback=None):

        output = self.operator.protocol.process(connection, self.index, input_stream, progress_frequency=progress_frequency, progress_callback=progress_callback)

        return output

