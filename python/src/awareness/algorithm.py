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
import data as i_data



class Algorithm:
    __metaclass__ = ABCMeta

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

        suggestions = []

        internal_cost, internal_assembly = self.search_internal(local_operator, i_data.Set(current_stream, input_set.output_stream))
        for i in xrange(len(internal_assembly.operations)):
            if 0 <= i < len(suggestions): # If this level exists
                suggestions[i].append(internal_assembly.operations[i][2:7])
                suggestions[i].append(internal_assembly.operations[i][8:13])
            else:
                suggestions[i] = [internal_assembly.operations[i][2:7], internal_assembly.operations[i][8:13]]


       if recursion_limit > 0:
            for operator in remote_operators:
                with operator:
                    res = operator.search(recursion_limit-1, i_data.Set(current_stream, input_set.output_stream))
                    for i in xrange(len(res.operations)):
                        if 0 <= i < len(suggestions):
                            suggestions[i].append(res.operations[i][2:7])
                            suggestions[i].append(res.operations[i][8:13])
                        else:
                            suggestions[i] = [res.operations[i][2:7], res.operations[i][8:13]]


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

                for test_in_offset in xrange(current_stream.parameters - component.inputs + 1):

                    # Extract the subset of the current_stream data that this Component will try to process.
                    res = component.run(current_stream.extract(test_in_offset, test_in_offset + component.inputs))


                    for test_out_offset in xrange(current_stream.parameters - component.outputs + 1):

                        # Create a 'model' stream in which to inject the result of the component's processing at the correct offset.
                        full_outs = copy.deepcopy(current_stream)
                        full_outs.inject(res, test_out_offset, test_out_offset + component.outputs)

                        # Evaluate the results.
                        outset = full_outs.extract(0, input_set.outputs)
                        this_cost = i_data.Stream.cost(outset, input_set.output_stream)

                        # Find the item of the test set that has the best cost (is most characteristic of this solution).
                        best_item_cost = float('inf')
                        best_item_idx = 0
                        for i in xrange(outset.count):
                            this = i_data.Stream.cost(i_data.Stream(outset.items[i]), input_set.output_stream)
                            if this < best_item_cost:
                                best_item_cost = this
                                best_item_idx = i

                        options.append((this_cost, best_item_idx, component, test_in_offset, test_out_offset))


            # Best results produced by any LocalComponent so far.
            lowest_cost = float('inf')
            lowest_best_item_idx = 0
            lowest_component = None
            lowest_in_offset = 0
            lowest_out_offset = 0

            second_lowest_cost = float('inf')
            second_lowest_best_item_idx = 0
            second_lowest_component = None
            second_lowest_in_offset = 0
            second_lowest_out_offset = 0

            for option in options:
                if option[0] < lowest_cost:
                    # Update the best solution.
                    lowest_cost = option[0]
                    lowest_best_item_idx = option[1]
                    lowest_component = option[2]
                    lowest_in_offset = option[3]
                    lowest_out_offset = option[4]

                elif option[0] < second_lowest_cost:
                    second_lowest_cost = option[0]
                    second_lowest_best_item_idx = option[1]
                    second_lowest_component = option[2]
                    second_lowest_in_offset = option[3]
                    second_lowest_out_offset = option[4]


            if lowest_component is None and second_lowest_component is None:
                return i_data.Assembly([]), float('inf')


            # Determine the parameter index to use as a threshold.
            stream_opt0 = i_data.Stream([current_stream.items[lowest_best_item_idx]  ,])
            stream_opt1 = i_data.Stream([current_stream.items[second_lowest_best_item_idx]  ,])

            highest_diffcost = 0
            chosen_idx = 0
            for i in xrange(stream_opt0.parameters):
                this = i_data.Stream.cost(stream_opt0.extract(i, i+1), stream_opt1.extract(i, i+1))
                if this > highest_diffcost:
                    highest_diffcost = this
                    chosen_idx = i

            # Get the values
            targ0 = stream_opt0.items[0][chosen_idx]
            targ1 = stream_opt1.items[0][chosen_idx]

            # Add information about this new operation to the Assembly we're creating.
            append_tuple = (chosen_idx, targ0, 
                            local_operator.public_host, local_operator.port, local_operator.components.index(lowest_component), lowest_in_offset, lowest_out_offset,
                            targ1,
                            local_operator.public_host, local_operator.port, local_operator.components.index(second_lowest_component), second_lowest_in_offset, second_lowest_out_offset
                            )

            last_assembly = copy.deepcopy(current_assembly)
            current_assembly.operations.append(append_tuple)

            # Update the state of the current stream.
            subassembly = i_data.Assembly([append_tuple,])
            current_stream = subassembly.run(current_stream)

            # Update costs.
            last_cost = cost
            cost = lowest_cost


        # Note that when the 'while cost.....' loop exits, both curernt_assembly and cost are not optimal,
        # since cost decreased on the last iteration. Use the 'last' (previous) iteration as the best result.
        return last_cost, last_assembly
