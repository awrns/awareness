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
import copy
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


        # Overall cost tracking for termination detection.
        last_cost = float('inf')
        cost = float('inf')
        first = True

        # Overall assembly state tracking.
        last_assembly = i_data.Assembly([])
        current_assembly = i_data.Assembly([])

        # Current data status, used in order to prevent re-run()-ning the current assembly each iteration
        max_param_len = max(len(input_set.output_stream.items[0].parameters), len(input_set.input_stream.items[0].parameters))
        current_stream = i_data.Stream.blankFromCountParameters(input_set.output_stream.count, max_param_len)
        current_stream.inject(input_set.input_stream, 0, len(input_set.input_stream.items[0].parameters))

        while cost < last_cost or first: # TODO use a more sophisticated stopping mechanism...
            first = False

            # Best results provided by any RemoteOperator so far.
            lowest_cost = float('inf')
            lowest_assembly = i_data.Assembly([])

            # Prime with the results of our own local capabilities.
            lowest_assembly, lowest_cost = self.search_internal(local_operator, i_data.Set(current_stream, input_set.output_stream))

            # if it is necessary to recursively search other Operators on the network:
            if propagation_limit > 0:
                for operator in remote_operators:
                    with operator:
                        res = operator.search(propagation_limit-1, i_data.Set(current_stream, input_set.output_stream))
                        full_outs = res.run(current_stream)
                    this_cost = self.cost(full_outs.extract(0, len(input_set.output_stream.items[0].parameters)), input_set.output_stream)
                    if this_cost < lowest_cost:
                        lowest_cost = this_cost
                        lowest_assembly = res

            else:
                # In the case that we are only searching locally, there's no sense in calling search_internal again.
                # Return its result, which is the best we'll get.
                return lowest_assembly


            # Update known state of the data stream, and of the Assembly that has formed
            current_stream = lowest_assembly.run(current_stream)
            
            last_assembly = copy.deepcopy(current_assembly)
            current_assembly.operations.extend(lowest_assembly.operations)

            # Update known state of the cost
            last_cost = cost
            cost = lowest_cost


        # Note that when the 'while cost.....' loop exits, both curernt_assembly and cost are not optimal,
        # since cost decreased on the last iteration. Use the 'last' (previous) iteration as the best result.
        return last_assembly
            



    def search_internal(self,
                        local_operator,
                        input_set,
                        progress_frequency=0,
                        progress_callback=None):


        # Overall cost tracking for termination detection.
        last_cost = float('inf')
        cost = float('inf')
        first = True

        #Overall assembly state tracking.
        last_assembly = i_data.Assembly([])
        current_assembly = i_data.Assembly([])

        # Current data status, used in order to prevent re-run()-ning the current assembly each iteration
        max_param_len = max(len(input_set.output_stream.items[0].parameters), len(input_set.input_stream.items[0].parameters))
        current_stream = i_data.Stream.blankFromCountParameters(input_set.output_stream.count, max_param_len)
        current_stream.inject(input_set.input_stream, 0, len(input_set.input_stream.items[0].parameters))

        while cost < last_cost or first: # TODO use a more sophisticated stopping mechanism...
            first = False

            # Best results produced by any LocalAffinity so far.
            lowest_cost = float('inf')
            lowest_affinity = None
            lowest_in_offset = 0
            lowest_out_offset = 0

            for affinity in local_operator.affinities:

                # Large nested iterative search over all possible configurations.
                # Note that the expression   len(current_stream.items[0].parameters) - affinity.inputs
                # evaluates to the number of offsets which are possible for the given affinity.inputs count and stream parameters count.

                for test_in_offset in range(len(current_stream.items[0].parameters) - affinity.inputs + 1):
                    for test_out_offset in range(len(current_stream.items[0].parameters) - affinity.outputs + 1):

                        # Extract the subset of the current_stream data that this Affinity will try to process.
                        res = affinity.run(current_stream.extract(test_in_offset, test_out_offset + affinity.inputs))

                        # Create a 'model' stream in which to inject the result of the affinity's processing at the correct offset.
                        full_outs = copy.deepcopy(current_stream)
                        full_outs.inject(res, test_out_offset, test_out_offset + affinity.outputs)

                        # Evaluate the results.
                        this_cost = self.cost(full_outs.extract(0, len(input_set.output_stream.items[0].parameters)), input_set.output_stream)
                        if this_cost < lowest_cost:
                            # Update the best solution.
                            lowest_cost = this_cost
                            lowest_affinity = affinity
                            lowest_in_offset = test_in_offset
                            lowest_out_offset = test_out_offset

            # Analogous to the offset processing in the above loop - update current_stream by first
            # extracting the section of it that has proved to be the best by the above loop
            # and processing it by the LocalAffinity that has been the most promising.
            # Finally, inject its results at the best known ouput offset over the same current data stream.

            res = lowest_affinity.run(current_stream.extract(lowest_in_offset, lowest_out_offset + affinity.inputs))
            current_stream.inject(res, lowest_out_offset, lowest_out_offset + lowest_affinity.outputs)

            # Add information about this new Affinity to the Assembly we're creating.
            append_tuple = (local_operator.public_host, local_operator.port, lowest_affinity.index, lowest_in_offset, lowest_out_offset)
            last_assembly = copy.deepcopy(current_assembly)
            current_assembly.operations.append(append_tuple)

            # Update costs.
            last_cost = cost
            cost = lowest_cost


        # Note that when the 'while cost.....' loop exits, both curernt_assembly and cost are not optimal,
        # since cost decreased on the last iteration. Use the 'last' (previous) iteration as the best result.
        return last_assembly, last_cost




    def cost(self, stream1, stream2):

        total = 0
        count = 0

        for item1, item2 in zip(stream1.items, stream2.items):
            for param1, param2 in zip(item1.parameters, item2.parameters):
                total += (abs(param1-param2))**2
                count += 1

        mean = total/count

        return mean


