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


        last_cost = -1
        cost = -1

        current_assembly = None

        while cost <= last_cost:
            
            suggested_assemblies = []

            for operator in remote_operators:
                res = operator.search(propagation_limit, input_set)
                suggested_assemblies.append(res)


    def search_internal(self,
                        local_operator,
                        input_set,
                        progress_frequency=0,
                        progress_callback=None):


        last_cost = float('inf')
        cost = float('inf')

        current_assembly = i_data.Assembly([])
        current_stream = input_set[0]

        while cost <= last_cost:

            lowest_cost = float('inf')
            lowest_affinity = None
            in_offset = 0
            out_offset = 0  # TODO set these in the below search loop

            for affinity in local_operator.affinities:
                res = affinity.run(current_stream) # TODO TODO splicing and in/out offsets
                this_cost = self.cost(res, input_set[1])
                if this_cost < lowest_cost:
                    lowest_cost = this_cost
                    lowest_affinity = affinity

            current_stream = lowest_affinity.run(current_stream)
            append_tuple = (local_operator.host, local_operator.port, lowest_affinity.index, in_offset, out_offset)
            current_assembly.operations.append()


            last_cost = cost
            cost = lowest_cost



    def cost(self, stream1, stream2): pass
