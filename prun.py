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

"""Script to generate results from previous evaluations.
"""

import sys
import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

from ctes import *
from ap import calculate_ap

NUM_ARGS = 2

def read_hist_data(file_name):
    
    data = []
    
    print "Reading historic file: %s" % file_name
    
    try:
        with open(file_name, "rb") as fr:
            
            reader = csv.reader(fr, delimiter=',', quotechar='"')        
            
            for row in reader:   
                 
                data.append([int(x) if i != HIST_PRED_R_COL and len(x) 
                             and x.isdigit() 
                             else x for i, x in enumerate(row)])
                
        print "Read %d lines from : %s" % (len(data), file_name)
                
    except csv.Error:
        print "Error reading data from CSV file: '%s'" % file_name 
                
    except IOError:
        print "Error reading CSV file: '%s'" % file_name     
    
    return data

def is_pre(hist_row):
    
    r = hist_row[HIST_PRED_R_COL]
    data_ref = hist_row[HIST_PRED_REF_FIRST_COL:HIST_PRED_REF_LAST_COL]
    
    r_pos = NAMES_AP_STR.find(r)
    min_pos = data_ref.index(min(data_ref))
    
    return r_pos != min_pos

def save_res(data, out_file_name):
    
    file_name = out_file_name
    
    try:                
        with open(file_name, 'wb') as fw:
            
            writer = csv.writer(fw, delimiter=',')
            
            for d in data:
                writer.writerow(d)            
               
    except csv.Error:
        print "Error writing data in CSV file: '%s'" % file_name                
                
    except IOError:
        print "Error writing CSV file: '%s'" % file_name 
        
def process_input_data(data):
    
    hist_data = []
    cl_data = []
    
    for d in data:
        hist_data.append(d[HIST_PRED_FIRST_COL:])
        cl_data.append(d[HIST_PRED_R_COL])
    
    return hist_data, cl_data  

def _get_val_index(values, order, sort_values, name):
    
    try:
        i = order.index(name)
        sort_values.append(values[i])
    except ValueError:
        sort_values.append(0)

def _sort_pre_values(values, order):
    
    sort_values = []
    
    _get_val_index(values, order, sort_values, FIRST_NAME)
    _get_val_index(values, order, sort_values, SECOND_NAME)
    _get_val_index(values, order, sort_values, THIRD_NAME)                
                
    return sort_values  

def link_perc_to_cl(prd, cl):
    
    data_out = []
    
    for p in prd:
        
        sort_pre_val = _sort_pre_values(p, cl)
        
        data_out.append([int(100 * x) for x in sort_pre_val])
        
    return data_out

def predict_rf(hist_data, data_to_predict, cl_data):
    
    np_hist_data = np.matrix(hist_data)
    np_classes_data = np.array(cl_data)
    np_prd_data = np.matrix(data_to_predict)
    
    rf = RandomForestClassifier(n_estimators=RF_NUM_ESTIMATORS_PRUN, 
        random_state=RF_SEED)
    
    rf.fit(np_hist_data, np_classes_data)
    
    score = metrics.accuracy_score(np_classes_data, rf.predict(np_hist_data))
    print("Accuracy RF: %f" % score)
    
    prd = rf.predict_proba(np_prd_data)

    return link_perc_to_cl(prd, np.ndarray.tolist(rf.classes_))

def predict(to_predict, pred_data):
    
    data_out = []
        
    hist_data, cl_data = process_input_data(pred_data)
    
    data_to_predict = [d[DAT_PRED_FIRST_COL:] for d in to_predict]
    
    if len(hist_data) and len(data_to_predict):
        
        data_out = predict_rf(hist_data, data_to_predict, cl_data)
        
    return data_out
        
def generate_pred(data_to_predict, pre_data, index):  
    
    pre_data_t1 = [x for x in pre_data if x[HIST_PRED_L_COL] == int(TYPE_1_COL)]
    pre_data_t2 = [x for x in pre_data if x[HIST_PRED_L_COL] == int(TYPE_2_COL)]    
    
    data_t1 = [x for x in data_to_predict if x[HIST_PRED_L_COL] == int(TYPE_1_COL)]
    data_t2 = [x for x in data_to_predict if x[HIST_PRED_L_COL] == int(TYPE_2_COL)]
    
    pred_out_1 = predict(data_t1, pre_data_t1)
    pred_out_2 = predict(data_t2, pre_data_t2)    
    
    pred_out = pred_out_1 + pred_out_2
        
    save_res(pred_out, PRED_OUT_FILE_NAME_PREFIX + index + PRED_OUT_FILE_EXT)  
    
    return pred_out

