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

"""Composition of different data.
"""

import csv
import numpy as np
from ctes import *
from kscraping import *

from storage import Storage
from propre import ProPre

class ComposeData(object):
    
    def __init__(self, index, stor):
  
        self._index = index
        self._stor = stor
        self._mean = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
        self._max_sign = [['' for _ in range(NUM_EXT_SOURCES)] for _ in range(NUM_ROWS)]
        self._signs = ['' for _ in range(NUM_ROWS)]
        self._lo_res = []
        self._vi_res = []
        
    # ------------------------------------- Getting data from CL.     
    def _get_data_from_cl(self, cl_data, name):
        
        data = []

        for i, cdat in enumerate(cl_data):
            if cdat[CL_NAME_COL] == name:
                return cdat[:]
                
        return data        
    
    def get_p_data_from_b1(self, name, as_lo = True):
        
        data = self._get_data_from_cl(self._stor.b1, name)
        
        if as_lo:
            return [int(data[i]) for i in LO_P_RANGE]
        else:
            return [int(data[i]) for i in VI_P_RANGE] 
    
    def get_p_data_from_a2(self, name, as_lo = True):
        
        data = self._get_data_from_cl(self._stor.a2, name)   
        c
        if as_lo:
            return [int(data[i]) for i in LO_P_RANGE]
        else:
            return [int(data[i]) for i in VI_P_RANGE] 
            
    # ------------------------------------- Calculations.
    def _fill_data(self):
        
        for i in range(NUM_ROWS):
            
            # Values to calculate the maximum values of each block.
            max_sign_val = [0] * NUM_EXT_SOURCES
            max_sign_str = [''] * NUM_EXT_SOURCES
            
            for j in range(NUM_COLS):
                
                # Calculate a mean of the data scraped.                
                val_np_arr = np.array([int(self._stor.lm[i][j]), \
                                      int(self._stor._ve[i][j]), \
                                      int(self._stor._qu[i][j]), \
                                      int(self._stor._q1[i][j]), \
                                      int(self._stor._cq[i][j])]) 
                                 
                self._mean[i][j] = np.mean(val_np_arr)
                                
                curr_sign_max = CURRENT_MAX[j]
                
                for k in range(NUM_EXT_SOURCES_FOR_MEAN):
                    if val_np_arr[k] > max_sign_val[k]:
                        max_sign_val[k] = val_np_arr[k]
                        max_sign_str[k] = curr_sign_max   
                        
            # A set of the maximum values.            
            max_sign_set = set()                                                                                 
            
            for k in range(NUM_EXT_SOURCES):
                self._max_sign[i][k] = max_sign_str[k] 
                max_sign_set.add(max_sign_str[k])
                         
            # Fill summary of highest values.
            self._signs[i] = ''.join(list(max_sign_set))
            
            # Get res for each name.                           
            if self._stor.k[i][TYPE_COL] == TYPE_1_COL:
                self._lo_res = self.get_p_data_from_b1(self._stor.k[i][NAME_LO_COL])
                self._vi_res = self.get_p_data_from_b1(self._stor.k[i][NAME_VI_COL], False)
            else:
                self._lo_res = self.get_p_data_from_a2(self._stor.k[i][NAME_LO_COL])
                self._vi_res = self.get_p_data_from_a2(self._stor.k[i][NAME_VI_COL], False) 

    def _calculate(self): 
        
        # Calculate Ps depending on the data for each one.
        for i in range(NUM_ROWS): 
            
            p_lo = ProPre.calculate_pro_data(self._lo_res[i])      
        
            p_vi = ProPre.calculate_pro_data(self._vi_res[i])
                
            p_lo_vi = ProPre.combine_lo_vi(p_lo, p_vi)
            
            p_final = ProPre.calc_final_p(p_lo_vi, self._stor.pre[i], p_type)             
                
            self._stor.p.append([p_final[0], p_final[1], p_final[2]])                                                   
               
    def _write_data(self):
        
        output_file_name = PREFIX_OUTPUT_FILE_NAME + \
            self._scr.index + OUTPUT_FILE_NAME_EXT        
        
        print "Saving results in: %s" % output_file_name    
                    
        with open(output_file_name, "w") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=CSV_DELIMITER)            
            
            for p in self._stor.p:
                csvwriter.writerow(p)

    def get_final_data(self):
        
        final_data = []
        
        for i in range(NUM_ROWS):
            final_data.append([self._stor.k[i][DAT_LI_COL]] + self._stor.p[i])
        
        return final_data
                         
    def compose_all_data(self):
        
        # Fill with source data from index.
        self._fill_data()
        
        # Calculations.
        self._calculate()
        
        # Write results.  
        self._write_data()
        
    def compose_own_data(self):    
        
        # Calculations.
        self._calculate()
        
        # Write results.  
        self._write_data()        