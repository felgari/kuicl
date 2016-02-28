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

"""Script to get a web page.
"""

import sys
import csv
from ctes import *
from kscraping import *
from compdata import *
from propre import *
from ap import *

NUM_ARGS = 2

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
        
    print "Read: %dx%d" % (len(data), len(data[0]))
            
    return data

def get_own_data(scr):
    """Get own data. This data could be generated from some data already 
    scrapped or could be read from local files.    
    """

    pro_data = []
    pre_data = []
    
    # Try to read data from file.
    if scr.index > DEFAULT_INDEX:           
        pro_file_name = PRO_FILE_NAME_PREFIX + scr.index + INPUT_FILE_NAME_EXT
        pro_data = read_input_file(pro_file_name)
        
        pre_file_name = PRE_FILE_NAME_PREFIX + scr.index + INPUT_FILE_NAME_EXT
        pre_data = read_input_file(pre_file_name)
    else:            
        propre = ProPre(scr.k_data, scr.b1_data, scr.a2_data)
        
        propre.generate_own_data()
        
        index_data = propre.index_data
        pro_data = propre.pro_data
        pre_data = propre.pre_data
    
    return pro_data, pre_data

def extract_list_text(txt, num):
    
    the_list = []
    
    pos = txt.find(SCR_TXT_DELIM)
    txt_red = txt[pos + 1:].strip()
    
    lst_from_txt = txt_red.translate(None, "[],\'").split()

    n = 0
    new_list = []
    for elt in lst_from_txt:
        new_list.append(elt)

        n += 1
        
        if n == num:
            the_list.append(new_list)
            new_list = []
            n = 0
    
    return the_list  

def read_data_from_file(index, scr):
    
    success = True
    lines = []
    
    # Read K data from local.
    index_file_name = K_FILE_NAME_PREFIX + index + INPUT_FILE_NAME_EXT
    
    scr.k_data = read_input_file(index_file_name)       
    
    # Reading from local file the rest of data.
    file_name = SCRAPPED_DATA_FILE_PREFIX + index + SCRAPPED_DATA_FILE_EXT  
    
    print "Reading data from file: %s" % file_name
    
    try:
        with open(file_name, "r") as f:
            for l in f:
                
                # Process text line.        
                l_txt = l[:-1].strip()
                
                if len(l_txt) > 0:                  
                    if l_txt.find(LM_TEXT) >= 0:
                        scr.lm_data = extract_list_text(l_txt, NUM_COLS_LM)
                        print "Read %dx%d from file for LM" % \
                            (len(scr.lm_data), len(scr.lm_data[0]))
                            
                    elif l_txt.find(VE_TEXT) >= 0:
                        scr.ve_data = extract_list_text(l_txt, NUM_COLS_VE)
                        print "Read %dx%d from file for VE" % \
                            (len(scr.ve_data), len(scr.ve_data[0]))
                            
                    elif l_txt.find(QU_TEXT) >= 0:
                        scr.qu_data = extract_list_text(l_txt, NUM_COLS_QU)
                        print "Read %dx%d from file for QU" % \
                            (len(scr.qu_data), len(scr.qu_data[0]))
                            
                    elif l_txt.find(Q1_TEXT) >= 0:
                        scr.q1_data = extract_list_text(l_txt, NUM_COLS_Q1)
                        print "Read %dx%d from file for Q1" % \
                            (len(scr.q1_data), len(scr.q1_data[0]))
                            
                    elif l_txt.find(CQ_TEXT) >= 0:
                        scr.cq_data = extract_list_text(l_txt, NUM_COLS_CQ)
                        print "Read %dx%d from file for CQ" % \
                            (len(scr.cq_data), len(scr.cq_data[0]))
                            
                    elif l_txt.find(CQP_TEXT) >= 0:
                        scr.cqp_data = extract_list_text(l_txt, NUM_COLS_CQ)
                        print "Read %dx%d from file for CQP" % \
                            (len(scr.cqp_data), len(scr.cqp_data[0]))
                        
                    elif l_txt.find(B1_TEXT) >= 0:
                        scr.b1_data = extract_list_text(l_txt, NUM_COLS_CL)
                        print "Read %dx%d from file for B1" % \
                            (len(scr.b1_data), len(scr.b1_data[0]))
                        
                    elif l_txt.find(A2_TEXT) >= 0:
                        scr.a2_data = extract_list_text(l_txt, NUM_COLS_CL)
                        print "Read %dx%d from file for A2" % \
                            (len(scr.a2_data), len(scr.a2_data[0]))
                            
    except IOError as ioe:
        print "Not found file: '%s'" % file_name  
        success = False
        
    return success 

def main(index):
    """Main function.
    """    
    
    print "Let's go with index %s ..." % index
    
    scr = KScraping(index)
    
    # If an index has been provided try to read data from local files.
    if int(index) > DEFAULT_INDEX:       
        read_data_from_file(index, scr)
    
    if not scr.data_ok():
        # Scrap data from the web.      
        scr.scrap_data()       
    
    if scr.data_ok():
        # Generate own data.
        pro_data, pre_data = get_own_data(scr)   
    
        # Compose the data.
        if len(pro_data) > 0 and len(pre_data) > 0:
            
            compdat = ComposeData(scr, pro_data, pre_data)
            
            compdat.compose()
            
            final_data = compdat.get_final_data()
            
            # Finally calculate ap.
            calculate_ap(final_data, scr.index)
        else:
            print "ERROR: No data to compose."
    else:
        print "ERROR: Not enough data."
        
    print "Program finished."
    
    return 0

# Where all begins ...
if __name__ == "__main__":
    
    index = DEFAULT_INDEX
    
    if len(sys.argv) == NUM_ARGS:
        index = sys.argv[1]
    
    sys.exit(main(index))
