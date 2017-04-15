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
import affinity as i_affinity
import backend as i_backend
import data as i_data
import operator as i_operator
import protocol as i_protocol


class Algorithm:
    __metaclass__ = ABCMeta

    @abstractmethod
    def search(self,
               local_operator,
               remote_operators,
               propagation_limit,
               input_set,
               progress_frequency=0,
               progress_callback=None):

        raise NotImplementedError()


    @abstractmethod
    def cost(self, stream1, stream2):
        raise NotImplementedError()




class DefaultAlgorithm(Algorithm):

    def search(self,
               local_operator,
               remote_operators,
               propagation_limit,
               input_set,
               progress_frequency=0,
               progress_callback=None):


        last_cost = float('inf')
        cost = float('inf')

        last_assembly = i_data.Assembly([])
        current_assembly = i_data.Assembly([])

        current_stream = input_set.input_stream

        while cost <= last_cost:
            
            lowest_cost = float('inf')
            lowest_assembly = None

            lowest_assembly, lowest_cost = self.search_internal(local_operator, input_set)


            if propagation_limit > 0:
                for operator in remote_operators:
                    res = operator.search(propagation_limit-1, input_set)
                    this_cost = self.cost(res.run(current_stream), input_set.output_stream)
                    if this_cost < lowest_cost:
                        lowest_cost = this_cost
                        lowest_assembly = res


            current_stream = lowest_assembly.run(current_stream)
            last_assembly = current_assembly
            current_assembly.operations.extend(lowest_assembly.operations)

            last_cost = cost
            cost = lowest_cost


        return last_assembly
            



    def search_internal(self,
                        local_operator,
                        input_set,
                        progress_frequency=0,
                        progress_callback=None):


        last_cost = float('inf')
        cost = float('inf')

        last_assembly = i_data.Assembly([])
        current_assembly = i_data.Assembly([])

        current_stream = input_set.input_stream

        while cost <= last_cost:

            lowest_cost = float('inf')
            lowest_affinity = None
            in_offset = 0
            out_offset = 0

            for affinity in local_operator.affinities:

                for test_in_offset in range(len(current_stream.items[0].parameters) - affinity.inputs):
                    for test_out_offset in range(len(current_stream.items[0].parameters) - affinity.outputs):

                        res = affinity.run(current_stream.extract(test_in_offset, test_in_offset + affinity.inputs))

                        full_outs = current_stream
                        full_outs.inject(res, test_out_offset, test_out_offset + affinity.outputs)

                        this_cost = self.cost(full_outs, input_set.output_stream)
                        if this_cost < lowest_cost:
                            lowest_cost = this_cost
                            lowest_affinity = affinity
                            in_offset = test_in_offset
                            out_offset = test_out_offset


            current_stream = lowest_affinity.run(current_stream)
            append_tuple = (local_operator.host, local_operator.port, lowest_affinity.index, in_offset, out_offset)
            last_assembly = current_assembly
            current_assembly.operations.append(append_tuple)

            last_cost = cost
            cost = lowest_cost



        return last_assembly, last_cost




    def cost(self, stream1, stream2): pass
