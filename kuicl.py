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

from ctes import *
from kparser import *
from storage import *
from kscraping import *
from compdata import *
from propre import *
from ap import *
from kfiles import *
from resum import *
from prun import do_prun

def generate_local_data(index, scr, stor):
 
    scr.scrap_cl_data()
    
    prp = ProPre(index, stor)
    
    prp.generate_pro_data()
    
    prp.generate_pre_data()

def calc_with_all_sources(index, scr, stor):
    
    # If an index has been provided try to read data from local files.
    if int(index) > DEFAULT_INDEX:       
        read_data_from_file(index, stor)    
    
    if not stor.ext_data_ok:
        scr.scrap_all_sources()
        
    if stor.ext_data_ok:
        
        # Generate own data.
        generate_local_data(index, scr, stor)
        
        # Compose the data.
        if stor.pro_pre_exists:
            
            compdat = ComposeData(index, stor)
            
            compdat.compose_all_data()
            
            final_data = compdat.get_final_data()
                
            ap_data = []
            
            for j, fd in enumerate(final_data):
                row = fd
                print row
                ap_data.append([row[AP_LI_COL]] + 
                               [row[AP_FIRST_P_COL + k] \
                                    for k in range(NAME_DATA_LEN) ])
            
            calculate_ap(ap_data, scr.index)
        else:
            print "ERROR: No data to compose."
    else:
        print "ERROR: Not enough data."

def calc_final_data(stor):

    final_data = []
    
    for i, kd in enumerate(stor.k):
        type_k = kd[K_TYPE_COL]
            
        p_final = ProPre.calc_final_p(stor.pro[i], stor.pre[i], type_k)
            
        final_data.append([type_k] + [ int(round(p)) for p in p_final ])
    
    return final_data

def calc_with_own_sources(index, scr, stor):
    
    if int(index) > DEFAULT_INDEX:
                        
        stor.load_local_data() 
        
        if ( not stor.pro_exists ) or ( not stor.pre_exists ): 
                       
            generate_local_data(index, scr, stor)            
        
        final_data = calc_final_data(stor)
        
        calculate_ap(final_data, scr.index)
    else:
        print "An index must be provided."

def main(progargs):
    """Main function.
    """    
    
    stor = Storage()
    
    if progargs.index_provided:
        print "Let's go with index %s ..." % progargs.index
        
        scr = KScraping(progargs.index, stor)
        
        if progargs.use_all_sources:
            print "Using all sources ..."
            calc_with_all_sources(progargs.index, scr, stor)    
        else:
            print "Using only local sources ..."
            calc_with_own_sources(progargs.index, scr, stor)
                
        print "Calculating prun ..."     
        do_prun(progargs.index, stor)
    else:
        print "No index provided. Only retrieving res ..."
    
        retrieve_res()
        
    print "Program finished."
    
    return 0

# Where all begins ...
if __name__ == "__main__":
    
    try:
        # Object to process the program arguments.
        progargs = ProgramArguments()
        
        sys.exit(main(progargs))   
    except ProgramArgumentsException as pae:
        print pae       