def generate_ap(index_name, data_to_predict, final_pred):
    
    pre_data_for_ap = []

    for i, dtp in enumerate(data_to_predict):
        pre_data_for_ap.append([dtp[HIST_PRED_L_COL]] + final_pred[i])
    
    return calculate_ap(pre_data_for_ap, index_name)  
    
def compile_un_data(data_to_predict, src_hist_data, pro_data):
    
    hist_data = []
    cl_data = []
    
    for d in src_hist_data:
        r = d[HIST_PRED_R_COL]
        col = UN_HIST_CONV[r]
        r_val = int(d[col])
        is_un = 1 if r_val < UN_MIN_VAL else 0
        row = [HIST_NAME_CONVERT[d[HIST_UN_LO_COL]], 
            HIST_NAME_CONVERT[d[HIST_UN_VI_COL]], 
            d[HIST_UN_FIRST_COL], 
            d[HIST_UN_FIRST_COL + 1], 
            d[HIST_UN_FIRST_COL + 2]]
        cl_data.append(is_un)
        hist_data.append(row)
    
    to_pred = []
    for dtp, pd in zip(data_to_predict, pro_data):
        row = [HIST_NAME_CONVERT[dtp[K_NAME_1_COL]], 
            HIST_NAME_CONVERT[dtp[K_NAME_2_COL]]]
        row.extend(pd)
        to_pred.append(row)
    
    return hist_data, cl_data, to_pred, dtp

def save_un(data_to_predict, prd, index):
    
    file_name = UN_FILE_NAME_PREFIX + index + UN_OUT_FILE_EXT
    
    print "Saving UN in file: %s" % file_name
    
    try:
        with open(file_name, "w") as f:
    
            for p, dtp in zip(prd, data_to_predict):
            
                if len(p) > 1:
                    perc = 100 * p[1]
                
                    if perc > UN_RES_MIN_VAL:
                        f.write("%s -> %d%%\n" % (dtp, perc))
    
    except IOError as ioe:
        print "Error saving text file: '%s'" % file_name

def generate_un(data_to_predict, hist_data, cl_data, to_pred, index):
    
    np_hist_data = np.matrix(hist_data)
    np_classes_data = np.array(cl_data)
    np_prd_data = np.matrix(to_pred)
    
    rf = RandomForestClassifier(n_estimators=RF_NUM_ESTIMATORS_PRUN, 
        random_state=RF_SEED)
    
    rf.fit(np_hist_data, np_classes_data)
    
    prd = rf.predict_proba(np_prd_data)
    
    save_un(data_to_predict, prd, index)  
    
    un = [int(100 * x[1]) for x in prd] 
    
    return un

def calculate_un(data_to_predict, hist_data, pro_data, index):  
    
    un = []  
    
    src_hist_data = [x for x in hist_data if len(x[HIST_PRED_R_COL])]
    
    if len(data_to_predict):
        if len(src_hist_data):
            if len(pro_data):
                hist_data, cl_data, to_pred, dtp = \
                    compile_un_data(data_to_predict,
                                    src_hist_data,
                                    pro_data)
        
                un = generate_un(data_to_predict, hist_data, cl_data, to_pred, 
                                 index)
            else:
                print "ERROR: No pro data to calculate UN"
        else:
            print "ERROR: No historic data to calculate UN"
    else:
        print "ERROR: No data to calculate UN"
        
    return un

def do_prun(index, k, pro):
    
    hist_data = read_hist_data(AP_HIST_FILE)
    
    data_to_pred = [x[:HIST_PRED_REF_LAST_COL] 
                       for x in hist_data if not len(x[HIST_PRED_R_COL])]
    
    data_for_pred = [x[:HIST_PRED_REF_LAST_COL] 
                       for x in hist_data if len(x[HIST_PRED_R_COL])]
    
    final_pred = generate_pred(data_to_pred, data_for_pred, index) 
          
    ap_data, comp_ap_data = \
        generate_ap(index + AP_FILE_PRE_NAME_SUFFIX, data_to_pred, final_pred)     

    un = calculate_un(k, hist_data, pro, index)
    
    return final_pred, ap_data, un