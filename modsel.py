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

"""Script to select between models using cross validation.
"""

import numpy as np
from sklearn import cross_validation

from ctes import *
from clda import ClDat
from kfiles import read_res_file, save_data_to_csv

def generate_data(name, res, cl, is_lo):
    
    data = []
    target = []
    
    if is_lo:
        res_col = R_NAME_2_COL
        cl_cols = VI_P_RANGE
    else:
        res_col = R_NAME_1_COL
        cl_cols = LO_P_RANGE
        
    for r in res:
        cl_data = [c for c in cl if c[CL_NAME_COL] == r[res_col]][0]
        
        new_row = [int(r[R_J_COL]), cl_data[CL_POS_COL]]
        new_row.extend([cl_data[i] for i in cl_cols])
        
        data.append(new_row)
        
        target.append(r[R_M_COL])
        
    target_int = [TARGET_TO_NUM[t] for t in target]
        
    return np.array(data), np.array(target)

def evaluate_models(name, res, cl, is_lo):
    
    data, target = generate_data(name, res, cl, is_lo)
    
    best_models = []
    
    best_mean_score = 0.0
    best_std_score = 0.0
    
    for clf_name, clf, i in zip(CL_NAMES, CLS, range(len(CL_NAMES))):
    
        scores = cross_validation.cross_val_score(clf, data, target, \
                                                  cv=CV_NUM_SETS)
        
        #print("Accuracy of %s: %0.2f (+/- %0.2f)" % \
              #(clf_name, scores.mean(), scores.std() * 2))
        
        if not len(best_models):
            best_models.append(i)
            best_mean_score = scores.mean()
            best_std_score = scores.std()
        elif best_mean_score - EPS < scores.mean() < best_mean_score + EPS:
            if scores.std() + EPS < best_std_score:
                best_models = [i]
                best_mean_score = scores.mean()
                best_std_score = scores.std()        
            elif best_std_score - EPS < scores.std() < best_std_score + EPS:
                best_models.append(i)
        elif best_mean_score + EPS < scores.mean():
            best_models = [i]
            best_mean_score = scores.mean()
            best_std_score = scores.std()
            
    #print "Best models (%0.2f): %s" % \
    #    (best_mean_score, [CL_NAMES[i] for i in best_models])
        
    return [best_mean_score] + best_models

def evaluate_all_models(cl, res):
    
    mdls = []
    
    for c in cl:
        name = c[CL_NAME_COL]
        
        lo_res = [ r for r in res if r[R_NAME_1_COL] == name ]
        lo_mdls = evaluate_models(name, lo_res, cl, True)
        
        vi_res = [ r for r in res if r[R_NAME_2_COL] == name ]
        vi_mdls = evaluate_models(name, vi_res, cl, False)
        
        mdl = [name]
        mdl.extend(lo_mdls)
        mdl.extend(vi_mdls)
        
        mdls.append(mdl)
        
    return mdls

def main():
    
    clda = ClDat()
    
    if clda.loaded:
    
        b1_res = read_res_file(B1_RES_FILE)
        a2_res = read_res_file(A2_RES_FILE)
        
        if len(b1_res) and len(a2_res):
            mdls_b1 = evaluate_all_models(clda.b1, b1_res)
            mdls_a2 = evaluate_all_models(clda.a2, a2_res)
            
            save_data_to_csv(MODELS_FILENAME, mdls_b1 + mdls_a2)
        else:
            print "Res data couldn't be read."
    else:
        print "Cl data couldn't be loaded."

if __name__ == "__main__":
    main()