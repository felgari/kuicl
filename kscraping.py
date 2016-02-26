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

"""QScraping class.
"""

import requests
import urllib2
from bs4 import BeautifulSoup
import unicodedata
import json
import os
from ctes import *

class KScraping(object):
    """Scraping on some web pages.
    """
    
    def __init__(self, index):
        """Constructor.                        
        """    
        
        self._index = index
        
        self._k_data = []
        
        self._b1_data = []
    
        self._a2_data = []         
        
        self._lm_data = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    
        self._ve_data = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    
        self._qu_data = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    
        self._q1_data = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
        
        self._pre_data = False
        
        self._post_data = False  
    
    # ------------------------------------- Common functions.
    def _prepare_request(self, url):
        """Prepare a http request to the url received.
        """
        
        session = requests.Session()
        
        headers = {"User-Agent": USER_AGENT, "Accept": FORMATS_ACCEPTED}
    
        return session.get(url, headers=headers)    
    
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
                bsObj = BeautifulSoup(req.text)
            except AttributeError as ae:
                print(ae)
                
        return bsObj 
    
    # ------------------------------------- K scraping.        
    def _process_k_page(self, bsObj):
        
        success = True
        
        tit = ''
        temp_index = ''
        
        order = []
        first = []
        second = []
        data = []
        
        for cobj in bsObj.findAll(K_COBJ_1, K_COBJ_1_DICT):
            txt = cobj.find(K_EOBJ_1, K_EOBJ_1_NAME).get_text().strip()
            title = unicodedata.normalize('NFKD', txt).encode('ascii','ignore')        
            pos_ini = title.find(K_TITLE_DELIM_1)
            pos_end = title.find(K_TITLE_DELIM_2)
            temp_index = title[pos_ini + 1:pos_end]
            break
        
        for cobj in bsObj.findAll(K_COBJ_2, K_COBJ_2_DICT):
            txt = cobj.find(K_EOBJ_2, K_EOBJ_2_NAME).get_text().strip()
            txt_norm = unicodedata.normalize('NFKD', txt).encode('ascii','ignore')
            txt_splt = txt_norm.split(K_DELIM)
            order = txt_splt
            
            txt = cobj.find(K_EOBJ_3, K_EOBJ_3_NAME).get_text().strip()
            txt_norm = unicodedata.normalize('NFKD', txt).encode('ascii','ignore')
            txt_splt = txt_norm.split(K_DELIM)
            for t in txt_splt:
                pos = t.find('-')        
                first.append(t[:pos])
                second.append(t[pos+1:])     
            
        if len(order) == len(first) and len(first) == len(second):
            for i in range(len(order)):
                type_el = TYPE_1_COL
                try:
                    first_name = K_B1_STR_CONVERT[first[i]]
                    second_name = K_B1_STR_CONVERT[second[i]]
                except KeyError as _:
                    type_el = TYPE_2_COL
                    first_name = K_A2_STR_CONVERT[first[i]]
                    second_name = K_A2_STR_CONVERT[second[i]]
                    
                data.append([order[i], type_el, first_name, second_name])
        else:
            print "ERROR reading K, data not paired."       
            success = False
            
        out_file_name = K_FILE_NAME_PREFIX + tit + INPUT_FILE_NAME_EXT
        
        print "Saving file: %s with %d lines" % (out_file_name, len(data))
        
        # Save data to a file.
        f = open(out_file_name,'w')
        
        for d in data:
            f.write("%s,%s,%s,%s\n" % (d[0], d[1], d[2], d[3]))
        
        f.close()   
        
        # If everything is ok, save also index.
        self._index = temp_index    
            
        return success  
    
    def _k_scraping(self):
    
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
                data.append(eobj.get_text().strip()) 
            for eobj in cobj.findAll(RE_EOBJ, RE_FIRST): 
                data.append(eobj.get_text().strip())  
                
            marcador = True
            for eobj in cobj.findAll(RE_EOBJ, RE_SCO):
                if marcador: 
                    data.append(eobj.get_text().strip())
                    marcador = False
                else:
                    data.append(eobj.get_text().strip())
                
            for eobj in cobj.findAll(RE_EOBJ, RE_VAL): 
                txt = eobj.get_text().strip()
                if len(txt) > 0 and txt[-1] == "'":
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
    
                    self._lm_data[i][j] = int(eobj.get_text().strip())
                    
                    j += 1
                    if j == NUM_COLS:
                        i += 1
                        j = 0                   
                     
                n = (n + 1) % LM_TD_ROW_SIZE        
    
    def _lm_scraping(self):
        
        req = self._prepare_request(LM_URL)
    
        bsObj = self._check_url(LM_URL, req)
        
        self._process_lm_page(bsObj)
        
        print "Read: %d" % len(self._lm_data)
        
    # ------------------------------------- VE scraping.        
    def _process_ve_page(self, bsObj):

        i = 0
        j = 0    
        
        for cobj in bsObj.findAll(VE_COBJ, VE_DICT):
            for eobj in cobj.findAll(VE_EOBJ):
                txt = eobj.get_text()
                
                self._ve_data[i][j] = int(txt[:len(txt) - 1])
                
                j += 1
                if j == NUM_COLS:
                    i += 1
                    j = 0      
    
    def _ve_scraping(self):
        
        req = self._prepare_request(VE_URL)
    
        bsObj = self._check_url(VE_URL, req)
        
        self._process_ve_page(bsObj)
        
        print "Read: %d" % len(self._ve_data)

    # ------------------------------------- QU scraping.
    def _process_qu_page(self, bsObj):
        
        i = 0
        j = 0   
        n = 0 
        
        for cobj in bsObj.findAll(QU_COBJ, QU_DICT):
            
            if i == NUM_ROWS - 1:
                return
            
            elif n >= QU_FIRST_COL and n <= QU_LAST_COL:
    
                self._qu_data[i][j] = int(cobj.get_text())
                
                j += 1
                if j == NUM_COLS:
                    i += 1
                    j = 0                   
                 
            n = (n + 1) % QU_TD_ROW_SIZE 
    
    def _qu_scraping(self):
        
        req = self._prepare_request(QU_URL)
    
        bsObj = self._check_url(QU_URL, req)
        
        self._process_qu_page(bsObj)
        
        print "Read: %d" % len(self._qu_data)
            
    # ------------------------------------- Q1 scraping.
    def _process_q1_page(self, bsObj):
        
        json_txt = str(bsObj.find(Q1_COBJ).get_text())
        
        json_data = json.loads(json_txt)
        
        for i in range(NUM_ROWS - 1):
            el = json_data[i]
            
            self._q1_data[i][0] = int(el[FIRST_FIELD])
            self._q1_data[i][1] = int(el[SECOND_FIELD])
            self._q1_data[i][2] = int(el[THIRD_FIELD])                        
    
    def _q1_scraping(self):
        
        # The ULR depends on the index received.  
        url = Q1_URL + self._index
        
        req = self._prepare_request(url)
    
        bsObj = self._check_url(url, req)
        
        print "Read: %d" % len(self._q1_data)
        
        self._process_q1_page(bsObj)    
    
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
                data[i][0] = CL_STR_CONVERT[temp_lst[i]]
            except KeyError as ke:
                print "ERROR: %s" % ke                  
           
        for i in range(len(CL_ELEMENTS)):            
            self._fill_cl_data(data, i + 1, size, bsObj, CL_ELEMENTS[i]) 
            
        return data            
    
    def _cl_scraping(self, url, size):
        
        req = self._prepare_request(url)
    
        bsObj = self._check_url(url, req)
        
        data = self._process_cl_page(bsObj, size)
        
        print "Read: %d" % len(data)
        
        return data  
    
    # ------------------------------------- Getting data from CL.     
    def _get_data_from_cl(self, cl_data, name):
        
        data = []
        
        for i in range(len(cl_data)):
            if cl_data[i][NAME_COL_CL] == name:
                return cl_data[i][NAME_COL_CL + 1:]
                
        return data        
    
    def get_data_from_b1(self, name, as_lo = True):
        
        data = self._get_data_from_cl(self._b1_data, name)
        
        if as_lo:
            return data[:NAME_DATA_LEN]
        else:
            return data[NAME_DATA_LEN:] 
    
    def get_data_from_a2(self, name, as_lo = True):
        
        data = self._get_data_from_cl(self._a2_data, name)   
        
        if as_lo:
            return data[:NAME_DATA_LEN]
        else:
            return data[NAME_DATA_LEN:]          
    
    # ------------------------------------- Properties.  
    @property
    def index(self):
        return self._index
                               
    @property
    def lm_data(self):    
        return self._lm_data
    
    @property
    def ve_data(self):    
        return self._ve_data
    
    @property
    def qu_data(self):    
        return self._qu_data
    
    @property
    def q1_data(self):    
        return self._q1_data
    
    @property
    def b1_data(self):    
        return self._b1_data
    
    @property
    def a2_data(self):    
        return self._a2_data
    
    @property
    def k_data(self):    
        return self._k_data 
    
    @property
    def pre_data_ok(self):
        return self._pre_data
    
    @property
    def post_data_ok(self):
        return self._post_data    
    
    def _save_scraping_data(self):
        
        out_file_name = SCRAPPED_DATA_FILE_PREFIX + self._index + \
            SCRAPPED_DATA_FILE_EXT
        
        f = open(out_file_name,'w')
        
        f.write("self._lm_data = %s\n\n" % str(self._lm_data))
        f.write("self._ve_data = %s\n\n" % str(self._ve_data))
        f.write("self._qu_data = %s\n\n" % str(self._qu_data))
        f.write("self._q1_data = %s\n\n" % str(self._q1_data))
        f.write("self._b1_data = %s\n\n" % str(self._b1_data))
        f.write("self._a2_data = %s\n" % str(self._a2_data))
        
        f.close()   
        
        print "Data scrapped saved in: %s" % out_file_name     

    def _get_res_file_name(self, index):
        
        return RES_FILE_PREFIX + index + INPUT_FILE_NAME_EXT
    
    def _save_res_data(self, file_name, data):
        
        f = open(file_name,'w')
        
        print data
        
        for d in data:
            f.write("%s\n" % str(d[0]))
        
        f.close() 
        
    def _scrap_res(self, max_range, file_dir, url_prefix, data_size): 
        
        for i in range(max_range):
            
            file_name = os.path.join(os.getcwd(), file_dir, \
                                     self._get_res_file_name(i))
            
            if not os.path.exists(file_name):     
                url = url_prefix + i   
                data = self._re_scraping(url)
                
                # If data could not be get, exit.
                if len(data) == data_size:                     
                    self._save_res_data(file_name, data)
                else:
                    break                     
    
    # ------------------------------------- Public functions. 
    def scrap_res_data(self):
        
        self._scrap_res(MAX_B1, RES_B1_DIR, RE_B1_URL, B1_SIZE / 2)
        
        self._scrap_res(MAX_A2, RES_A2_DIR, RE_A2_URL, A2_SIZE / 2)           
         
    def scrap_pre_data(self):
        """Scraping prior data.
        """
        
        self._k_data = self._k_scraping()
        
        self._b1_data = self._cl_scraping(CL_B1_URL, B1_SIZE)

        self._a2_data = self._cl_scraping(CL_A2_URL, A2_SIZE)
        
        if self._k_data == NUM_ROWS and self._b1_data == B1_SIZE and \
            self._a2_data == A2_SIZE:        
            self._pre_data = True
        
    def scrap_post_data(self):
        """Scraping posterior data.
        """

        self._lm_scraping()
   
        self._ve_scraping()

        self._qu_scraping()

        self._q1_scraping()
        
        # As a final step, save all the data scrapped.
        self._save_scraping_data()
        
        self._post_data = True        