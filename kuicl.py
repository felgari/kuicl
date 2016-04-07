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

"""Calculations with local data and data scrapped from web pages.
"""

import sys
import kparser
from ctes import *
from kscraping import *
from compdata import *
from propre import *
from ap import *
from files import *
from resum import *
from prun import do_prun

def get_own_data(scr):
    """Get own data. This data could be generated from some data already 
    scrapped or could be read from local files.    
    """

    pro_data = []
    pre_data = []
    
    propre = ProPre(scr.k_data, scr.b1_data, scr.a2_data, scr.index)
    
    # Try to read data from file.
    if scr.index > DEFAULT_INDEX:           
        pro_data = read_pro_file(scr.index)
        
        pre_data = read_pre_file(scr.index)
    
    # If the data has not been read from a file, generate it.
    if not len(pro_data):
        pro_data = propre.generate_pro_data()
        
    if not len(pre_data):        
        pre_data = propre.generate_pre_data()        
    
    return pro_data, pre_data

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

def read_data_from_file(index, scr):
    
    success = True
    lines = []
    
    # Read K data from local.
    scr.k_data = read_k_file(index)    
    
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

def calc_with_all_sources(scr):
    
    # If an index has been provided try to read data from local files.
    if int(scr.index) > DEFAULT_INDEX:       
        read_data_from_file(scr.index, scr)    
    
    if not scr.data_ok(): # Scrap data from the web.
        scr.scrap_all_sources()
        
    if scr.data_ok():
        
        # Generate own data.
        pro_data, pre_data = get_own_data(scr)
        
        # Compose the data.
        if len(pro_data) and len(pre_data):
            
            compdat = ComposeData(scr, pro_data, pre_data)
            compdat.compose_all_data()
            
            final_data = compdat.get_final_data()
            
            for i, aps in enumerate(AP_SUFFIXES):
                
                ap_data = []
                
                for j, fd in enumerate(final_data):
                    row = fd
                    ap_data.append([row[AP_LI_COL]] + 
                                   [row[AP_FIRST_P_COL + k + i * NAME_DATA_LEN] \
                                        for k in range(NAME_DATA_LEN) ])
                
                calculate_ap(ap_data, scr.index + aps)
        else:
            print "ERROR: No data to compose."
    else:
        print "ERROR: Not enough data."

def calc_final_data(k_data, pro_data, pre_data):

    final_data = []
    
    for i, kd in enumerate(k_data):
        type_k = kd[K_TYPE_COL]
            
        p_final = ProPre.calc_final_p(pro_data[i], pre_data[i], type_k)
            
        final_data.append([type_k] + [ int(round(p)) for p in p_final ])
    
    return final_data
        
def calc_with_own_sources(scr):
    
    if int(scr.index) > DEFAULT_INDEX:                 
        # Read data from local.
        k_data = read_k_file(scr.index)                   
        pro_data = read_pro_file(scr.index)
        pre_data = read_pre_file(scr.index) 
        
        if not len(pro_data) or not len(pre_data) == 0:            
            scr.scrap_cl_data()
            
            prp = ProPre(k_data, scr.b1_data, scr.a2_data, scr.index)     
                    
            pro_data = prp.generate_pro_data()
        
            pre_data = prp.generate_pre_data()            
        
        final_data = calc_final_data(k_data, pro_data, pre_data)
        
        calculate_ap(final_data, scr.index)
    else:
        print "An index must be provided."

def main(progargs):
    """Main function.
    """    
    
    if progargs.index_provided:
        print "Let's go with index %s ..." % progargs.index
        
        scr = KScraping(progargs.index)
        
        if progargs.use_all_sources:
            print "Using all sources ..."
            calc_with_all_sources(scr)    
        else:
            print "Using only local sources ..."
            calc_with_own_sources(scr)   
            
        print "Calculating prun ..."     
        do_prun(progargs.index)
    else:
        print "No index provided. Only retrieving res ..."
    
        retrieve_res()
        
    print "Program finished."
    
    return 0

# Where all begins ...
if __name__ == "__main__":
    
    try:
        # Object to process the program arguments.
        progargs = kparser.ProgramArguments()
        
        sys.exit(main(progargs))   
    except kparser.ProgramArgumentsException as pae:
        print pae       
