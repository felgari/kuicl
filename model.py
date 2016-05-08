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

"""Class to store model information.
"""

import csv

from ctes import *

class Model(object):
    
    def __init__(self, name, lo_best, lo_mdls, vi_best, vi_mdls):

       self._name = name
       self._lo_best = lo_best
       self._lo_mdls = lo_mdls
       self._vi_best = vi_best
       self._vi_mdls = vi_mdls
       
    @property
    def name(self):
        return self._name
    
    @property
    def lo_best(self):
        return self._lo_best
    
    @property
    def lo_mdls(self):
        return self._lo_mdls
    
    @property
    def vi_best(self):
        return self._vi_best
    
    @property
    def vi_mdls(self):
        return self._vi_mdls
    
    def __str__(self):
        return "%s %0.2f %s %0.2f %s" % (self._name, 
                                         self._lo_best, self._lo_mdls, 
                                         self._vi_best, self._vi_mdls)
    
def read_mdl_file():
    
    file_name = MODELS_FILENAME
    
    print "Reading mdl file: %s" % file_name
                
    mdls = []
    
    try:
        with open(file_name, 'rb') as f:
            
            reader = csv.reader(f)
            
            for row in reader:
                
                name = row[MDL_NAME_COL]
                read_lo_best = False
                read_vi_best = False
                lo_best = 0.0
                lo_mdls = []
                vi_best = 0.0
                vi_mdls = []
                
                for i in range(MDL_FIRST_DATA_COL, len(row)):
                    if row[i].find('.') >= 0:
                        if not read_lo_best:
                            lo_best = float(row[i])
                            read_lo_best = True
                        else:
                            vi_best = float(row[i])
                            read_vi_best = True
                    else:
                        if read_vi_best:
                            vi_mdls.append(int(row[i]))
                        else:
                            lo_mdls.append(int(row[i]))
                            
                mdls.append(Model(name, lo_best, lo_mdls, vi_best, vi_mdls))
            
    except csv.Error:
        print "ERROR: reading file %s" % file_name
    except IOError:
        print "ERROR: reading file %s" % file_name
            
    return mdls