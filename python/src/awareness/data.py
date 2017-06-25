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



import operator as i_operator
import numpy


import warnings
warnings.filterwarnings("ignore")



class Stream:


    items = []

    def __init__(self, items):
        self.items = numpy.asarray(items, dtype=numpy.uint8)


    def to_datums(self):

        arr = self.items.flatten()
        arr.shape = (arr.size, 1)
        return arr


    def extract(self, start_parameter, end_parameter):

        subset = self.items[:, start_parameter:end_parameter]
        return Stream(subset)


    def inject(self, other_stream, start_parameter, end_parameter):

        self.items[:, start_parameter:end_parameter] = other_stream.items


    @classmethod
    def cost(self, stream1, stream2):

        # Mean bitwise error

        arr = numpy.bitwise_xor(stream1.items, stream2.items)
        arr = numpy.unpackbits(arr)
        mean = numpy.mean(arr)

        return mean


    @classmethod
    def msdi(self, stream1, stream2):

        # Most significant difference index

        costs = numpy.empty(stream1.items.parameters, dtype=numpy.uint8)

        for i in xrange(stream1.items.parameters):

            s1 = stream1.items[:, i:i+1]
            s2 = stream2.items[:, i:i+1]

            arr = numpy.bitwise_xor(s1, s2)
            arr = numpy.unpackbits(arr)
            mean = numpy.mean(arr)

            costs[i] = mean


        greatest_idx = numpy.argmax(costs)

        return greatest_idx


    @classmethod
    def from_count_datums(self, count, datums):

        arr = numpy.asarray(datums, dtype=numpy.uint8)
        arr.shape = (count, arr.size / count)
        return Stream(arr)


    @property
    def count(self):

        return self.items.shape[0]


    @property
    def parameters(self):

        return self.items.shape[1]


    @classmethod
    def blankFromCountParameters(self, count, parameters):
        
        arr = numpy.zeros((count, parameters), dtype=numpy.uint8)
        return Stream(arr)



class Set:

    input_stream = None
    output_stream = None

    def __init__(self, input_stream, output_stream):
        self.input_stream = input_stream
        self.output_stream = output_stream


    def to_datums(self):

        return numpy.concatenate((self.input_stream.to_datums(), self.output_stream.to_datums()))



    @classmethod
    def from_inputs_outputs_count_datums(self, n_inputs, n_outputs, count, datums):


        input_arr = datums[:n_inputs*count]
        output_arr = datums[n_inputs*count:(n_inputs*count) + n_outputs*count]

        input_stream = Stream.from_count_datums(count, input_arr)
        output_stream = Stream.from_count_datums(count, output_arr)


        return Set(input_stream, output_stream)



    @property
    def count(self):
        return self.input_stream.count

    @property
    def inputs(self):
        return self.input_stream.parameters

    @property
    def outputs(self):
        return self.output_stream.parameters



class Assembly:

    # Naive conditional operation sequence.


    # List of tuples (thresh_idx, targ_0, addr0, port0, index0, in_offset0, out_offset0, targ_1, addr1, port1, index1, in_offset1, out_offset1)
    operations = []

    def __init__(self, operations):

        self.operations = operations


    def to_datums(self):
        return self.operations

    @classmethod
    def from_datums(self, datums):

        operations = []
        for datum in datums:
            listdatum = list(datum)
            listdatum[0] = listdatum[0].rstrip('\0')
            operations.append(tuple(listdatum))

        return Assembly(operations)


    def run(self, input_stream, progress_frequency=0, progress_callback=None):


        stream_state = input_stream  # Pump pipeline on first iteration

        for operation in self.operations:

            with i_operator.RemoteOperator(operation[0], port=operation[1]) as operator:
                operator.retrieve_components()

                data_in_start_idx = operation[3]  # in_offset
                data_in_end_idx = operation[3] + operator.components[operation[2]].inputs  # plus number of inputs

                data_section = stream_state.extract(data_in_start_idx, data_in_end_idx)

                result = operator.process(operation[2], data_section)

                data_out_start_idx = operation[4]  # out_offset
                data_out_end_idx = operation[4] + operator.components[operation[2]].outputs  # plus number of outputs
                stream_state.inject(result, data_out_start_idx, data_out_end_idx)  # stream_state will then be used above to construct a new Stream for the next operation


        return stream_state
