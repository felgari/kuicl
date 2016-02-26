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
    
    index_data = []
    pro_data = []
    pre_data = []
    
    # Try to generate the data.
    if scr.pre_data_ok:
        
        propre = ProPre(scr.k_data, scr.b1_data, scr.a2_data)
        
        index_data = propre.index_data
        pro_data = propre.pro_data
        pre_data = propre.pre_data
        
    if len(index_data) == 0 or len(pro_data) == 0 or len(pre_data) == 0:
        
        if scr.index > DEFAULT_INDEX:
            # Read local data.
            index_file_name = K_FILE_NAME_PREFIX + scr.index + INPUT_FILE_NAME_EXT
            index_data = read_input_file(index_file_name)
            
            pro_file_name = PRO_FILE_NAME_PREFIX + scr.index + INPUT_FILE_NAME_EXT
            pro_data = read_input_file(pro_file_name)
            
            pre_file_name = PRE_FILE_NAME_PREFIX + scr.index + INPUT_FILE_NAME_EXT
            pre_data = read_input_file(pre_file_name)
        else:
            print "ERROR: No index as argument to get local data."
    
    return index_data, pro_data, pre_data

def main(index):
    """Main function.
    """    
    
    print "Let's go ..."
    
    # Do some scraping.
    scr = KScraping(index)

    scr.scrap_pre_data()    
    
    index_data, pro_data, pre_data = get_own_data(scr)   
    
    if len(index_data) > 0 and len(pro_data) and \
        len(pre_data) > 0:
        
        # Do more scraping.
        scr.scrap_post_data()
    
        # Compose data.
        compdat = ComposeData(scr, index_data, pro_data, pre_data)
        
        compdat.compose()
        
        final_data = compdat.get_final_data()
        
        print final_data
        
        # Finally calculate ap.
        calculate_ap(final_data, index)
    else:
        print "ERROR: No local data."
        
    print "Program finished."
    
    return 0

# Where all begins ...
if __name__ == "__main__":
    
    index = DEFAULT_INDEX
    
    if len(sys.argv) == NUM_ARGS:
        index = sys.argv[1]
    
    sys.exit(main(index))
