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
               local_affinities,
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
               local_affinities,
               remote_operators,
               propagation_limit,
               input_set,
               progress_frequency=0,
               progress_callback=None):

        affinities = []

        affinities += local_affinities
        if propagation_limit > 0:
            for operator in remote_operators:
                affinities += operator.affinities

        propagation_limit -= 1


        last_cost = -1
        cost = -1

        while cost <= last_cost:
            pass


    def cost(self): pass
