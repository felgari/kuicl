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

"""Script to get a summary of previous data.
"""

import csv

from ctes import *

def read_file(file_name):
    
    data = []
    
    try:
        with open(file_name, "rb") as fr:
            
            reader = csv.reader(fr, delimiter=',', quotechar='"')        
            
            for row in reader:   
                 
                data.append(row)
                
    except csv.Error:
        print "Error reading data from CSV file: '%s'" % file_name 
                
    except IOError:
        print "Error reading CSV file: '%s'" % file_name     
    
    return data

def get_label_and_match(row):
    
    values = [ int(row[i]) for i in range(SUM_P1_COL, SUM_P3_COL + 1) ]
    
    maxi = max(values)
    index_maxi = values.index(maxi) + SUM_P1_COL
    
    mini = min(values)
    index_mini = values.index(mini) + SUM_P1_COL
    
    res_pos = HIST_CONV[row[SUM_R_COL]]
    
    if maxi >= HIST_MAX_P:
        label = LAB_1_OP          
    elif mini <= HIST_MIN_P:
        label = LAB_3_OP
    else:
        label = LAB_2_OP
        
    if res_pos == index_maxi:
        match = RES_IS_FIRST
    elif res_pos == index_mini:
        match = RES_IS_THIRD
    else:
        match = RES_IS_SECOND
        
    return label, match

def calc_labels_and_match(data):
    
    for d in data:
        label, match = get_label_and_match(d)
        
        d.append(label)
        d.append(match)
        
def inc_p(sum_p, val):
    
    if val == RES_IS_FIRST:
        sum_p[0] += 1
    elif val == RES_IS_SECOND:
        sum_p[1] += 1
    else:
        sum_p[2] += 1
        
def gen_ratio(sum_p):
    
    su = sum(sum_p)
    
    if su > 0:
        return [ int(100 * x / su) for x in sum_p ]
    else:
        return sum_p
        
def summary(data):
    
    num_of_p = [0] * 3
    sum_1p = [0] * 3
    sum_2p = [0] * 3
    sum_3p = [0] * 3
    
    calc_labels_and_match(data)
    
    for d in data:
        if d[SUM_LABEL_COL] == LAB_1_OP:
            num_of_p[0] += 1
            inc_p(sum_1p, d[SUM_MATCH_COL])
        elif d[SUM_LABEL_COL] == LAB_2_OP:
            num_of_p[1] += 1
            inc_p(sum_2p, d[SUM_MATCH_COL])
        else:
            num_of_p[2] += 1
            inc_p(sum_3p, d[SUM_MATCH_COL])
    
    print "Number of each type: %s" % gen_ratio(num_of_p)
    print "Cases for 1p: %s" % gen_ratio(sum_1p)
    print "Cases for 2p: %s" % gen_ratio(sum_2p)
    print "Cases for 3p: %s" % gen_ratio(sum_3p)
        
def generate_summary(data):
    
    l_list = list(set([ d[HIST_L_COL] for d in data]))
    
    for l in l_list:
        print "Summary for: %s" % l
        
        l_data = [ [ d[i] for i in HIST_SUM_COLS] for d in data if d[HIST_L_COL] == l ]
        
        summary(l_data)

def main():
    
    hist_data = read_file(AP_HIST_FILE)

    if len(hist_data) > 0:
        generate_summary(hist_data)

if __name__ == "__main__":
    
    main()