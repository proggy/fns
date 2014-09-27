#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright notice
# ----------------
#
# Copyright (C) 2014 Daniel Jung
# Contact: djungbremen@gmail.com
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
#
"""Frog definitions for this package. Requires the frog module."""
__created__ = '2014-09-27'
__modified__ = '2014-09-27'

from frog import Frog
import fns


# dashify
f = Frog(inmap=dict(files='$@'),
         usage='dashify [options] FILES',
         optdoc=dict(alldots='do not even preserve the last dot',
                     verbose='be verbose',
                     test='list changes without actually renaming any files',
                     nolower='do not switch to lowercase'))
         #allow_interspersed_args=False
f(fns.dashify)
