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
from model import Model, read_mdl_file
from kscrap import KScrap
from kfiles import read_input_file, read_res_file, save_data_to_csv
from putil import combine_lo_vi, get_cl_data_for_name

class Pre(object):
    
    _mdls = read_mdl_file()
    
    def __init__(self, index, k, b1, a2, force_calc = False):
        """Constructor.                        
        """    
        
        self._index = index
        self._pre = []
        self._k = k
        self._b1 = b1
        self._a2 = a2
        
        try:
            self._generate(force_calc)
        except ZeroDivisionError:
            self._pre = []
        
    @classmethod
    def get_mdl(cls, name):
        
        for m in cls._mdls:
            if m.name == name:
                return m
                
        return None
    
    @staticmethod
    def get_data_for_pre(name, cl_data, res_data, is_lo):
        
        pre_data = []
        
        if is_lo:
            col = R_NAME_1_COL
            col_other = R_NAME_2_COL
            the_range = LO_D_RANGE
            the_other_range = VI_D_RANGE
        else:
            col = R_NAME_2_COL
            col_other = R_NAME_1_COL  
            the_range = VI_D_RANGE
            the_other_range = LO_D_RANGE
            
        cl = get_cl_data_for_name(name, cl_data)
        final_cl = [cl[i] for i in the_range]
        
        for res_d in res_data:       
            if res_d[col] == name:
                cl_other = get_cl_data_for_name(res_d[col_other], cl_data)
                final_cl_other = [cl_other[i] for i in the_other_range]
                
                new_row = [ cl_other[CL_POS_COL] ]
                new_row.extend(final_cl_other)
                new_row.extend([res_d[RES_ELT_COL]])

                pre_data.append(new_row)                          
                                               
        return pre_data, [cl[CL_POS_COL]] + final_cl
    
    @staticmethod
    def _get_val_index(values, order, sort_values, name):
        
        try:
            i = order.index(name)
            sort_values.append(values[i])
        except ValueError:
            sort_values.append(0)

    @staticmethod
    def _sort_pre_values(values, order):
        
        sort_values = []
        
        Pre._get_val_index(values, order, sort_values, FIRST_NAME)
        Pre._get_val_index(values, order, sort_values, SECOND_NAME)
        Pre._get_val_index(values, order, sort_values, THIRD_NAME)                
                    
        return sort_values        
    
    @staticmethod
    def get_pre_values(src_data, target_data, mdls):
        
        source_data = []
        classes_data = []
        
        for d in src_data:            
            source_data.append(d[:-1])
            
            classes_data.extend([d[-1]])
        
        np_src_data = np.matrix(source_data)
        np_classes_data = np.array(classes_data)
        np_prd_data = np.matrix(target_data)
        
        if mdls:
            cl = CLS[mdls[0]]
        else:
            cl = RandomForestClassifier(n_estimators = RF_NUM_ESTIMATORS,
                                        random_state = RF_SEED)  

        if len(np_classes_data) == len(CLASSES_PRE):
            cl.fit(np_src_data, np_classes_data)
            
            prd = cl.predict_proba(np_prd_data)
    
            sort_pre_val = Pre._sort_pre_values(prd[0],
                                                np.ndarray.tolist(cl.classes_))
        else:
            sort_pre_val = [0.0] * len(CLASSES_PRE)
        
        return [ int(100 * x) for x in sort_pre_val]
    
    def _generate(self, force_calc):  
        
        pre_file_name = PRE_FILE_NAME_PREFIX + self._index + INPUT_FILE_NAME_EXT
        
        if not force_calc:
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
                    
                lo_data, lo_target_data = Pre.get_data_for_pre(k[NAME_LO_COL], 
                                                               cl_data,
                                                               res_data, True) 
                    
                lo_mdl = Pre.get_mdl(k[NAME_LO_COL]) 
                
                vi_data, vi_target_data = Pre.get_data_for_pre(k[NAME_VI_COL], 
                                                               cl_data,
                                                               res_data, False)
                    
                vi_mdl = Pre.get_mdl(k[NAME_VI_COL]) 
                    
                print "Predicting: %s - %s" % (k[NAME_LO_COL], k[NAME_VI_COL])
                
                lo_pre = self.get_pre_values(lo_data, lo_target_data, 
                                             lo_mdl.lo_mdls)             
    
                vi_pre = self.get_pre_values(vi_data, vi_target_data, 
                                             vi_mdl.vi_mdls)
                
                self._pre.append(combine_lo_vi(lo_pre, vi_pre))
                
            if self.generated:
                save_data_to_csv(pre_file_name, self._pre)
            
    @property
    def pre(self):
        return self._pre
    
    @property
    def mdls(self):
        return self._mdls
    
    @property
    def generated(self):
        return len(self._pre) > 0