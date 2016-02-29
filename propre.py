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

"""ProPre class.
"""

from ctes import *

class ProPre(object):
    
    def __init__(self, k_data, b1_data, a2_data, index):
        """Constructor.                        
        """    
        
        self._k_data = k_data
        self._b1_data = b1_data
        self._a2_data = a2_data
        self._index = index
        
        self._pro = []
        self._pre = []
            
    def _get_data(self, data, name):
        
        row = []
        
        for d in data:
            if d[NAME_COL_CL] == name:
                row = d
                break
        
        return row
    
    def _calculate_pro_data(self, data):
        
        final_data = []
        
        data_sum = float(sum(data))
        
        for d in data:
            final_data.append(100 * float(d) / data_sum)
        
        return final_data
    
    def _save_pro_data(self):
        
        out_file_name = PRO_FILE_NAME_PREFIX + self._index + INPUT_FILE_NAME_EXT
        
        f = open(out_file_name,'w')
        
        for p in self._pro:
            
            f.write("%s\n" % CSV_DELIMITER.join(str(i) for i in p))
        
        f.close()   
        
        print "Pro data saved in: %s" % out_file_name       
    
    @property
    def index_data(self):
        return self._index
    
    @property
    def pro_data(self):
        return self._pro
    
    @property
    def pre_data(self):
        return self._pre
    
    def generate_pro_data(self):
        
        for k in self._k_data:
            if k[TYPE_COL] == TYPE_1_COL:  
                data_source = self._b1_data
            else:
                data_source = self._a2_data
                
            data = self._get_data(data_source, k[NAME_LO_COL])
                
            lo_data = [int(data[i]) for i in \
                       range(CL_INDEX_LO, CL_INDEX_LO + CL_INDEX_SIZE)]    
            
            final_lo_data = self._calculate_pro_data(lo_data)         
            
            data = self._get_data(data_source, k[NAME_VI_COL])
            
            vi_data = [int(data[i]) for i in \
                       range(CL_INDEX_VI, CL_INDEX_VI + CL_INDEX_SIZE)]
            
            final_vi_data = self._calculate_pro_data(vi_data)
            
            self._pro.append([int(round(LO_WEIGHT * final_lo_data[FIRST_LO] + 
                                        final_vi_data[FIRST_VI] * VI_WEIGHT)),
                              int(round(LO_WEIGHT * final_lo_data[SECOND_LO] + 
                                        final_vi_data[SECOND_VI] * VI_WEIGHT)),
                              int(round(LO_WEIGHT * final_lo_data[THIRD_LO] + 
                                        final_vi_data[THIRD_VI] * VI_WEIGHT))])
            
        self._save_pro_data()
        
        return self._pro
    
    def generate_pre_data(self):  
        
        k_element_data = self._get_pro_data_source()
        
        for ke in k_element_data:
            
            pass 
        
        self._pre   
