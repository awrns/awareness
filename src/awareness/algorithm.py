#
# Copyright (c) 2016-2017 Aedan S. Cullen.
#
# This file is part of the Awareness Python implementation.
#
# Awareness is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Awareness is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Awareness.  If not, see <http://www.gnu.org/licenses/>.
#


from abc import ABCMeta, abstractmethod
import copy
import numpy
from . import data as i_data
from . import operator as i_operator



class Algorithm(metaclass=ABCMeta):
    @abstractmethod
    def search(self,
               local_operator,
               remote_operators,
               recursion_limit,
               input_set,
               split_idx,
               progress_callback=None):

        raise NotImplementedError()



class DefaultAlgorithm(Algorithm):


    # Aedan's algorithm implementation; there are probably better ways to do this though.
    # that evaluates the results of Components to create a 'program' (Assembly).

    def search(self,
               local_operator,
               remote_operators,
               recursion_limit,
               input_set,
               split_idx,
               progress_callback=None):

        
        training_set = i_data.Set(
            i_data.Stream(input_set.input_stream.items[:split_idx]),
            i_data.Stream(input_set.output_stream.items[:split_idx])
            )

        test_set = i_data.Set(
            i_data.Stream(input_set.input_stream.items[split_idx:]),
            i_data.Stream(input_set.output_stream.items[split_idx:])
            )



        # Overall cost tracking for termination detection.
        last_cost = float('inf')
        cost = float('inf')
        first = True

        # Overall assembly state tracking.
        last_assembly = i_data.Assembly([])
        current_assembly = i_data.Assembly([])

        # Current data status, used in order to prevent re-run()-ning the current assembly each iteration
        max_param_len = max(input_set.outputs, input_set.inputs)

        current_training_stream = i_data.Stream.from_blank(training_set.output_stream.count, max_param_len)
        current_training_stream.inject(training_set.input_stream, 0, training_set.input_stream.parameters)

        current_test_stream = i_data.Stream.from_blank(test_set.output_stream.count, max_param_len)
        current_test_stream.inject(test_set.input_stream, 0, test_set.input_stream.parameters)


        while cost < last_cost or first: # TODO use a more sophisticated stopping mechanism...
            first = False

            options = []

            # if it is necessary to recursively search other Operators on the network:
            if recursion_limit > 0:
                for operator in remote_operators:
                    

                    glued_set = i_data.Set(
                        i_data.Stream(current_training_stream.items.tolist() + current_test_stream.items.tolist()),
                        i_data.Stream(training_set.output_stream.items.tolist() + test_set.output_stream.items.tolist())
                    )

                    glue_index = current_training_stream.count

                    with operator:
                        res = operator.search(recursion_limit-1, glued_set, glue_index)

                    full_outs = res.run(current_test_stream)

                    this_cost = i_data.Stream.cost(full_outs.extract(0, test_set.outputs), test_set.output_stream)

                    options.append((this_cost, res))


            # Best results provided by any RemoteOperator so far.
            lowest_cost = float('inf')
            lowest_assembly = i_data.Assembly([])

            # Prime with the results of our own local capabilities.
            internal_cost, internal_assembly = self.search_internal(local_operator, i_data.Set(current_training_stream, training_set.output_stream))
            options.append((internal_cost, internal_assembly))

            for option in options:
                if option[0] < lowest_cost:
                    lowest_cost = option[0]
                    lowest_assembly = option[1]


            # Update known state of the data streams, and of the Assembly that has formed
            current_training_stream = lowest_assembly.run(current_training_stream)
            current_test_stream = lowest_assembly.run(current_test_stream)
            
            last_assembly = copy.deepcopy(current_assembly)
            current_assembly.operations.extend(lowest_assembly.operations)

            # Update known state of the cost
            last_cost = cost
            cost = lowest_cost


        # Now, last_assembly is the final result. Search the local Operator's remote_operators and add any that we don't know about yet.

        for operation in last_assembly.operations:
            found = False
            for existing_operator in local_operator.remote_operators:
                if existing_operator.host == operation[0] and existing_operator.port == operation[1]:
                    found = True
                    break

            if not found:
                new_remoteoperator = i_operator.RemoteOperator(operation[0], port = operation[1])
                local_operator.remote_operators.append(new_remoteoperator)


        # Note that when the 'while cost.....' loop exits, both curernt_assembly and cost are not optimal,
        # since cost decreased on the last iteration. Use the 'last' (previous) iteration as the best result.
        return last_assembly
            



    def search_internal(self,
                        local_operator,
                        input_set, # Note no split_idx. 

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
        current_stream = i_data.Stream.from_blank(input_set.output_stream.count, max_param_len)
        current_stream.inject(input_set.input_stream, 0, input_set.inputs)

        while cost < last_cost or first: # TODO use a more sophisticated stopping mechanism...
            first = False

            options = []

            for component in local_operator.components:

                # Large nested iterative search over all possible configurations.
                # Note that the expression   current_stream.parameters - component.inputs + 1
                # evaluates to the number of offsets which are possible for the given component.inputs count and stream parameters count.

                max_iolen = max(component.inputs, component.outputs)

                if max_iolen > current_stream.parameters:
                    continue

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
                return float('inf'), i_data.Assembly([])

            # Analogous to the offset processing in the above loop - update current_stream by first
            # extracting the section of it that has proved to be the best by the above loop
            # and processing it by the LocalComponent that has been the most promising.
            # Finally, inject its results at the best known ouput offset over the same current data stream.

            res = lowest_component.run(current_stream.extract(lowest_in_offset, lowest_in_offset + lowest_component.inputs))
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
