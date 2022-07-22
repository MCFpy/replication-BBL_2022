# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 11:09:04 2022.

@author: HBusshoff
"""

# %%

import os
from mcf import modified_causal_forest

# %%

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
OUTPFAD = ROOT_DIR + '/data'
DATPFAD = OUTPFAD
INDATA = 'bw_data'

# %%

y_name = ['dbirwt']
d_name = ['d']
x_name_ord = ['dmage_cat', 'dmeduc', 'dfeduc']
x_name_unord = ['adequacy', 'alcohol', 'cntyfipb', 'deadkids_cat', 'dfage_cat',
                'dlivord_cat', 'dmar', 'foreignb', 'frace', 'mrace',
                'nprevist_cat', 'trimester', 'years_cat']
z_name_split_ord = ['dmage_cat']
z_name_split_unord = ['nprevist_cat', 'mrace']
z_name_mgate = z_name_split_ord
atet_flag = True
gatet_flag = False
l_centering = False
reduce_split_sample = True
reduce_split_sample_pred_share = 0.1
reduce_largest_group_train = True
reduce_largest_group_share = 0.1
_mp_ray_shutdown = True
_mp_ray_del = ('refs', 'rest')
cond_var_flag = True
boot = 1000
mp_parallel = 20

# %%

if __name__ == '__main__':
    modified_causal_forest(
        outpfad=OUTPFAD,
        datpfad=DATPFAD,
        indata=INDATA,
        y_name=y_name,
        d_name=d_name,
        x_name_ord=x_name_ord,
        x_name_unord=x_name_unord,
        atet_flag=atet_flag,
        gatet_flag=gatet_flag,
        l_centering=l_centering,
        z_name_split_ord=z_name_split_ord,
        z_name_split_unord=z_name_split_unord,
        z_name_mgate=z_name_mgate,
        reduce_split_sample=reduce_split_sample,
        reduce_split_sample_pred_share=reduce_split_sample_pred_share,
        reduce_largest_group_train=reduce_largest_group_train,
        reduce_largest_group_train_share=reduce_largest_group_share,
        _mp_ray_shutdown=_mp_ray_shutdown,
        _mp_ray_del=_mp_ray_del,
        cond_var_flag=cond_var_flag,
        mp_parallel=mp_parallel)
