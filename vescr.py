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

"""Functions to scrap VE.
"""

from bs4 import BeautifulSoup
from common import *
from ctes import *

def process_page(bsObj):
    
    ve_data = [[0 for x in range(NUM_COLS)] for x in range(NUM_ROWS)]
    
    i = 0
    j = 0    
    
    for div in bsObj.findAll("div", VE_DICT):
        for div2 in div.findAll("div"):
            txt = div2.get_text()
            
            ve_data[i][j] = int(txt[:len(txt) - 1])
            
            j += 1
            if j == NUM_COLS:
                i += 1
                j = 0               
        
    return ve_data

def ve_scraping():
    """
    """
    
    req = prepare_request(VE_URL)

    bsObj = get_page(VE_URL, req)
    
    lm_data = process_page(bsObj)
    
    return lm_data