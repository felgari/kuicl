# -*- coding: utf-8 -*-

# Copyright (c) 2016 Felipe Gallego. All rights reserved.
#
# This is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Some utilities for the calculation of p.
"""

from ctes import *

def get_cl_data_for_name(name, cl_data):
    
    row = []
    
    for cl_d in cl_data:
        if cl_d[CL_NAME_COL] == name:
            row = cl_d
            break
        
    return row

def combine_lo_vi(lo, vi):
    
    return [int(round(LO_WEIGHT * lo[FIRST_LO] + vi[FIRST_VI] * VI_WEIGHT)), 
            int(round(LO_WEIGHT * lo[SECOND_LO] + vi[SECOND_VI] * VI_WEIGHT)),
            int(round(LO_WEIGHT * lo[THIRD_LO] + vi[THIRD_VI] * VI_WEIGHT))] 