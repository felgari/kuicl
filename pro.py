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

"""Calculation of pro.
"""

from ctes import *
from kscrap import KScrap
from kfiles import read_input_file, save_data_to_csv
from putil import combine_lo_vi, get_cl_data_for_name

class Pro(object):
    
    def __init__(self, index, k, b1, a2):
        """Constructor.                        
        """    
        
        self._index = index
        self._pro = []
        self._k = k
        self._b1 = b1
        self._a2 = a2
        
        self._generate()
    
    @staticmethod
    def _calculate_pro_data(data):
        
        if int(sum(data)):
            data_sum = float(sum(data))
        else:
            data_sum = 1.0
        
        return [ 100.0 * float(d) / data_sum for d in data ]
    
    @staticmethod
    def get_data_for_pro(k, cl_data, is_lo):
        
        if is_lo:
            name_col = NAME_LO_COL
            p_range = LO_P_RANGE
        else:
            name_col = NAME_VI_COL
            p_range = VI_P_RANGE
                    
        data_from_name = get_cl_data_for_name(k[name_col], cl_data)
        
        pos = int(data_from_name[CL_POS_COL])
        
        data_from_range = [int(data_from_name[i]) for i in p_range]
        
        data_for_calc = Pro._calculate_pro_data(data_from_range)
        
        return data_for_calc, pos
    
    def _generate(self):
        
        pro_file_name = PRO_FILE_NAME_PREFIX + self._index + INPUT_FILE_NAME_EXT
    
        self._pro = read_input_file(pro_file_name)
        
        if not len(self._pro):
        
            for k in self._k:             
                       
                if k[TYPE_COL] == TYPE_1_COL:  
                    cl_data = self._b1
                else:
                    cl_data = self._a2
                    
                calc_lo_data, lo_pos = Pro.get_data_for_pro(k, cl_data, True)         
                
                calc_vi_data, vi_pos = Pro.get_data_for_pro(k, cl_data, False) 
                
                self._pro.append(combine_lo_vi(calc_lo_data, calc_vi_data))
                
            if self.generated:
                save_data_to_csv(pro_file_name, self._pro)
            
    @property
    def pro(self):
        return self._pro
    
    @property
    def generated(self):
        return len(self._pro)
        