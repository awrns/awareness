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
