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

"""Script to do something.
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

def calc_ap_base(data):
    """Get the ap for each row. """
    
    base = []
    
    for d in data:        
        values = d[AP_FIRST_P_COL:]
        
        maxi = max(values)
        index_maxi = values.index(maxi)
        
        mini = min(values)
        index_mini = values.index(mini)
        
        if maxi >= HIST_MAX_P:
            new_base = CURRENT_MAX[index_maxi]         
        elif mini <= HIST_MIN_P:
            indexes = [0, 1, 2]
            indexes.remove(index_maxi)
            indexes.remove(index_mini)
            
            new_base = CURRENT_MAX[index_maxi] + CURRENT_MAX[indexes[0]]
        else:               
            if d[AP_LI_COL] == AP_LI_TYPE_1:
                new_base = CURRENT_MAX[index_maxi] + CURRENT_MAX[index_mini]
            else:    
                indexes = [0, 1, 2]
                indexes.remove(index_maxi)
                indexes.remove(index_mini)
                
                new_base = CURRENT_MAX[index_maxi] + CURRENT_MAX[indexes[0]] 
                
        try:
            base.append(AP_CONV[new_base])
        except KeyError:
            base.append(new_base)
    
    return base

def complementary(data):
    
    comp = []
    
    for d in data:
        comp.append(COMPLEMENT[d])
    
    return comp

def write_data(ap_data, comp_ap_data, index):
    
    out_file_name = AP_FILE_PREFIX + index + AP_FILE_EXT
    
    print "Saving results in: %s" % out_file_name    
                
    with open(out_file_name, "wb") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=CSV_DELIMITER)            
        
        for i in range(len(ap_data)):
            row = [ ap_data[i], comp_ap_data[i] ]
            csvwriter.writerow(row)   
            
def calculate_ap(data, index):
    
    ap_data = calc_ap_base(data)
    
    comp_ap_data = complementary(ap_data)
    
    write_data(ap_data, comp_ap_data, index)    
     
def main(index):
    """Main function.

    """    

    data = read_data(index)
                
    calculate_ap(data, index)
        
    print "Program finished."
    
    return 0

# Where all begins ...
if __name__ == "__main__":
    
    if len(sys.argv) == NUM_ARGS:
        sys.exit(main(sys.argv[1]))
    else:
        print "An index must be provided to read input file."    