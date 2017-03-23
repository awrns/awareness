#
# This file is part of the Awareness Operator Python implementation.
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


from abc import ABCMeta, abstractproperty, abstractmethod
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
               localAbilities,
               remoteOperators,
               propagationLimit,
               inputSet,
               progressFrequency=0,
               progressCallback=None):

        raise NotImplementedError()


class DefaultAlgorithm(Algorithm):

    def search(self,
               localAbilities,
               remoteOperators,
               propagationLimit,
               inputSet,
               progressFrequency=0,
               progressCallback=None):

        pass
