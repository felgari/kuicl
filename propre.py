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

"""ProPre class.
"""

from ctes import *

class ProPre(object):
    
    def __init__(self, k_data, b1_data, a2_data):
        """Constructor.                        
        """    
        
        self._k_data = k_data
        self._b1_data = b1_data
        self._a2_data = a2_data
        
        self._index = []
        self._pro = []
        self._pre = []
        
    def _generate_index(self):
        
        for k in self._k_data:
            self._index.append([k[TYPE_COL], k[NAME_LO_COL], k[NAME_VI_COL]])
        
    def _generate_pro(self):
        
        pass
    
    def _generate_pre(self):
        
        pass
    
    @property
    def index_data(self):
        return self._index
    
    @property
    def pro_data(self):
        return self._pro
    
    @property
    def pre_data(self):
        return self._pre        
        
    def generate_own_data(self):
        
        self._generate_index()
        
        self._generate_pro()
        
        self._generate_pre()
