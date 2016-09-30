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

"""Common functions to read and write files.
"""

import csv

from ctes import *

def read_input_file(input_file_name):
             
    print "Reading local file: %s" % input_file_name
                
    data = []

    try:
        with open(input_file_name, 'rb') as f:
            
            reader = csv.reader(f)
        
            for row in reader:
                if row[0].isdigit():
                    data.append(row)
                else:
                    print "Ignoring line in file %s, maybe a header: %s" % \
                        (input_file_name, row)
        
    except csv.Error:
        print "ERROR: reading file %s" % input_file_name
        data = []
    except IOError:
        print "ERROR: reading file %s" % input_file_name
        data = []
        
    if len(data):
        print "Read: %dx%d" % (len(data), len(data[0]))
    else:
        print "ERROR: No data read."
            
    return data
    
def read_res_file(file_name):
    
    print "Reading res file: %s" % file_name
                
    res_data = []

    try:
        with open(file_name, 'rb') as f:
            
            reader = csv.reader(f)
        
            for row in reader:
                
                # Ignore header.
                if row[R_J_COL].isdigit():
                
                    red_row = [row[i] for i in RES_ELEMENTS]
                    
                    res_data.append(red_row)
        
    except csv.Error:
        print "ERROR: reading file %s" % file_name
    except IOError:
        print "ERROR: reading file %s" % file_name
        
    if len(res_data):
        print "Read: %dx%d" % (len(res_data), len(res_data[0]))
            
    return res_data

def extract_list_text(txt, num):
    
    the_list = []
    
    pos = txt.find(SCR_TXT_DELIM)
    txt_red = txt[pos + 1:].strip()
    
    lst_from_txt = txt_red.translate(None, "[],\'").split()

    n = 0
    new_list = []
    for elt in lst_from_txt:
        if elt.isdigit():
            new_list.append(int(elt))
        else:
            new_list.append(elt)
            
        n += 1
        
        if n == num:
            the_list.append(new_list)
            new_list = []
            n = 0
    
    return the_list   

def save_data_to_csv(out_file_name, data):
    
    try:

        with open(out_file_name, 'w') as f:        
            for d in data:            
                f.write("%s\n" % CSV_DELIMITER.join(str(e) for e in d))
        
        print "File saved: %s" % out_file_name
           
    except IOError as ioe:
         print "Error saving file: '%s'" % out_file_name
         
def save_all(k, extm, p, p_rf, ap_rf, p_nn, ap_nn, index):
    
    out_file_name = OUTPUT_FILE_PREFIX + index + OUTPUT_FILE_NAME_EXT
    
    print "Saving all data to: %s" % out_file_name
    
    try:

        with open(out_file_name, 'w') as f:  
                  
            for i, k_elt in enumerate(k):    
                
                row = [k_elt[K_NAME_1_COL], k_elt[K_NAME_2_COL]] + extm[i] + \
                    p[i] + p_rf[i] + [ap_rf[i]] + p_nn[i] + [ap_nn[i]]
                       
                f.write("%s\n" % CSV_DELIMITER.join(str(e) for e in row))
        
        print "File saved: %s" % out_file_name
           
    except IOError as ioe:
         print "Error saving file: '%s'" % out_file_name
    