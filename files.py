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

def read_k_file(index):
    
    k_file_name = K_FILE_NAME_PREFIX + index + INPUT_FILE_NAME_EXT
    
    return read_input_file(k_file_name)

def read_pro_file(index):
    
    pro_file_name = PRO_FILE_NAME_PREFIX + index + INPUT_FILE_NAME_EXT
    
    return read_input_file(pro_file_name)

def read_pre_file(index):
    
    pre_file_name = PRE_FILE_NAME_PREFIX + index + INPUT_FILE_NAME_EXT
    
    return read_input_file(pre_file_name)