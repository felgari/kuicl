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

"""Calculation of pre.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from ctes import *
from kscrap import KScrap
from kfiles import read_input_file, read_res_file, save_data_to_csv
from putil import combine_lo_vi, get_cl_data_for_name

class Pre(object):
    
    def __init__(self, index, k, b1, a2):
        """Constructor.                        
        """    
        
        self._index = index
        self._pre = []
        self._k = k
        self._b1 = b1
        self._a2 = a2
        
        self._generate()
    
    def _get_data_for_pre(self, name, cl_data, res_data, is_lo):
        
        pre_data = []
        
        if is_lo:
            col = LO_COL_RES
            col_other = VI_COL_RES
            the_range = LO_D_RANGE
            the_other_range = VI_D_RANGE
        else:
            col = VI_COL_RES
            col_other = LO_COL_RES  
            the_range = VI_D_RANGE
            the_other_range = LO_D_RANGE
            
        cl = get_cl_data_for_name(name, cl_data)
        final_cl = [cl[i] for i in the_range]
        
        for res_d in res_data:       
            if res_d[col] == name:
                cl_other = get_cl_data_for_name(res_d[col_other], cl_data)
                final_cl_other = [cl_other[i] for i in the_other_range]

                if is_lo:
                    pre_data.append([cl[CL_POS_COL], final_cl, \
                                     cl_other[CL_POS_COL], final_cl_other, \
                                     res_d[RES_ELT_COL]])                 
                else:
                    pre_data.append([cl_other[CL_POS_COL], final_cl_other, \
                                     cl[CL_POS_COL], final_cl, \
                                     res_d[RES_ELT_COL]])                                      
                                               
        return pre_data, cl[CL_POS_COL], final_cl
    
    def _get_val_index(self, values, order, sort_values, name):
        
        try:
            i = order.index(name)
            sort_values.append(values[i])
        except ValueError:
            sort_values.append(0)

    def _sort_pre_values(self, values, order):
        
        sort_values = []
        
        self._get_val_index(values, order, sort_values, FIRST_NAME)
        self._get_val_index(values, order, sort_values, SECOND_NAME)
        self._get_val_index(values, order, sort_values, THIRD_NAME)                
                    
        return sort_values        
    
    def _get_pre_values(self, data, lo_pos, lo_cl, vi_pos, vi_cl):
        
        tr_data = []
        classes_data = []
        
        for d in data:            
            new_d = []            
            new_d.append(int(d[0]) - int(d[2]))
            new_d.extend(d[1])
            new_d.extend(d[3])
            
            tr_data.append(new_d)
            
            classes_data.extend([d[4]])
            
        prd_data = [ int(lo_pos) - int(vi_pos) ]
        prd_data.extend(lo_cl)
        prd_data.extend(vi_cl)
        
        np_tr_data = np.matrix(tr_data)
        np_classes_data = np.array(classes_data)
        np_prd_data = np.matrix(prd_data)
            
        rf = RandomForestClassifier(n_estimators = RF_NUM_ESTIMATORS, 
                                     random_state = RF_SEED)  

        rf.fit(np_tr_data, np_classes_data)      

        prd = rf.predict_proba(np_prd_data)

        sort_pre_val = self._sort_pre_values(prd[0],
                                             np.ndarray.tolist(rf.classes_))
        
        return [ int(100 * x) for x in sort_pre_val]
    
    def _generate(self):  
        
        pre_file_name = PRE_FILE_NAME_PREFIX + self._index + INPUT_FILE_NAME_EXT
        
        self._pre = read_input_file(pre_file_name)
        
        if not len(self._pre):
        
            b1_res = read_res_file(B1_RES_FILE)
            a2_res = read_res_file(A2_RES_FILE)
            
            for k in self._k:
                if k[TYPE_COL] == TYPE_1_COL:  
                    cl_data = self._b1
                    res_data = b1_res
                else:
                    cl_data = self._a2
                    res_data = a2_res
                    
                lo_data, lo_pos, lo_cl = \
                    self._get_data_for_pre(k[NAME_LO_COL], cl_data, res_data, 
                                           True)     
                
                vi_data, vi_pos, vi_cl = \
                    self._get_data_for_pre(k[NAME_VI_COL], cl_data, res_data, 
                                           False)
                    
                print "Predicting: %s - %s" % (k[NAME_LO_COL], k[NAME_VI_COL])
                
                lo_pre = self._get_pre_values(lo_data, lo_pos, lo_cl, vi_pos, 
                                              vi_cl)             
    
                vi_pre = self._get_pre_values(vi_data, lo_pos, lo_cl, vi_pos, 
                                              vi_cl)
                
                self._pre.append(combine_lo_vi(lo_pre, vi_pre))
                
            if self.generated:
                save_data_to_csv(pre_file_name, self._pre)
            
    @property
    def pre(self):
        return self._pre
    
    @property
    def generated(self):
        return len(self._pre)