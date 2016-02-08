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
from lmscr import lm_scraping
from vescr import ve_scraping
    
NUM_ARGS = 2

def read_input_file(input_file_name):
                
    data = []
    
    with open(input_file_name, 'rb') as f:
        
        reader = csv.reader(f)
    
        try:
            for row in reader:
                data.append(row)
        
        except csv.Error:
            print "ERROR: reading file %s" % input_file_name
            
    return data                

def main(input_file_name):
    """Main function.
    
    Args:
        input_file_name: Name of the input file to process.

    """    
    
    print "Let's go ..."
    
    lm_data = lm_scraping()
    
    ve_data = ve_scraping()
    
    print ve_data    
        
    print "Program finished."
    
    return 0

# Where all begins ...
if __name__ == "__main__":
    
    if len(sys.argv) == NUM_ARGS:
        sys.exit(main(sys.argv[1]))
    else:
        print "ERROR: Wrong number of parameters. Use: %s input_file_name" % \
        sys.argv[0]   