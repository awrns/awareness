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

    def toDatums(self):
        return list(self.parameters)


    @classmethod
    def fromDatums(self, datums):
        return Item(tuple(datums))



class Stream:


    items = []

    def __init__(self, items):
        self.items = items


    def toDatums(self):
        datums = []
        for item in self.items:
            datums.append(item.toDatums())
        return datums


    def fromCountDatums(self, count, datums):
        items = []
        nParams = len(datums) / count

        for itemIndex in count:
            startPos = itemIndex * nParams
            endPos = (itemIndex + 1) * nParams
            items.append(Item.fromDatums(datums[startPos:endPos]))

        return Stream(items)



class Set:

    inputStream = None
    outputStream = None

    def __init__(self, inputStream, outputStream):
        self.inputStream = inputStream
        self.outputStream = outputStream


    def toDatums(self):
        return self.inputStream.toDatums() + self.outputStream.toDatums()  # concat


    @classmethod
    def fromInputsOutputsCountDatums(self, nInputs, nOutputs, count, datums):

        inputs = datums[:nInputs*count]
        outputs = datums[nInputs*count:nOutputs*count]

        inputStream = Stream.fromDatums(outputs)
        outputStream = Stream.fromDatums(outputs)


        return Set(inputStream, outputStream)


class Assembly:
    

    def run(self, inputStream, progressFrequency=0, progressCallback=None):
        pass
