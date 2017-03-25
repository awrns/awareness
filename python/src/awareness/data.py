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


class ItemApplication():
    INPUT = True
    OUTPUT = False


class Item:

    affinity = None
    application = None
    parameters = ()

    def __init__(self, affinity, application, parameters):
        self.affinity = affinity
        self.application = application
        self.parameters = parameters

    def toDatums(self):
        return list(self.parameters)


    @classmethod
    def fromAffinityApplicationDatums(self, affinity, application, datums):
        return Item(affinity, application, tuple(datums))



class Stream:


    items = []

    def __init__(self, items):
        self.items = items

    @property
    def affinity(self):  # Required by Protocol to form output Streams for accessor process calls
        return self.items[0].affinity


    def toDatums(self):
        datums = []
        for item in self.items:
            datums.append(item.toDatums())
        return datums


    def fromAffinityApplicationDatums(self, affinity, application, datums):
        items = []

        if application == ItemApplication.INPUT:
            nParams = affinity.inputs
        elif application == ItemApplication.OUTPUT:
            nParams = affinity.outputs

        for itemIndex in range(len(datums) / nParams):
            startPos = itemIndex * nParams
            endPos = (itemIndex + 1) * nParams
            items.append(Item.fromAffinityApplicationDatums(affinity, application, datums[startPos:endPos]))

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
    def fromAffinityCountDatums(self, affinity, count, datums):

        inputs = datums[:affinity.inputs*count]
        outputs = datums[affinity.inputs*count:affinity.outputs*count]

        inputStream = Stream.fromAffinityApplicationDatums(affinity, ItemApplication.INPUT, datums)
        outputStream = Stream.fromAffinityApplicationDatums(affinity, ItemApplication.OUTPUT, datums)


        return Set(affinity, inputStream, outputStream)


class Assembly:
    

    def run(self, inputStream, progressFrequency=0, progressCallback=None):
        pass
