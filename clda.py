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

"""Class to get and store cl data.
"""

from ctes import *
from kscrap import KScrap
from kfiles import extract_list_text

class ClDat(object):
    
    def __init__(self, index):
        
        self._index = index
        self._b1 = []
        self._a2 = []
        
        # Try read data from a local file.
        self._read_cldata(index)
            
        # If not read from local, retrieve from external source.
        if not self.loaded:
            self._b1, self._a2 = KScrap.scrap_cl_data()
            
            if self.loaded:
                self._save_cldata()
            else:
                # If data isn't retrieved, update the index with the value 
                # received.
                self._index = index
                
    def _read_cldata(self, index):
        
        lines = []   
        
        # Reading from local file the rest of data.
        file_name = PREFIX_CL_FILE_NAME + index + SCRAPPED_DATA_FILE_EXT  
        
        print "Reading data from file: %s" % file_name
        
        try:
            with open(file_name, "r") as f:
                for l in f:
                    
                    # Process text line.        
                    l_txt = l[:-1].strip()
                    
                    if len(l_txt):                  
                        if l_txt.find(B1_TEXT) >= 0:
                            self._b1 = extract_list_text(l_txt, NUM_COLS_CL)
                            print "Read %dx%d from file for B1" % \
                                (len(self._b1), len(self._b1[0]))
                            
                        elif l_txt.find(A2_TEXT) >= 0:
                            self._a2 = extract_list_text(l_txt, NUM_COLS_CL)
                            print "Read %dx%d from file for A2" % \
                                (len(self._a2), len(self._a2[0]))
                                
        except IOError as ioe:
            print "ERROR: Reading file '%s'" % file_name  
            self._b1 = []
            self._a2 = []
            
    def _save_cldata(self):
        
        out_file_name = PREFIX_CL_FILE_NAME + self._index + SCRAPPED_DATA_FILE_EXT
        
        try:
            
            with open(out_file_name, 'w') as f:
            
                f.write("%s %s %s\n\n" % (B1_TEXT, SCR_TXT_DELIM, str(self._b1)))
                f.write("%s %s %s\n" % (A2_TEXT, SCR_TXT_DELIM, str(self._a2))) 
            
            print "Data scrapped saved in: %s" % out_file_name
            
        except IOError as ioe:
             print "Error saving file: '%s'" % out_file_name  
        
    @property
    def b1(self):
        return self._b1
    
    @property
    def a2(self):
        return self._a2
    
    @property
    def index(self):
        return self._index
    
    @property
    def loaded(self):
        return len(self._b1) and len(self._a2)