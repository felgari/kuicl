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

"""Common functions.
"""

import requests
import urllib2
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome"
FORMATS_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"

def prepare_request(url):
    
    session = requests.Session()
    
    headers = {"User-Agent": USER_AGENT, "Accept": FORMATS_ACCEPT}

    return session.get(url, headers=headers)    

def get_page(url, req):
    
    bsObj = None
    
    print "Reading page from: %s" % url
    
    try:    
        html = urllib2.urlopen(url)
    except HTTPError as he:
        print(he)
    except URLError as ue:
        print(ue)
    else:
        try:
            bsObj = BeautifulSoup(req.text)
        except AttributeError as ae:
            print(ae)
            
    return bsObj