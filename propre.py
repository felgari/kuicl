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
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

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
            
    def _get_cl_data_for_name(self, name, cl_data):
        
        row = []
        
        for cl_d in cl_data:
            if cl_d[CL_NAME_COL] == name:
                row = cl_d
                break
            
        return row
    
    def _calculate_pro_data(self, data):
        
        final_data = []
        
        data_sum = float(sum(data))
        
        for d in data:
            final_data.append(100 * float(d) / data_sum)
        
        return final_data
    
    def _combine_lo_vi(self, lo_data, vi_data):
        
        return [int(round(LO_WEIGHT * lo_data[FIRST_LO] + \
                          vi_data[FIRST_VI] * VI_WEIGHT)), 
            int(round(LO_WEIGHT * lo_data[SECOND_LO] + \
                    vi_data[SECOND_VI] * VI_WEIGHT)), 
            int(round(LO_WEIGHT * lo_data[THIRD_LO] + \
                    vi_data[THIRD_VI] * VI_WEIGHT))]    
    
    def _save_data(self, out_file_name, data):
        
        f = open(out_file_name,'w')
        
        for d in data:
            
            f.write("%s\n" % CSV_DELIMITER.join(str(i) for i in d))
        
        f.close()   
        
        print "File saved: %s" % out_file_name   
        
    def _read_res_file(self, file_name):
        
        print "Reading ref file: %s" % file_name
                    
        res_data = []
    
        try:
            with open(file_name, 'rb') as f:
                
                reader = csv.reader(f)
            
                for row in reader:
                    
                    # Ignore header.
                    if row[J_COL_RES].isdigit():
                    
                        red_row = [row[i] for i in RES_ELEMENTS]
                        
                        res_data.append(red_row)
            
        except csv.Error:
            print "ERROR: reading file %s" % file_name
        except IOError:
            print "ERROR: reading file %s" % file_name
            
        if len(res_data) > 0:
            print "Read: %dx%d" % (len(res_data), len(res_data[0]))
                
        return res_data        
    
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
        
        cl = self._get_cl_data_for_name(name, cl_data)
        final_cl = [cl[i] for i in the_range]
        
        for res_d in res_data:       
            if res_d[col] == name:
                cl_other = self._get_cl_data_for_name(res_d[col_other], cl_data)
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
        
        #rf = AdaBoostClassifier()
        #rf = SVC(gamma=2, C=1, probability=True)
        #rf = GaussianNB()
        #rf = KNeighborsClassifier(12)

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

    def generate_pro_data(self):
        
        for k in self._k_data:
            if k[TYPE_COL] == TYPE_1_COL:  
                cl_data = self._b1_data
            else:
                cl_data = self._a2_data
                
            data = self._get_cl_data_for_name(k[NAME_LO_COL], cl_data)
                
            lo_data = [int(data[i]) for i in LO_P_RANGE]
            
            calc_lo_data = self._calculate_pro_data(lo_data)         
            
            data = self._get_cl_data_for_name(k[NAME_VI_COL], cl_data)
            
            vi_data = [int(data[i]) for i in VI_P_RANGE]
            
            calc_vi_data = self._calculate_pro_data(vi_data)
            
            self._pro.append(self._combine_lo_vi(calc_lo_data, calc_vi_data))
            
        out_file_name = PRO_FILE_NAME_PREFIX + self._index + INPUT_FILE_NAME_EXT
        
        self._save_data(out_file_name, self._pro)
        
        return self._pro
    
    def generate_pre_data(self):  
        
        b1_res = self._read_res_file(B1_RES_FILE)
        a2_res = self._read_res_file(A2_RES_FILE)
        
        for k in self._k_data:
            if k[TYPE_COL] == TYPE_1_COL:  
                cl_data = self._b1_data
                res_data = b1_res
            else:
                cl_data = self._a2_data
                res_data = a2_res
                
            lo_data, lo_pos, lo_cl = \
                self._get_data_for_pre(k[NAME_LO_COL], cl_data, res_data, True)     
            
            vi_data, vi_pos, vi_cl = \
                self._get_data_for_pre(k[NAME_VI_COL], cl_data, res_data, False)
                
            print "Predicting: %s - %s" % (k[NAME_LO_COL], k[NAME_VI_COL])
            
            lo_pre = self._get_pre_values(lo_data, lo_pos, lo_cl, vi_pos, vi_cl)             

            vi_pre = self._get_pre_values(vi_data, lo_pos, lo_cl, vi_pos, vi_cl)
            
            self._pre.append(self._combine_lo_vi(lo_pre, vi_pre))
            
        out_file_name = PRE_FILE_NAME_PREFIX + self._index + INPUT_FILE_NAME_EXT
            
        self._save_data(out_file_name, self._pre)            

        return self._pre
