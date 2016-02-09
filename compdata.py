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

import numpy as np
from ctes import *
from qscraping import *

class ComposeData(object):
    
    def __init__(self, scr, index_data, pro_data, pre_data):
  
        self._scr = scr
        self._index_data = index_data
        self._pro_data = pro_data
        self._pre_data = pre_data
  
        self._compdata = \
            [[0 for _ in range(TOTAL_NUM_COLS)] for _ in range(NUM_ROWS)]
            
    def _fill_data(self):
        
        len_index = len(self._index_data[0])

        for i in range(NUM_ROWS):
            for j in range(len_index):
                self._compdata[i][j] = self._index_data[i][j]
        
        pre_base = len_index + len(self._pro_data[0])
        lm_base = pre_base + len(self._pre_data[0])
        ve_base = lm_base + len(self._scr.lm_data[0])
        qu_base = ve_base + len(self._scr.ve_data[0])
        q1_base = qu_base + len(self._scr.qu_data[0]) 
        med_base = q1_base + len(self._scr.q1_data[0])               

        for i in range(NUM_ROWS):
            
            max_val = [0] * NUM_EXT_SOURCES
            max_str = [''] * NUM_EXT_SOURCES

            max_set = set()
            
            for j in range(NUM_COLS):
                
                # Fill with data scraped. 
                self._compdata[i][j + len_index] = self._pro_data[i][j]
                self._compdata[i][j + pre_base] = self._pre_data[i][j]
                self._compdata[i][j + lm_base] = self._src.lm_data[i][j]
                self._compdata[i][j + ve_base] = self._src._ve_data[i][j]
                self._compdata[i][j + qu_base] = self._src._qu_data[i][j]
                self._compdata[i][j + q1_base] = self._src._q1_data[i][j]
                
                # Calculate a mean of the data scraped for this column.                
                np_arr = np.array([self._pro_data[i][j], \
                                  self._pre_data[i][j], \
                                  self._src.lm_data[i][j], \
                                  self._src._ve_data[i][j], \
                                  self._src._qu_data[i][j], \
                                  self._src._q1_data[i][j]])     
                                 
                self._compdata[i][j + med_base] = np.mean(np_arr)
                                
                curr_max = CURRENT_MAX[j]
                
                for i in range(NUM_EXT_SOURCES):
                    if np_arr[i] > max_val[i]:
                        max_val[i] = np_arr[i]
                        max_str[i] = curr_max   
                        max_set.add(curr_max)                                                                 
            
            # Fill highest value of each external.        
            max_base = med_base + NUM_COLS   
            
            for i in range(NUM_EXT_SOURCES):
                self._compdata[i][NUM_COLS + max_base + i] = max_str[i] 
                         
            # Fill summary of highest values.
            self._compdata[i][NUM_COLS + max_base + NUM_EXT_SOURCES] = \
                ''.join(list(max_set))
            
            # Fill data for each name.
            name_lo_data = []
            name_vi_data = []
                
            if self._compdata[i][TYPE_COL] == TYPE_1_COL:
                name_lo_data = self._scr.get_data_from_b1(self._compdata[i][NAME_LO_COL])
                name_vi_data = self._scr.get_data_from_b1(self._compdata[i][NAME_VI_COL])
            else:
                name_lo_data = self._scr.get_data_from_a2(self._compdata[i][NAME_LO_COL])
                name_vi_data = self._scr.get_data_from_a2(self._compdata[i][NAME_VI_COL])
                
            if len(name_lo_data) < NAME_DATA_LEN:
                print "ERROR: Retrieving data for: %s" % self._compdata[i][NAME_LO_COL] 
                
            if len(name_vi_data) < NAME_DATA_LEN:
                print "ERROR: Retrieving data for: %s" % self._compdata[i][NAME_VI_COL]                 
                
            for k in range(len(name_lo_data)):
                self._compdata[i][k + MAT_FIRST_COL] = int(name_lo_data[k])
                
            for k in range(len(name_vi_data)):
                self._compdata[i][k + MAT_FIRST_COL + NAME_DATA_LEN] = int(name_vi_data[k])                            
        
    def _calculate(self):        
        
        # Calculate Ps depending on the data for each one.
        for i in range(NUM_ROWS):
            p_with = 1
            
            if self._compdata[i][TYPE_COL] == TYPE_1_COL: 
                p_with = P_WITH_B1
            else:
                p_with = P_WITH_A2
                
            p_lo_sum = 0
            p_vi_sum = 0                
                
            for k in range(NAME_DATA_LEN):
                p_lo_sum += self._compdata[i][MAT_FIRST_COL + k]
                
                p_vi_sum += self._compdata[i][MAT_FIRST_COL + NAME_DATA_LEN + k]

            p_lo_1 = self._compdata[i][MAT_FIRST_COL] / p_lo_sum
            p_lo_2 = self._compdata[i][MAT_FIRST_COL + 1] / p_lo_sum
            p_lo_3 = self._compdata[i][MAT_FIRST_COL + 2] / p_lo_sum
            
            p_vi_1 = self._compdata[i][MAT_FIRST_COL + NAME_DATA_LEN] / p_vi_sum
            p_vi_2 = self._compdata[i][MAT_FIRST_COL + NAME_DATA_LEN + 1] / p_vi_sum
            p_vi_3 = self._compdata[i][MAT_FIRST_COL + NAME_DATA_LEN + 2] / p_vi_sum 
            
            p_13 = p_lo_1 * p_vi_3
            p_22 = p_lo_2 * p_vi_2
            p_31 = p_lo_3 * p_vi_1   
                
            p_1 = p_13 * self._compdata[i][AVE_FIRST_COL] / p_with
            p_2 = p_22 * self._compdata[i][AVE_FIRST_COL + 1] / p_with                     
            p_3 = p_31 * self._compdata[i][AVE_FIRST_COL + 2] / p_with  
            
            p_sum = p_1 + p_2 + p_3
            
            p_1_final = 100 * p_1 / p_sum
            p_2_final = 100 * p_2 / p_sum
            p_3_final = 100 * p_3 / p_sum  
            
            self._compdata[i][ST_FIRST_COL] = p_1_final
            self._compdata[i][ST_FIRST_COL + 1] = p_2_final  
            self._compdata[i][ST_FIRST_COL + 2] = p_3_final 
            
            # Set the values over the minimum.
            p_dict = { MAX_IS_FIRST : p_1_final, \
                      MAX_IS_SECOND : p_2_final, \
                      MAX_IS_THIRD: p_3_final }
            
            keys_sorted = sorted(p_dict) 
            
            val = keys_sorted[0]   
            
            for i in [1,2]:             
                if p_dict[keys_sorted[i]] > MIN_PER:   
                    val += keys_sorted[i]                   
            
            self._compdata[i][ST_FIRST_COL + 3] = val  
        
    def _write_data(self):
        
        output_file_name = PREFIX_OUTPUT_FILE_NAME + \
            self._scr.index + OUTPUT_FILE_NAME_EXT
                    
        with open(output_file_name, "w") as fw:
            
            for i in range(len(self._compdata)):
                fw.write(CSV_DELIMITER.join(self._compdata[i]))
                         
    def compose(self):
        
        # Fill with source data from index.
        self._fill_data()
        
        # Calculations.
        self._calculate()
        
        # Write results.  
        self._write_data()      