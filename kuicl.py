#!/usr/bin/env python
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

"""Main module, calculations made with local data and data scrapped from 
web pages.
"""

import sys

from ctes import *
from kparser import *
from kdat import KDat
from clda import ClDat
from pro import Pro
from pre import Pre
from pdat import PDat
from resd import retrieve_res
from ap import calculate_ap
from prun import do_prun
from extd import ExtD
from report import report_generated, do_report 

def load_source_data(index):
    
    success = True
    
    k = KDat(index)
    
    if k.loaded:
        print "K data loaded successfully for index %s" % k.index
        cl = ClDat(k.index)
        
        if cl.loaded:
            print "Cl data loaded successfully."
        else:
            print "ERROR: Cl data not loaded."
            success = False
    else:
        print "ERROR: k data not loaded."
        success = False
        
    return success, k, cl

def generate_p(k, cl, force_calc):
    
    success = True
 
    pro = Pro(k.index, k.k, cl.b1, cl.a2, force_calc)
    
    pre = Pre(k.index, k.k, cl.b1, cl.a2, force_calc)
    
    p = None
    
    if pro.generated:
        if pre.generated:
            p = PDat(k.index, k.k, pro.pro, pre.pre, cl.b1, cl.a2, force_calc)
        else:
            print "ERROR: pre not generated."
            success = False
    else:
        print "ERROR: pro not generated."
        success = False
        
    return success, pro, pre, p

def generate_ap(k, p_data, index):
    
    ap_data = []
    
    for i, fd in enumerate(p_data):
        ap_data.append([k[i][TYPE_COL]] + fd)
    
    calculate_ap(ap_data, index)

def main(progargs):
    """Main function.
    """    
    
    if progargs.retrieve_res:
        print "Retrieving res ..."
        retrieve_res()
    
    if progargs.index != DEFAULT_INDEX:
        print "Let's go with index %s ..." % progargs.index
    else:
        print "Let's go without index ..."
        
    success, k, cl = load_source_data(progargs.index)
        
    if success:
        success, pro, pre, p = generate_p(k, cl, progargs.force_calc)    
                    
        if success:
            generate_ap(k.k, p.p, k.index)
            
            print "Calculating prun ..."     
            do_prun(k.index, k.k, pro.pro)
            
            print "Loading external data ..."
            extd = ExtD(k.index)
            
            extd.load_data()
            
        if progargs.force_calc or not report_generated(k.index):
            do_report(k.index, k.k)
    else:
        print "Source data couldn't be loaded, nothing calculated."
        
    print "Program finished."
    
    return 0

# Where all begins ...
if __name__ == "__main__":
    
    try:
        # Object to process the program arguments.
        progargs = ProgramArguments()
        
        sys.exit(main(progargs))   
    except ProgramArgumentsException as pae:
        print pae       
