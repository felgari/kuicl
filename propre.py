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
import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from ctes import *
from kfiles import *
from storage import Storage

class ProPre(object):
    
    def __init__(self, index, stor):
        """Constructor.                        
        """    
        
        self._index = index
        self._stor = stor
            
    @staticmethod
    def get_cl_data_for_name(name, cl_data):
        
        row = []
        
        for cl_d in cl_data:
            if cl_d[CL_NAME_COL] == name:
                row = cl_d
                break
            
        return row
    
    @staticmethod
    def calculate_pro_data(data):
        
        if int(sum(data)):
            data_sum = float(sum(data))
        else:
            data_sum = 1.0
        
        return [ 100.0 * float(d) / data_sum for d in data ]
    
    @staticmethod
    def combine_lo_vi(lo_data, vi_data):
        
        return [int(round(LO_WEIGHT * lo_data[FIRST_LO] + 
                          vi_data[FIRST_VI] * VI_WEIGHT)), 
                int(round(LO_WEIGHT * lo_data[SECOND_LO] +
                          vi_data[SECOND_VI] * VI_WEIGHT)),
                int(round(LO_WEIGHT * lo_data[THIRD_LO] +
                          vi_data[THIRD_VI] * VI_WEIGHT))]    
        
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
            
        cl = ProPre.get_cl_data_for_name(name, cl_data)
        final_cl = [cl[i] for i in the_range]
        
        for res_d in res_data:       
            if res_d[col] == name:
                cl_other = ProPre.get_cl_data_for_name(res_d[col_other], cl_data)
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
    
    @property
    def index_data(self):
        return self._index
    
    @property
    def pro_data(self):
        return self._pro
    
    @property
    def pre_data(self):
        return self._pre

    @staticmethod
    def get_data_for_pro(k, cl_data, is_lo):
        
        if is_lo:
            name_col = NAME_LO_COL
            p_range = LO_P_RANGE
        else:
            name_col = NAME_VI_COL
            p_range = VI_P_RANGE
                    
        data_from_name = ProPre.get_cl_data_for_name(k[name_col], cl_data)
        
        pos = int(data_from_name[CL_POS_COL])
        
        data_from_range = [int(data_from_name[i]) for i in p_range]
        
        data_for_calc = ProPre.calculate_pro_data(data_from_range)
        
        return data_for_calc, pos

    def generate_pro_data(self):
        
        for k in self._stor.k:             
                   
            if k[TYPE_COL] == TYPE_1_COL:  
                cl_data = self._stor.b1
            else:
                cl_data = self._stor.a2
                
            calc_lo_data, lo_pos = ProPre.get_data_for_pro(k, cl_data, True)         
            
            calc_vi_data, vi_pos = ProPre.get_data_for_pro(k, cl_data, False) 
            
            self._stor.pro.append(ProPre.combine_lo_vi(calc_lo_data, calc_vi_data))
            
        out_file_name = PRO_FILE_NAME_PREFIX + self._index + INPUT_FILE_NAME_EXT
        
        save_data_to_csv(out_file_name, self._stor.pro)
    
    def generate_pre_data(self):  
        
        b1_res = read_res_file(B1_RES_FILE)
        a2_res = read_res_file(A2_RES_FILE)
        
        for k in self._stor.k:
            if k[TYPE_COL] == TYPE_1_COL:  
                cl_data = self._stor.b1
                res_data = b1_res
            else:
                cl_data = self._stor.a2
                res_data = a2_res
                
            lo_data, lo_pos, lo_cl = \
                self._get_data_for_pre(k[NAME_LO_COL], cl_data, res_data, True)     
            
            vi_data, vi_pos, vi_cl = \
                self._get_data_for_pre(k[NAME_VI_COL], cl_data, res_data, False)
                
            print "Predicting: %s - %s" % (k[NAME_LO_COL], k[NAME_VI_COL])
            
            lo_pre = self._get_pre_values(lo_data, lo_pos, lo_cl, vi_pos, vi_cl)             

            vi_pre = self._get_pre_values(vi_data, lo_pos, lo_cl, vi_pos, vi_cl)
            
            self._stor.pre.append(ProPre.combine_lo_vi(lo_pre, vi_pre))
            
        out_file_name = PRE_FILE_NAME_PREFIX + self._index + INPUT_FILE_NAME_EXT
            
        save_data_to_csv(out_file_name, self._stor.pre)            
