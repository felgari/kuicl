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
import json
from ctes import *

class QScraping(object):
    """Scraping on some web pages.
    """
    
    def __init__(self, index):
        """Constructor.
        
        Args:
            index: Index used for the scraping.
                        
        """    
        
        self._index = index
        
        self._lm_data = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    
        self._ve_data = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    
        self._qu_data = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    
        self._q1_data = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    
        self._b1_data = []
    
        self._a2_data = []    
    
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
    
    # ------------------------------------- LM scraping.    
    def _process_lm_page(self, bsObj):
        
        i = 0
        j = 0
        n = 0
        
        for table in bsObj.findAll("table"):
            for td_center in table.findAll("td", LM_DICT):        
                    
                if i == NUM_ROWS:
                    return 
                
                elif n >= LM_FIRST_COL and n <= LM_LAST_COL:
    
                    self._lm_data[i][j] = int(td_center.get_text().strip())
                    
                    j += 1
                    if j == NUM_COLS:
                        i += 1
                        j = 0                   
                     
                n = (n + 1) % LM_TD_ROW_SIZE
    
    def _lm_scraping(self):
        
        req = self._prepare_request(LM_URL)
    
        bsObj = self._check_url(LM_URL, req)
        
        self._process_lm_page(bsObj)
        
    # ------------------------------------- VE scraping.        
    def _process_ve_page(self, bsObj):

        i = 0
        j = 0    
        
        for div in bsObj.findAll("div", VE_DICT):
            for div2 in div.findAll("div"):
                txt = div2.get_text()
                
                self._ve_data[i][j] = int(txt[:len(txt) - 1])
                
                j += 1
                if j == NUM_COLS:
                    i += 1
                    j = 0      
    
    def _ve_scraping(self):
        
        req = self._prepare_request(VE_URL)
    
        bsObj = self._check_url(VE_URL, req)
        
        self._process_ve_page(bsObj)

    # ------------------------------------- QU scraping.
    def _process_qu_page(self, bsObj):
        
        i = 0
        j = 0   
        n = 0 
        
        for td in bsObj.findAll("td", QU_DICT):
            
            if i == NUM_ROWS - 1:
                return
            
            elif n >= QU_FIRST_COL and n <= QU_LAST_COL:
    
                self._qu_data[i][j] = int(td.get_text())
                
                j += 1
                if j == NUM_COLS:
                    i += 1
                    j = 0                   
                 
            n = (n + 1) % QU_TD_ROW_SIZE
    
    def _qu_scraping(self):
        
        req = self._prepare_request(QU_URL)
    
        bsObj = self._check_url(QU_URL, req)
        
        self._process_qu_page(bsObj)
            
    # ------------------------------------- Q1 scraping.
    def _process_q1_page(self, bsObj):
        
        json_txt = str(bsObj.find("body").get_text())
        
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
        
        self._process_q1_page(bsObj)    
    
    # ------------------------------------- CL scraping.
    def _fill_cl_data(self, data, index, size, bsObj, td_class):
        
        temp_lst = []
        
        for td in bsObj.findAll("td", td_class):        
            temp_lst.append(td.get_text())  
            
        for i in range(size):
            data[i][index] = int(temp_lst[i])                  
    
    def _process_cl_page(self, bsObj, size):
        
        data = [[0 for _ in range(NUM_COLS_CL)] for _ in range(size)]
        
        temp_lst = []        
        
        for td in bsObj.findAll("td", CL_EQ_DICT):        
            temp_lst.append(td.get_text()) 
            
        for i in range(size):
            try:
                data[i][0] = CL_STR_CONVERT[temp_lst[i]]
            except KeyError as ke:
                print "ERROR: %s" % ke                  
           
        for i in range(len(CL_TD_CLASSES)):            
            self._fill_cl_data(data, i + 1, size, bsObj, CL_TD_CLASSES[i])                                     
            
        return data            
    
    def _cl_scraping(self, url, size):
        
        req = self._prepare_request(url)
    
        bsObj = self._check_url(url, req)
        
        data = self._process_cl_page(bsObj, size)
        
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
    
    # ------------------------------------- Public functions.    
    def do_scraping(self):
        """Do all the scraping.
        """

        self._lm_scraping()
   
        self._ve_scraping()

        self._qu_scraping()

        self._q1_scraping()

        self._b1_data = self._cl_scraping(CL_B1_URL, B1_SIZE)

        self._a2_data = self._cl_scraping(CL_A2_URL, A2_SIZE)