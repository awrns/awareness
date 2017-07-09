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


from abc import ABCMeta, abstractmethod
import copy
from . import data as i_data



class Algorithm(metaclass=ABCMeta):
    @abstractmethod
    def search(self,
               local_operator,
               remote_operators,
               recursion_limit,
               input_set,
               progress_frequency=0,
               progress_callback=None):

        raise NotImplementedError()



class DefaultAlgorithm(Algorithm):


    # Aedan's algorithm implementation; there are certainly better ways to do this though.
    # that evaluates the results of Components to create a 'program' (Assembly).

    def search(self,
               local_operator,
               remote_operators,
               recursion_limit,
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
        max_param_len = max(input_set.outputs, input_set.inputs)
        current_stream = i_data.Stream.blankFromCountParameters(input_set.output_stream.count, max_param_len)
        current_stream.inject(input_set.input_stream, 0, input_set.input_stream.parameters)


        while cost < last_cost or first: # TODO use a more sophisticated stopping mechanism...
            first = False

            options = []

            # if it is necessary to recursively search other Operators on the network:
            if recursion_limit > 0:
                for operator in remote_operators:
                    with operator:
                        res = operator.search(recursion_limit-1, i_data.Set(current_stream, input_set.output_stream))
                        full_outs = res.run(current_stream)
                    this_cost = i_data.Stream.cost(full_outs.extract(0, input_set.outputs), input_set.output_stream)

                    options.append((this_cost, res))


            # Best results provided by any RemoteOperator so far.
            lowest_cost = float('inf')
            lowest_assembly = i_data.Assembly([])

            # Prime with the results of our own local capabilities.
            internal_cost, internal_assembly = self.search_internal(local_operator, i_data.Set(current_stream, input_set.output_stream))
            options.append((internal_cost, internal_assembly))

            for option in options:
                if option[0] < lowest_cost:
                    lowest_cost = option[0]
                    lowest_assembly = option[1]


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
        max_param_len = max(input_set.outputs, input_set.inputs)
        current_stream = i_data.Stream.blankFromCountParameters(input_set.output_stream.count, max_param_len)
        current_stream.inject(input_set.input_stream, 0, input_set.inputs)

        while cost < last_cost or first: # TODO use a more sophisticated stopping mechanism...
            first = False

            options = []

            for component in local_operator.components:

                # Large nested iterative search over all possible configurations.
                # Note that the expression   current_stream.parameters - component.inputs + 1
                # evaluates to the number of offsets which are possible for the given component.inputs count and stream parameters count.

                for test_in_offset in range(current_stream.parameters - component.inputs + 1):

                    # Extract the subset of the current_stream data that this Component will try to process.
                    res = component.run(current_stream.extract(test_in_offset, test_in_offset + component.inputs))


                    for test_out_offset in range(current_stream.parameters - component.outputs + 1):

                        # Create a 'model' stream in which to inject the result of the component's processing at the correct offset.
                        full_outs = copy.deepcopy(current_stream)
                        full_outs.inject(res, test_out_offset, test_out_offset + component.outputs)

                        # Evaluate the results.
                        this_cost = i_data.Stream.cost(full_outs.extract(0, input_set.outputs), input_set.output_stream)


                        options.append((this_cost, component, test_in_offset, test_out_offset))


            # Best results produced by any LocalComponent so far.
            lowest_cost = float('inf')
            lowest_component = None
            lowest_in_offset = 0
            lowest_out_offset = 0

            for option in options:
                if option[0] < lowest_cost:
                    # Update the best solution.
                    lowest_cost = option[0]
                    lowest_component = option[1]
                    lowest_in_offset = option[2]
                    lowest_out_offset = option[3]


            if lowest_component is None:
                return i_data.Assembly([]), float('inf')

            # Analogous to the offset processing in the above loop - update current_stream by first
            # extracting the section of it that has proved to be the best by the above loop
            # and processing it by the LocalComponent that has been the most promising.
            # Finally, inject its results at the best known ouput offset over the same current data stream.

            res = lowest_component.run(current_stream.extract(lowest_in_offset, lowest_out_offset + component.inputs))
            current_stream.inject(res, lowest_out_offset, lowest_out_offset + lowest_component.outputs)

            # Add information about this new component to the Assembly we're creating.
            append_tuple = (local_operator.public_host, local_operator.port, local_operator.components.index(lowest_component), lowest_in_offset, lowest_out_offset)
            last_assembly = copy.deepcopy(current_assembly)
            current_assembly.operations.append(append_tuple)

            # Update costs.
            last_cost = cost
            cost = lowest_cost


        # Note that when the 'while cost.....' loop exits, both curernt_assembly and cost are not optimal,
        # since cost decreased on the last iteration. Use the 'last' (previous) iteration as the best result.
        return last_cost, last_assembly
