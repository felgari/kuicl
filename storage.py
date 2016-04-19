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

"""Class to store the data used during the calculations.
"""

from files import *
from kscrapping import *
from resum import *

class Storage(object):
    
    def __init__(self):
        
        self._k = []
        self._pro = []
        self._pre = []
        self._lm = []
        self._ve = []
        self._qu = []
        self._q1 = []
        self._cq = []
        self._cqp = []
        self._mean = []
        self._b1_cl = []
        self._a2_cl = []
        self._p = []
        self._ap = []
        self._un = []
        self._res = []
        
    @property
    def k(self):
        return self._k
    
    @k.setter
    def k(self, k_data):
        self._k = k_data
        
    @property
    def k_exists(self):
        return len(self._k) > 0
        
    @property
    def pro(self):
        return self._pro
    
    @pro.setter
    def pro(self, pro_data):
        self._pro = pro_data    
        
    @property
    def pro_exists(self):
        return len(self._pro) > 0
        
    @property
    def pre(self):
        return self._pre
    
    @pre.setter
    def pre(self, pre_data):
        self._pre = pre_data  
        
    @property
    def pre_exists(self):
        return len(self._pre) > 0
        
    @property
    def lm(self):
        return self._lm
    
    @lm.setter
    def lm(self, lm_data):
        self._lm = lm_data  
        
    @property
    def lm_exists(self):
        return len(self._lm) > 0   
        
    @property
    def ve(self):
        return self._ve
    
    @ve.setter
    def ve(self, ve_data):
        self._ve = ve_data  
        
    @property
    def ve_exists(self):
        return len(self._ve) > 0
        
    @property
    def qu(self):
        return self._qu
    
    @qu.setter
    def qu(self, qu_data):
        self._qu = qu_data  
        
    @property
    def qu_exists(self):
        return len(self._qu) > 0
        
    @property
    def q1(self):
        return self._q1
    
    @q1.setter
    def q1(self, q1_data):
        self._q1 = q1_data  
        
    @property
    def q1_exists(self):
        return len(self._q1) > 0 
    
    @property
    def cq(self):
        return self._cq
    
    @cq.setter
    def cq(self, cq_data):
        self._cq = cq_data 
        
    @property
    def cq_exists(self):
        return len(self._cq) > 0 
        
    @property
    def cqp(self):
        return self._cqp
    
    @cqp.setter
    def cqp(self, cqp_data):
        self._cqp = cqp_data 
        
    @property
    def cqp_exists(self):
        return len(self._cqp) > 0  
        
    @property
    def b1(self):
        return self._b1
    
    @b1.setter
    def b1(self, b1_data):
        self._b1 = b1_data  
        
    @property
    def b1_exists(self):
        return len(self._b1) > 0       
        
    @property
    def a2(self):
        return self._a2
    
    @a2.setter
    def a2(self, a2_data):
        self._a2 = a2_data
        
    @property
    def a2_exists(self):
        return len(self._a2) > 0  
    
    @property
    def p(self):
        return self._p
    
    @p.setter
    def p(self, p_data):
        self._p = p_data 
        
    @property
    def ap(self):
        return self._ap
    
    @ap.setter
    def ap(self, ap_data):
        self._ap = ap_data 
        
    @property
    def un(self):
        return self._un
    
    @un.setter
    def un(self, un_data):
        self._un = un_data 
        
    @property
    def ext_data_ok(self):
         
        return len(self._k) == NUM_ROWS and \
            len(self._lm) == NUM_ROWS and \
            len(self._ve) == NUM_ROWS and \
            len(self._qu) == NUM_ROWS and \
            len(self._q1) == NUM_ROWS and \
            len(self._cq) == NUM_ROWS and \
            len(self._cqp) == NUM_ROWS and \
            len(self._b1) == B1_SIZE and \
            len(self._a2) == A2_SIZE
            
    @property
    def pro_pre_exists(self):
        return len(self._pro) > 0 and len(self._pre) > 0

    def calc_mean(self):
        mean_sources = []
        
        if len(self._lm):
            mean_sources.append(self._lm)
        if len(self._ve):
            mean_sources.append(self._ve)
        if len(self._qu):
            mean_sources.append(self._qu)
        if len(self._q1):
            mean_sources.append(self._q1)
        if len(self._cq):
            mean_sources.append(self._cq)
        
        if len(mean_sources) > 1:
            for i in NUM_ROWS:
                new_row = []
                for j in NUM_COLS:
                    values = [s[i][j] for s in mean_sources]
                    new_row.append(mean(values))
                
                self._mean.append(new_row)
                
    @property
    def mean(self):
        
        if not len(self._mean):
            self.calc_mean()                                                      
        
        return self._mean
    
    def load_local_data(self):
        
        success = True
        
        read_k_file(scr.index, self)                   
        read_pro_file(scr.index, self)
        read_pre_file(scr.index, self)
        
        return success
        
    def load_all_data(self):
        
        success = True
        
        self.load_local_data()
        
        pass # TODO
        # lm ...
        
        return success        
    
    def save_data(self):
        
        pass # TODO
