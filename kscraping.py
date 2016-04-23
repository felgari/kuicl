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

"""Class to scrap web sites.
"""

import requests
import urllib2
from bs4 import BeautifulSoup
import unicodedata
import json
import os

from ctes import *
from storage import *
from kfiles import *

class KScraping(object):
    """Scraping on some web pages.
    """
    
    def __init__(self, index, stor):
        """Constructor.                        
        """    
        
        self._index = index
        
        self._stor = stor
    
    # ------------------------------------- Common functions.
    def _prepare_request(self, url):
        """Prepare a http request to the url received.
        """
        
        session = requests.Session()
    
        return session.get(url, headers=REQUEST_HEADERS)    
    
    def _check_url(self, url, req):
        """Check connection and retrieving from the url received.
        
        Args:
            url: URL to use.
            req: Request to use.
            
        """
        
        bsObj = None
        
        print "Reading page from: %s" % url
        
        try:    
            _ = urllib2.urlopen(url)
        except urllib2.HTTPError as he:
            print(he)
        except urllib2.URLError as ue:
            print(ue)
        else:
            try:
                bsObj = BeautifulSoup(req.text, "lxml")
            except AttributeError as ae:
                print(ae)
                
        return bsObj 
    
    # ------------------------------------- K scraping.        
    def _process_k_page(self, bsObj):
        
        success = True
        
        temp_index = ''
        
        first = []
        second = []
        data = []
        
        for cobj in bsObj.findAll(K_COBJ, K_COBJ_DICT):
            for eobj in cobj.findAll(K_EOBJ, K_EOBJ_NAME):
                txt = eobj.get_text().strip()
                txt_norm = unicodedata.normalize('NFKD', txt).encode('ascii','ignore')
                pos2 = txt_norm.find(K_POS_1_SEP)
                pos1 = txt_norm[:pos2].rfind(K_POS_2_SEP)
                temp_index = txt_norm[pos1+1:pos2].strip()
                
        print temp_index
        
        for cobj in bsObj.findAll(K_COBJ_INF, K_COBJ_INF_DICT):
            for eobj in cobj.findAll(K_EOBJ_1, K_EOBJ_1_NAME):
                txt = eobj.get_text().strip()
                txt_norm = unicodedata.normalize('NFKD', txt).encode('ascii','ignore')
                first.append(txt_norm)
                
            for eobj in cobj.findAll(K_EOBJ_2, K_EOBJ_2_NAME):
                txt = eobj.get_text().strip()
                txt_norm = unicodedata.normalize('NFKD', txt).encode('ascii','ignore')
                second.append(txt_norm)
            
        if len(first) == len(second):
            for i, first_it in enumerate(first):
                type_el = TYPE_1_COL
                
                try:               
                    first_name = K_B1_STR_CONVERT[first_it]
                    second_name = K_B1_STR_CONVERT[second[i]]
                except KeyError:                
                    type_el = TYPE_2_COL
                    first_name = K_A2_STR_CONVERT[first_it]
                    second_name = K_A2_STR_CONVERT[second[i]]

                data.append([str(i), type_el, first_name, second_name])
        else:
            print "ERROR reading K, data not paired."       
            success = False
            
        self._stor.k = data
        
        success = save_k_data(temp_index, data)   
        
        if success:
            self._index = temp_index    
            
        return success  
    
    def _k_scraping(self):
    
        if len(self._stor.k) != NUM_ROWS:
            req = self._prepare_request(K_URL)
        
            bsObj = self._check_url(K_URL, req)
            
            try:
                self._process_k_page(bsObj)
            except KeyError as ke:
                print "ERROR in k: %s" % ke
    
    # ------------------------------------- Re scraping.        
    def _process_re_page(self, bsObj):

        data = []
        
        for cobj in bsObj.findAll(RE_COBJ, RE_LINE):            
            for eobj in cobj.findAll(RE_EOBJ, RE_SECOND): 
                second = eobj.get_text().strip()
            for eobj in cobj.findAll(RE_EOBJ, RE_FIRST): 
                data.append(eobj.get_text().strip())     
                
            data.append(second)              
                
            marcador = True
            for eobj in cobj.findAll(RE_EOBJ, RE_SCO):
                if marcador: 
                    data.append(eobj.get_text().strip())
                    marcador = False
                else:
                    data.append(eobj.get_text().strip())
                
            for eobj in cobj.findAll(RE_EOBJ, RE_VAL): 
                txt = eobj.get_text().strip()
                if len(txt) and txt[-1] == "'":
                    plus = -1
                    i = len(txt) - 2
                    while ( txt[i].isdigit() or txt[i] == RE_DELIM) and i >= 0:
                        if txt[i] == RE_DELIM:
                            plus = i
                        i -= 1
                    z = 0
                    if plus > 0:
                        x = int(txt[i:plus])
                        y = int(txt[plus+1:-1])
                        z =  x + y
                    else:
                        z = int(txt[i:-1])
                    data.append(z)
                    
        return data
    
    def _re_scraping(self, url):
        
        req = self._prepare_request(url)
    
        bsObj = self._check_url(url, req)
        
        return self._process_re_page(bsObj)    
    
    # ------------------------------------- LM scraping.    
    def _process_lm_page(self, bsObj):
        
        i = 0
        j = 0
        n = 0
        
        for cobj in bsObj.findAll(LM_COBJ):
            for eobj in cobj.findAll(LM_EOBJ, LM_DICT):        
                    
                if i == NUM_ROWS:
                    return 
                
                elif n >= LM_FIRST_COL and n <= LM_LAST_COL:
    
                    self._stor.lm[i][j] = int(eobj.get_text().strip())
                    
                    j += 1
                    if j == NUM_COLS:
                        i += 1
                        j = 0                   
                     
                n = (n + 1) % LM_TD_ROW_SIZE        
    
    def _lm_scraping(self):
        
        if sum(self._stor.lm[0]) == 0:
            req = self._prepare_request(LM_URL)
        
            bsObj = self._check_url(LM_URL, req)
            
            self._process_lm_page(bsObj)
            
            print "Read: %dx%d" % (len(self._stor.lm), len(self._stor.lm[0]))
        
    # ------------------------------------- VE scraping.        
    def _process_ve_page(self, bsObj):

        i = 0
        for ob in bsObj.findAll(VE_COBJ_1, VE_DICT_1):     
            j = 0   
            for cobj in ob.findAll(VE_COBJ_2, VE_DICT_2):
                self._stor.ve[i][j] = int(cobj.get(VE_ATTRIBUTE))
                
                j += 1
                if j == NUM_COLS:
                    i += 1
                    j = 0      
    
    def _ve_scraping(self):
        
        if sum(self._stor.ve[0]) == 0:
            req = self._prepare_request(VE_URL)
        
            bsObj = self._check_url(VE_URL, req)
            
            self._process_ve_page(bsObj)
            
            print "Read: %dx%d" % (len(self._stor.ve), len(self._stor.ve[0]))

    # ------------------------------------- QU scraping.
    def _process_qu_page(self, bsObj):
        
        i = 0
        j = 0   
        n = 0 
        
        for cobj in bsObj.findAll(QU_COBJ, QU_DICT):
            
            if i == NUM_ROWS - 1:
                return
            
            elif n >= QU_FIRST_COL and n <= QU_LAST_COL:
    
                self._stor.qu[i][j] = int(cobj.get_text())
                
                j += 1
                if j == NUM_COLS:
                    i += 1
                    j = 0                   
                 
            n = (n + 1) % QU_TD_ROW_SIZE 
    
    def _qu_scraping(self):
        
        if sum(self._stor.qu[0]) == 0:
            req = self._prepare_request(QU_URL)
        
            bsObj = self._check_url(QU_URL, req)
            
            self._process_qu_page(bsObj)
            
            print "Read: %dx%d" % (len(self._stor.qu), len(self._stor.qu[0]))
            
    # ------------------------------------- Q1 scraping.
    def _process_q1_page(self, bsObj):
        
        try:
            json_obj = bsObj.find(Q1_COBJ).get_text()
            
            json_data = json.loads(str(json_obj))
            
            for i in range(NUM_ROWS - 1):
                el = json_data[i]
                
                self._stor.q1[i][0] = int(el[FIRST_FIELD])
                self._stor.q1[i][1] = int(el[SECOND_FIELD])
                self._stor.q1[i][2] = int(el[THIRD_FIELD])  
        except UnicodeEncodeError as uee:
            print uee                   
    
    def _q1_scraping(self):
        
        if sum(self._stor.q1[0]) == 0:
            # The ULR depends on the index received.  
            url = Q1_URL + self.index
            
            req = self._prepare_request(url)
        
            bsObj = self._check_url(url, req)
            
            self._process_q1_page(bsObj)    
            
            print "Read: %dx%d" % (len(self._stor.q1), len(self._stor.q1[0]))        
        
    # ------------------------------------- CQ scraping.
    def _process_cq_page(self, bsObj):
        
        current_data = self._stor.cq
        
        i = 0
        for ob in bsObj.findAll(CQ_OB, CQ_DICT):        
            for cobj in ob.findAll(CQ_OBJ):
                j = 0
                for eobj in cobj.findAll(CQ_EOBJ, CQ_EOBJ_DICT):
                    txt = eobj.get_text().strip() 
                    if i < NUM_ROWS - 1:
                        if len(txt):
                            txt_nor = unicodedata.normalize('NFKD', txt).encode('ascii','ignore')
                            
                            pos = txt_nor.find(CQ_SEP)
                            if pos > 0:
                                txt_red = txt_nor[:pos]                        
                        
                            current_data[i][j] = int(txt_red)
                            
                            j += 1
                            if j == NUM_COLS:
                                i += 1
                                j = 0 
                    
            current_data = self._stor.cqp  
            i = 0
            j = 0                     
    
    def _cq_scraping(self):
        
        if sum(self._stor.cq[0]) == 0:
            url = CQ_URL
            
            req = self._prepare_request(url)
        
            bsObj = self._check_url(url, req)        
            
            self._process_cq_page(bsObj)     
            
            print "Read: %dx%d" % (len(self._stor.q1), len(self._stor.q1[0]))     
    
    # ------------------------------------- CL scraping.
    def _fill_cl_data(self, data, index, size, bsObj, cobj_data):
        
        temp_lst = []
        
        for cobj in bsObj.findAll(CL_COBJ, cobj_data):        
            temp_lst.append(cobj.get_text())  
            
        for i in range(size):
            data[i][index] = int(temp_lst[i])                  
    
    def _process_cl_page(self, bsObj, size):
        
        data = [[0 for _ in range(NUM_COLS_CL)] for _ in range(size)]
        
        temp_lst = []        
        
        for cobj in bsObj.findAll(CL_COBJ, CL_EQ_DICT):        
            temp_lst.append(cobj.get_text()) 
            
        for i in range(size):
            try:
                data[i][CL_POS_COL] = i + 1
                data[i][CL_NAME_COL] = CL_STR_CONVERT[temp_lst[i]]
            except KeyError as ke:
                print "ERROR: %s" % ke                  
           
        for i, elt in enumerate(CL_ELEMENTS):            
            self._fill_cl_data(data, i + CL_INDEX_P_LO, size, bsObj, elt) 
            
        return data            
    
    def _cl_scraping(self, url, size):
        
        req = self._prepare_request(url)
    
        bsObj = self._check_url(url, req)
        
        data = self._process_cl_page(bsObj, size)
        
        print "Read: %dx%d" % (len(data), len(data[0]))
        
        return data            
    
    # ------------------------------------- Properties.  
    @property
    def index(self):
        return self._index   
    
    @property
    def cl_data_ok(self):
        return self._stor.k == NUM_ROWS and self._stor.b1 == B1_SIZE and \
            self._stor.a2 == A2_SIZE     

    def _get_res_file_name(self, index):
        
        return RES_FILE_PREFIX + index + INPUT_FILE_NAME_EXT
        
    def _scrap_res(self, max_range, file_dir, url_prefix, data_size): 
        
        for i in range(1, max_range + 1):
            
            i_str = str(i).zfill(2)
            
            file_name = os.path.join(os.getcwd(), file_dir, \
                                     self._get_res_file_name(i_str))
            
            if not os.path.exists(file_name):   
                print "Retrieving data for file: %s" % file_name  
                url = url_prefix + i_str   
                data = self._re_scraping(url)
                
                # If data could not be get, exit.
                if len(data) > data_size * 4:                     
                    self._save_res_data(file_name, data)
                else:
                    print "Exiting as no data has been retrieved for: %s." % \
                        file_name
                    break     
                
    def _save_res_data(self, out_file_name, data):
        
        print "Saving file: %s" % out_file_name
        
        try:
            
            with open(out_file_name, 'w') as f:
        
                for d in data:
                    if type(d) is int:
                        f.write("%d\n" % d)
                    else:
                        f.write("%s\n" % unicodedata.normalize('NFKD', d).encode('ascii','ignore'))
        
        except IOError as ioe:
             print "Error saving file: '%s'" % out_file_name                 
    
    # ------------------------------------- Public functions.    
    def scrap_res_data(self):
        
        self._scrap_res(MAX_B1, RES_B1_DIR, RE_B1_URL, B1_SIZE / 2)
        
        self._scrap_res(MAX_A2, RES_A2_DIR, RE_A2_URL, A2_SIZE / 2)           
         
    def scrap_cl_data(self):
        """Scraping CL data.
        """
        
        if len(self._stor.b1) != B1_SIZE:
            self._stor.b1 = self._cl_scraping(CL_B1_URL, B1_SIZE)

        if len(self._stor.a2) != A2_SIZE:
            self._stor.a2 = self._cl_scraping(CL_A2_URL, A2_SIZE)
        
    def scrap_all_sources(self):
        """Scraping data from multiple sources.
        """
        
        self._k_scraping()

        self._lm_scraping()
        
        self._ve_scraping()
        
        self._qu_scraping()
        
        self._q1_scraping()
        
        self._cq_scraping()      
        
        self.scrap_cl_data()          
        
        if self.data_ok():
            save_scraping_data(self._index, self._stor)      
        
    def data_ok(self):
         
        return len(self._stor.k) == NUM_ROWS and \
            len(self._stor.lm) == NUM_ROWS and \
            len(self._stor.ve) == NUM_ROWS and \
            len(self._stor.qu) == NUM_ROWS and \
            len(self._stor.q1) == NUM_ROWS and \
            len(self._stor.cq) == NUM_ROWS and \
            len(self._stor.cqp) == NUM_ROWS and \
            len(self._stor.b1) == B1_SIZE and \
            len(self._stor.a2) == A2_SIZE
            
    def __str__(self):
        
        return "%s: %d %d %d %d %d %d %d %d %d" % \
        (type(self).__name__, len(self._stor.k), len(self._stor.lm), \
            len(self._stor.ve), len(self._stor.qu), len(self._stor.q1), \
            len(self._stor.cq), len(self._stor.cqp), len(self._stor.b1), \
            len(self._stor.a2))        