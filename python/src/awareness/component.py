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



class Component:
    __metaclass__ = ABCMeta


    def getinputs(self): raise NotImplementedError()
    def setinputs(self, values): raise NotImplementedError()
    inputs = abstractproperty(getinputs, setinputs)


    def getoutputs(self): raise NotImplementedError()
    def setoutputs(self, value): raise NotImplementedError()
    outputs = abstractproperty(getoutputs, setoutputs)


    @abstractmethod
    def run(self, input_stream, progress_frequency=0, progress_callback=None):
        raise NotImplementedError()



class LocalComponent(Component):


    def __init__(self):

        pass


    def to_json(self):
        raise NotImplementedError()


    @classmethod
    def from_json(self, json):
        raise NotImplementedError()



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

