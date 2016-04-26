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

"""Calculation of p.
"""

from ctes import *
from kfiles import read_input_file, save_data_to_csv
from putil import combine_lo_vi

class PDat(object):
    
    def __init__(self, index, k, pro, pre, b1, a2):
        """Constructor.                        
        """
        
        self._index = index
        self._k = k
        self._pro = pro
        self._pre = pre
        self._p = []
        self._b1 = b1
        self._a2 = a2
        
        self._calculate()
        
    @staticmethod
    def _get_data_from_cl(cl_data, name):
        
        data = []

        for i, cdat in enumerate(cl_data):
            if cdat[CL_NAME_COL] == name:
                return cdat[:]
                
        return data 
        
    @staticmethod
    def _calculate_pro_data(data):
        
        if int(sum(data)):
            data_sum = float(sum(data))
        else:
            data_sum = 1.0
        
        return [ 100.0 * float(d) / data_sum for d in data ] 
    
    @staticmethod
    def calc_final_p(pro, pre, p_type):
        
        if p_type == TYPE_1_COL: 
            p_with = P_WITH_B1
        else:
            p_with = P_WITH_A2          
        
        p_num = []
        
        for i, pd in enumerate(pro):
            
            p_num.append(( int(pd) / 100.0 ) * ( int(pre[i]) / 100.0 ))
            
        if p_with > 0.0:
            p_num = [ p / p_with for p in p_num ]
            
        p_sum = sum(p_num)
        
        if p_sum > 0:
            p_num = [ int(round(100.0 * p / p_sum)) for p in p_num ]  
            
        return p_num 
        
    def _calculate(self):
        
        p_file_name = P_FILE_NAME_PREFIX + self._index + INPUT_FILE_NAME_EXT
        
        self._p = read_input_file(p_file_name)
        
        if not len(self._p):
        
            for i in range(NUM_ROWS):  
                
                p_value = PDat.calc_final_p(self._pro[i],
                                            self._pre[i],
                                            self._k[i][TYPE_COL])
                
                self._p.append(p_value)
            
            if self.generated:
                save_data_to_csv(p_file_name, self._p)
        
    @property
    def p(self):
        return self._p
    
    @property
    def generated(self):
        return len(self._p)