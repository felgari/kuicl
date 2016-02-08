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

"""Functions to scrap LM.
"""

from bs4 import BeautifulSoup
from common import *
from ctes import *

def process_page(bsObj):
    
    lm_data = [[0 for x in range(NUM_COLS)] for x in range(NUM_ROWS)]
    
    i = 0
    j = 0
    n = 0
    
    for table in bsObj.findAll("table"):
        for td_center in table.findAll("td", LM_DICT):        
                
            if i == NUM_ROWS:
                return lm_data
            
            elif n >= LM_FIRST_COL and n <= LM_LAST_COL:

                lm_data[i][j] = int(td_center.get_text().strip())
                
                j += 1
                if j == NUM_COLS:
                    i += 1
                    j = 0                   
                 
            n = (n + 1) % LM_TD_ROW_SIZE

def lm_scraping():
    """
    """
    
    req = prepare_request(LM_URL)

    bsObj = get_page(LM_URL, req)
    
    lm_data = process_page(bsObj)
    
    return lm_data