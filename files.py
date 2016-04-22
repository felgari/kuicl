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

"""Functions related to files.
"""

import csv

from ctes import *
from storage import *

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
    except IOError:
        print "ERROR: reading file %s" % input_file_name
        
    if len(data):
        print "Read: %dx%d" % (len(data), len(data[0]))
            
    return data

def read_k_file(index, stor):
    
    k_file_name = K_FILE_NAME_PREFIX + index + INPUT_FILE_NAME_EXT
    
    stor.k = read_input_file(k_file_name) 

def read_pro_file(index, stor):
    
    pro_file_name = PRO_FILE_NAME_PREFIX + index + INPUT_FILE_NAME_EXT
    
    stor.pro = read_input_file(pro_file_name)

def read_pre_file(index, stor):
    
    pre_file_name = PRE_FILE_NAME_PREFIX + index + INPUT_FILE_NAME_EXT
    
    stor.pre = read_input_file(pre_file_name)
    
def read_res_file(file_name):
    
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
        
    if len(res_data):
        print "Read: %dx%d" % (len(res_data), len(res_data[0]))
            
    return res_data

def _extract_list_text(txt, num):
    
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

def read_data_from_file(index, stor):
    
    success = True
    lines = []
    
    # Read K data from local.
    stor.k_data = read_k_file(index, stor)    
    
    # Reading from local file the rest of data.
    file_name = SCRAPPED_DATA_FILE_PREFIX + index + SCRAPPED_DATA_FILE_EXT  
    
    print "Reading data from file: %s" % file_name
    
    try:
        with open(file_name, "r") as f:
            for l in f:
                
                # Process text line.        
                l_txt = l[:-1].strip()
                
                if len(l_txt):                  
                    if l_txt.find(LM_TEXT) >= 0:
                        stor.lm = _extract_list_text(l_txt, NUM_COLS_LM)
                        print "Read %dx%d from file for LM" % \
                            (len(stor.lm), len(stor.lm[0]))
                            
                    elif l_txt.find(VE_TEXT) >= 0:
                        stor.ve = _extract_list_text(l_txt, NUM_COLS_VE)
                        print "Read %dx%d from file for VE" % \
                            (len(stor.ve), len(stor.ve[0]))
                            
                    elif l_txt.find(QU_TEXT) >= 0:
                        stor.qu = _extract_list_text(l_txt, NUM_COLS_QU)
                        print "Read %dx%d from file for QU" % \
                            (len(stor.qu), len(stor.qu[0]))
                            
                    elif l_txt.find(Q1_TEXT) >= 0:
                        stor.q1 = _extract_list_text(l_txt, NUM_COLS_Q1)
                        print "Read %dx%d from file for Q1" % \
                            (len(stor.q1), len(stor.q1[0]))
                            
                    elif l_txt.find(CQ_TEXT) >= 0:
                        stor.cq = _extract_list_text(l_txt, NUM_COLS_CQ)
                        print "Read %dx%d from file for CQ" % \
                            (len(stor.cq), len(stor.cq[0]))
                            
                    elif l_txt.find(CQP_TEXT) >= 0:
                        stor.cqp = _extract_list_text(l_txt, NUM_COLS_CQ)
                        print "Read %dx%d from file for CQP" % \
                            (len(stor.cqp), len(stor.cqp[0]))
                        
                    elif l_txt.find(B1_TEXT) >= 0:
                        stor.b1 = _extract_list_text(l_txt, NUM_COLS_CL)
                        print "Read %dx%d from file for B1" % \
                            (len(stor.b1), len(stor.b1[0]))
                        
                    elif l_txt.find(A2_TEXT) >= 0:
                        stor.a2 = _extract_list_text(l_txt, NUM_COLS_CL)
                        print "Read %dx%d from file for A2" % \
                            (len(stor.a2), len(stor.a2[0]))
                            
    except IOError as ioe:
        print "Not found file: '%s'" % file_name  
        success = False
        
    return success 

def save_k_data(index, k_data):
    
    success = True
    
    out_file_name = K_FILE_NAME_PREFIX + index + INPUT_FILE_NAME_EXT
    
    print "Saving file: %s with %dx%d elements" % \
        (out_file_name, len(k_data), len(k_data[0]))
        
    try:
    
        with open(out_file_name, 'w') as f:
        
            for d in k_data:
                f.write("%s,%s,%s,%s\n" % (d[0], d[1], d[2], d[3]))
        
    
    except IOError as ioe:
         print "Error saving file: '%s'" % out_file_name 
         success = False
         
    return success

def save_scraping_data(index, stor):
    
    out_file_name = SCRAPPED_DATA_FILE_PREFIX + index + SCRAPPED_DATA_FILE_EXT
    
    try:
        
        with open(out_file_name, 'w') as f:
        
            f.write("%s %s %s\n\n" % (LM_TEXT, SCR_TXT_DELIM, str(stor.lm)))
            f.write("%s %s %s\n\n" % (VE_TEXT, SCR_TXT_DELIM, str(stor.ve)))
            f.write("%s %s %s\n\n" % (QU_TEXT, SCR_TXT_DELIM, str(stor.qu)))
            f.write("%s %s %s\n\n" % (Q1_TEXT, SCR_TXT_DELIM, str(stor.q1)))
            f.write("%s %s %s\n\n" % (CQ_TEXT, SCR_TXT_DELIM, str(stor.cq)))
            f.write("%s %s %s\n\n" % (CQP_TEXT, SCR_TXT_DELIM, str(stor.cqp)))
            f.write("%s %s %s\n\n" % (B1_TEXT, SCR_TXT_DELIM, str(stor.b1)))
            f.write("%s %s %s\n" % (A2_TEXT, SCR_TXT_DELIM, str(stor.a2))) 
        
        print "Data scrapped saved in: %s" % out_file_name
        
    except IOError as ioe:
         print "Error saving file: '%s'" % out_file_name  
         
def save_res_data(out_file_name, data):
    
    print "Saving file: %s" % out_file_name
    
    try:
        
        with open(out_file_name, 'w') as f:
    
            for d in data:
                if type(d) is int:
                    f.write("%d\n" % d)
                else:
                    f.write("%s\n" % unicodedata.normalize('NFKD', d).encode('ascii','ignore'))
    
    except IOError as ioe:
         print "Error saving file: '%s'" % out_file_name 

def save_data_to_csv(out_file_name, data):
    
    try:
        
        with open(out_file_name, 'w') as f:        
            for d in data:            
                f.write("%s\n" % CSV_DELIMITER.join(str(i) for i in d))
        
        print "File saved: %s" % out_file_name
           
    except IOError as ioe:
         print "Error saving file: '%s'" % out_file_name 