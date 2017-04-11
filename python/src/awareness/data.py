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


import exception
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

    def to_datums(self):
        datums = []
        for parameter in self.parameters:
            datums.append((float(parameter),))  # The parameter in a 1-tuple
        return datums


    @classmethod
    def from_datums(self, datums):
        parameters = []
        for datum in datums:
            parameters.append(datum[0])  # First (only) tuple item
        return Item(tuple(parameters))

    @property
    def count(self):
        return len(self.parameters)



class Stream:


    items = []

    def __init__(self, items):
        self.items = items


    def to_datums(self):
        datums = []
        for item in self.items:
            datums += item.to_datums()
        return datums

    @classmethod
    def from_count_datums(self, count, datums):
        items = []
        n_params = len(datums) / count if count != 0 else 0

        for item_index in range(count):
            start_pos = item_index * n_params
            end_pos = (item_index + 1) * n_params
            items.append(Item.from_datums(datums[start_pos:end_pos]))

        return Stream(items)


    @property
    def count(self):
        return len(self.items)



class Set:

    input_stream = None
    output_stream = None

    def __init__(self, input_stream, output_stream):
        self.input_stream = input_stream
        self.output_stream = output_stream


    def to_datums(self):
        return self.input_stream.to_datums() + self.output_stream.to_datums()  # concat


    @classmethod
    def from_inputs_outputs_count_datums(self, n_inputs, n_outputs, count, datums):

        inputs = datums[:n_inputs*count]
        outputs = datums[n_inputs*count:n_outputs*count]

        input_stream = Stream.from_datums(outputs)
        output_stream = Stream.from_datums(outputs)


        return Set(input_stream, output_stream)


    @property
    def count(self):
        return self.input_stream.count


class Assembly:

    # List of tuples (addr, port, index, slice, offset)
    operations = []

    def __init__(self, operations):

        self.operations = operations


    def to_datums(self):
        return self.operations

    @classmethod
    def from_datums(self, datums):

        return Assembly(datums)


    def run(self, input_stream, progress_frequency=0, progress_callback=None):
        
        max_slice = -1
        for operation in self.operations:
            if operation[4] > max_slice: max_slice = operation[4]


        data_status = input_stream  # Pump pipeline on first iteration

        for slice in range(max_slice):
            pass
            #with i_operator.RemoteOperator(operation[0].rstrip('\0'), port=operation[1]) as operator:
            #    operator.retrieve_affinities()
            #    result = operator.process(operation[3], result)
