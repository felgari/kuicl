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

"""Script to do something.
""" 

import sys
import csv
import operator

FILE_NAME = 'pro.csv'
FIRST_NAME = 'A'
SECOND_NAME = 'B'
THIRD_NAME = 'C'

ROW_NAME = 'i'
COL_NAME = 'j'

MULT = 0.75
VALUE_LIMIT = 19
MULT_LIMIT = 40
COMB = [ [0, 3], [2 ,2], [5, 0], [7, 0], [3, 3] ]

COMPLEMENT = { 'A':'C', 'B':'ABC', 'C':'AB', 'AB':'BC', 'BC':'A', 'AC':'B', 'ABC': 'B' }

def read_data():
    
    data = []
    
    with open(FILE_NAME, 'rb') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                
                row_num = []
                
                for e in row:
                    row_num.append(int(e))
                
                data.append(row_num)
        
        except csv.Error:
            print "ERROR: reading file %s" % FILE_NAME
            
    return data

def get_name(value):
    
    if value == 0:
        name = FIRST_NAME
    elif value == 1:
        name = SECOND_NAME
    else:
        name = THIRD_NAME    
             
    return name

def get_base(data):
    num_row = len(data)
    num_col = len(data[0])    
    
    data_control = [[False for _ in range(num_col)] for _ in range(num_row)]
    base = []
    
    for i in range(num_row):
        
        max_val = 0
        num_max = 0
        
        for j in range(num_col):
            if data[i][j] > max_val:
                max_val = data[i][j]
                num_max = j
        
        data_control[i][num_max] = True
        
        base.append(get_name(num_max))
    
    return data_control, base

def get_data_rest(data, data_control):
    num_row = len(data)
    num_col = len(data[0])      
    
    data_rest = dict()
    for i in range(num_row):
        for j in range(num_col):
            if not data_control[i][j]:
                key = "%s%d%s%d" % (ROW_NAME, i, COL_NAME, j)
                data_rest[key] = data[i][j]
    
    sorted_data_rest = sorted(data_rest.items(), key=operator.itemgetter(1), reverse=True)
    
    return sorted_data_rest

def get_row_col(key):
    row_pos = key.find(ROW_NAME)
    
    col_pos = key.find(COL_NAME, row_pos)
    
    row = int(key[row_pos + 1: col_pos])
    col = int(key[col_pos + 1:])
    
    return row, col

def calculate_cost(data):
    
    do = 0
    tr = 0
    calc = 1
    
    for e in data:
        l = len(e)
        if l == 2:
            do += 1
        elif l == 3:
            tr += 1
            
        calc *= l
                
    return calc, do, tr

def possible_data(do, tr):
    
    poss = False
    val =  [do, tr]
    
    for n in COMB:
        if val[0] <= n[0] and val[1] <= n[1]:
            poss = True
        
    return poss

def get_ap(base, data_rest):

    cost = 0
    i = 0
    do = 0
    tr = 0
    
    while cost < MULT_LIMIT or possible_data(do, tr):
        pair = data_rest[i]
        key = pair[0]
        value = pair[1]    
        i += 1
        
        if value > VALUE_LIMIT or possible_data(do, tr):
            row, col = get_row_col(key)
            
            name = get_name(col)
            
            new_base = base[:]
            
            new_base[row] = new_base[row] + name
            
            cost, do, tr = calculate_cost(new_base)
        
            if cost < MULT_LIMIT or possible_data(do, tr):
                base = new_base
            else:
                break
        else:
            break
        
    for i in range(len(base)):
        base[i] = ''.join(sorted(base[i]))
        
    return base

def ap(data):
    
    data_control, base = get_base(data)
        
    data_rest = get_data_rest(data, data_control)
    
    ap_data = get_ap(base, data_rest)
    
    return ap_data 

def complementary(data):
    
    comp = []
    
    for d in data:
        comp.append(COMPLEMENT[d])
    
    return comp

def main():
    """Main function.

    """    

    data = read_data()
            
    ap_data = ap(data)
    
    print ap_data
    
    comp_ap_data = complementary(ap_data)
    
    print comp_ap_data
        
    print "Program finished."
    
    return 0

# Where all begins ...
if __name__ == "__main__":
    
    sys.exit(main())      