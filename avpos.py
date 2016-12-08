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

"""Class to get average pos.
"""

import datetime
import os

from ctes import *
from clda import ClDat
from kfiles import save_data_to_csv

class AvPos(object):
    
    def __init__(self):
        
        self.__dir = None
        
        self.__cl_files = []
        
        self.__cl_files_order = []
        
    def _compose_dir_name(self):
        
        now = datetime.datetime.now()
        
        first_year = now.year
        
        if now.month < REF_MONTH:
            first_year = first_year - 1
            
        self.__dir = str(first_year - 2000) + "-" + str(first_year + 1 - 2000)
    
    def _get_cl_files(self, dir):
        
        print "Searching cl files in: %s" % dir
        
        return [fn for fn in os.listdir(dir) 
                    if fn.startswith(PREFIX_CL_FILE_NAME)]
    
    def _extract_order(self, file_name):
        
        return int(os.path.splitext(file_name)[0][len(PREFIX_CL_FILE_NAME):])
        
    def _compile_cl(self):
        
        self._compose_dir_name()
        
        self.__cl_files = self._get_cl_files(self.__dir)
        
        self.__cl_files_order = \
            [ self._extract_order(fn) for fn in self.__cl_files ]
            
    def _add_cl(self, avpos, cldata):
        
        for c in cldata:
            
            name = c[CL_NAME_COL]
            pos = c[CL_POS_COL]

            found = False
            
            for a in avpos:
                
                if a[AVPOS_NAME_COL] == name:
                    a.append(pos)
                    found = True
                    break
                
            if not found:
                avpos.append([name, pos])
            
        return avpos
        
    def get_avpos(self):
        
        avpos = []
        
        # Compile files with cl.
        self._compile_cl()
        
        # Process the files sorted by name.
        files_sorted = sorted(self.__cl_files_order)
        
        for fs in files_sorted:
            idx = self.__cl_files_order.index(fs)
            
            clda = ClDat(NO_READ_INDEX)
            
            full_file_name = os.path.join(self.__dir, self.__cl_files[idx])
            
            clda.read_cldata(full_file_name)
            
            avpos = self._add_cl(avpos, clda.b1)
            avpos = self._add_cl(avpos, clda.a2)
            
        save_data_to_csv(AVPOS_FILE, avpos)
            
        return avpos
            
            