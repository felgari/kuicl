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

"""Script to report results.
"""

import sys
import csv

from ctes import *

def read_file(file_name):
    
    data = []
    
    try:
        with open(file_name, "rb") as fr:
            
            reader = csv.reader(fr, delimiter=',', quotechar='"')        
            
            for row in reader:   
                 
                data.append(row)
                
        print "Read %d from %s" % (len(data), file_name)
                
    except csv.Error:
        print "Error reading data from CSV file: '%s'" % file_name 
                
    except IOError:
        print "Error reading CSV file: '%s'" % file_name     
    
    return data

def get_matchings(name, data, is_first):
    
    mat = []
    
    for d in data:
        if is_first:
            data_name = d[R_NAME_1_COL]
        else:
            data_name = d[R_NAME_2_COL]
            
        if name == data_name:
            mat.append([d[i] for i in R_COLS])
            
    return mat

def process_k(k_data, b1_data, a2_data, index):
    
    out_file_name = REP_OUT_FILE_PREFIX + index + REP_OUT_FILE_EXT
    
    print "Saving to file: %s" % out_file_name
    
    try:    
    
        with open(out_file_name, 'w') as f: 
        
            for k_elt in k_data:
                elt_type = k_elt[K_TYPE_COL]
                k_name_1 = k_elt[K_NAME_1_COL]
                k_name_2 = k_elt[K_NAME_2_COL]
                
                if elt_type == TYPE_1_COL:
                    data = b1_data
                else:
                    data = a2_data
                    
                mat1 = get_matchings(k_name_1, data, True)
                mat2 = get_matchings(k_name_2, data, False)
                
                f.write("%s\n" % GEN_SEP)
                f.write("-> %s - %s\n" % (k_name_1, k_name_2))
                f.write("%s\n" % FIRST_SEP)
                for m in mat1:
                    f.write("%s\n" % m)
                f.write("%s\n" % SECOND_SEP)
                for m in mat2:
                    f.write("%s\n" % m)
                    
    except IOError as ioe:
         print "Error saving file: '%s'" % out_file_name                    

def main(index):
    
    b1_data = read_file(B1_RES_FILE)    
    
    a2_data = read_file(A2_RES_FILE)
    
    index_file_name = K_FILE_NAME_PREFIX + index + INPUT_FILE_NAME_EXT
    
    k_data = read_file(index_file_name)    
    
    process_k(k_data, b1_data, a2_data, index)

if __name__ == "__main__":
    
    if len(sys.argv) == NUM_ARGS:
        sys.exit(main(sys.argv[1]))
    else:
        print "The index is needed as argument."