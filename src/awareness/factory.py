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