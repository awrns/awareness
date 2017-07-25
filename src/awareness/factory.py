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
# Portions of this file are originally the work of Michael Nielsen,
# and are distributed here in a modified form under the terms of the MIT License.
# The following information applies to these portions.
#
# Copyright (c) 2012-2015 Michael Nielsen
#
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the Software 
# is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import io
import sys

backup = sys.stderr
sys.stderr = io.StringIO()
import theano
out = sys.stderr.getvalue()
sys.stderr = backup

if out.find("(") != -1:
    out = out[:out.find("(")]

sub = out.split(":")[-1]
device = sub.strip() if sub.strip() != "" else "CPU"

from abc import ABCMeta, abstractmethod


class Factory(metaclass=ABCMeta):

    @abstractmethod
    def fabricate(self, input_set, progress_frequency=0, progress_callback=None):
        raise NotImplementedError()


class DefaultFactory(Factory):

    def fabricate(self, input_set, progress_frequency=0, progress_callback=None):
        pass