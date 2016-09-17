#!/usr/bin/env python
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

"""Calculation of ap.
""" 

import sys
import csv
import operator

from ctes import *

NUM_ARGS = 2

def read_data(index):
    
    data = []
    
    file_name = PREFIX_OUTPUT_FILE_NAME + index + OUTPUT_FILE_NAME_EXT
    
    with open(file_name, 'rb') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                
                data.append([int(float(row[i])) for i in COLS_FOR_AP_FROM_FILE])
        
        except csv.Error:
            print "ERROR: reading file %s" % file_name
            
    return data

def get_second_index(index_maxi, index_mini):
        
    indexes = [0, 1, 2]
    
    indexes.remove(index_maxi)
    indexes.remove(index_mini)   
    
    return indexes[0]

def calc_ap_base(data):
    """Get the ap for each row. """
    
    print "Calculating ap ..."
    
    base = []
    
    for d in data:       
        values = [ int(x) for x in d[AP_FIRST_P_COL:]]
        
        if sum(values) > AP_MIN_PERCENT:
        
            maxi = max(values)
            index_maxi = values.index(maxi)
            
            mini = min(values)
            index_mini = values.index(mini)
            
            index_mid = get_second_index(index_maxi, index_mini)
            
            if maxi >= HIST_MAX_P: # One clear option
                new_base = CURRENT_MAX[index_maxi]           
            elif mini <= HIST_MIN_P: # Two options
                if d[AP_LI_COL] == AP_LI_TYPE_1:
                    new_base = CURRENT_MAX[index_maxi]
                else:
                    new_base = CURRENT_MAX[index_maxi] + CURRENT_MAX[index_mid]
            else: # Three options.                           
                new_base = CURRENT_MAX[index_maxi] + CURRENT_MAX[index_mid] 
                    
            if new_base == MAX_IS_SECOND:
                if mini > AP_MIN_VAL_P:
                    new_base = NAMES_AP_STR
                else:
                    new_base += CURRENT_MAX[index_mid]
                    
            try:
                base.append(AP_CONV[new_base])
            except KeyError:
                base.append(new_base)
                
        else:
            base.append(MAX_IS_FIRST)
            
    return base

def complementary(data):
    
    comp = []
    
    for d in data:
        comp.append(COMPLEMENT[d])
    
    return comp

def write_data(ap_data, comp_ap_data, index):
    
    out_file_name = AP_FILE_PREFIX + str(index) + AP_FILE_EXT
    
    print "Saving results in: %s" % out_file_name    
                
    with open(out_file_name, "wb") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=CSV_DELIMITER)            
        
        for i, ap_d in enumerate(ap_data):
            row = [ ap_d, comp_ap_data[i] ]
            csvwriter.writerow(row)   
            
def calculate_ap(data, index):
    
    ap_data = calc_ap_base(data)
    
    comp_ap_data = complementary(ap_data)
    
    write_data(ap_data, comp_ap_data, index)    
    
    return ap_data, comp_ap_data

def calc_stats(data, ap_data):
    
    st = [0.0] * len(data)
    
    for i, d in enumerate(data):
        ap = ap_data[i]
                        
        for j, n in enumerate(NAMES_AP):            
            if ap.find(n) >= 0:
                st[i] += d[AP_FIRST_P_COL + j] / 100.0
                
    prob = []
        
    for n in range(AP_STAT_TIMES):
        prob.append(int(reduce(operator.mul, st, 1) * 100))
        st.remove(min(st))
        
    print "Prob is: %s" % prob
     
def main(index):
    """Main function.

    """    

    data = read_data(index)
                
    ap_data, comp_ap_data = calculate_ap(data, index)
    
    calc_stats(data, ap_data)   
        
    print "Program finished."
    
    return 0

# Where all begins ...
if __name__ == "__main__":
    
    if len(sys.argv) == NUM_ARGS:
        sys.exit(main(sys.argv[1]))
    else:
        print "An index must be provided to read input file."    