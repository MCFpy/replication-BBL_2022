# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 13:40:13 2021.

@author: HBodory
"""

# %%

import os
from mcf import modified_causal_forest

# %%

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
OUTPFAD = ROOT_DIR + '/data'
DATPFAD = OUTPFAD
INDATA = 'data_rhc'

# %%

y_name = ['dth30']
d_name = ['swang1']
x_name_ord = ['adld3pc', 'age', 'alb1', 'amihx', 'aps1', 'bili1',
              'card', 'cardiohx', 'cat2_miss', 'chfhx',
              'chrpulhx', 'crea1', 'das2d3pc', 'dementhx', 'dnr1', 'edu',
              'gastr', 'gibledhx', 'hema', 'hema1', 'hrt1', 'immunhx',
              'income', 'liverhx', 'malighx', 'meanbp1', 'meta', 'neuro',
              'ortho', 'paco21', 'pafi1', 'ph1', 'pot1', 'psychhx',
              'renal', 'renalhx', 'resp', 'resp1', 'scoma1', 'seps', 'sex',
              'sod1', 'surv2md1', 'temp1', 'transhx', 'trauma', 'urin1',
              'urin1_miss', 'wblc1', 'wtkilo1']
x_name_unord = ['ca', 'cat1', 'cat2', 'ninsclas', 'race']

important_x_name_ordered = ['adld3pc', 'age', 'aps1', 'meanbp1', 'surv2md1',
                            'dnr1', 'scoma1']
important_x_name_unordered = ['cat1']

x_balance_name_ord = important_x_name_ordered
x_balance_name_unord = important_x_name_unordered
x_name_always_in_ord = important_x_name_ordered
x_name_always_in_unord = important_x_name_unordered
x_name_remain_ord = important_x_name_ordered
x_name_remain_unord = important_x_name_unordered

z_name_list = important_x_name_ordered[:5]
z_name_split_ord = important_x_name_ordered[5:]
z_name_split_unord = important_x_name_unordered
z_name_amgate = important_x_name_ordered + important_x_name_unordered
z_name_mgate = important_x_name_ordered + important_x_name_unordered

ATET_FLAG = True
GATET_FLAG = True
L_CENTERING = True
SE_BOOT_ATE = False
FS_YES = True
VARIABLE_IMPORTANCE_OOB = True
L_CENTERING_REPLICATION = True

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
        x_balance_name_ord=x_balance_name_ord,
        x_balance_name_unord=x_balance_name_unord,
        x_name_always_in_ord=x_name_always_in_ord,
        x_name_always_in_unord=x_name_always_in_unord,
        x_name_remain_ord=x_name_remain_ord,
        x_name_remain_unord=x_name_remain_unord,
        z_name_list=z_name_list,
        z_name_split_ord=z_name_split_ord,
        z_name_split_unord=z_name_split_unord,
        z_name_amgate=z_name_amgate,
        z_name_mgate=z_name_mgate,
        atet_flag=ATET_FLAG,
        gatet_flag=GATET_FLAG,
        l_centering=L_CENTERING,
        se_boot_ate=SE_BOOT_ATE,
        fs_yes=FS_YES,
        variable_importance_oob=VARIABLE_IMPORTANCE_OOB,
        l_centering_replication=L_CENTERING_REPLICATION)
