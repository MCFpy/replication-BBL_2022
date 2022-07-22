# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 19:22:40 2021.

@author: HBodory
"""

# %%

import os
from mcf import modified_causal_forest

# %%

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
OUTPFAD = ROOT_DIR + '/data'
DATPFAD = OUTPFAD
INDATA = 'data_wia'

# %%

y_name = ['earnings']
d_name = ['mtreat']
x_name_ord = ['age', 'asian', 'black', 'disab', 'educ_col', 'educ_nod',
              'educ_sec', 'emp_b1', 'emp_b2', 'emp_b3', 'female', 'latino',
              'lowinc', 'uc', 'unemp', 'vet', 'wage_b1', 'wage_b2',
              'wage_b3', 'white']
x_name_unord = ['occup', 'sec_b1', 'sec_b2', 'sec_b3']

important_x_name_ordered = ['age', 'uc']

x_balance_name_ord = important_x_name_ordered
x_name_always_in_ord = important_x_name_ordered
x_name_remain_ord = important_x_name_ordered

z_name_list = important_x_name_ordered[:1]
z_name_split_ord = important_x_name_ordered[1:]
z_name_amgate = important_x_name_ordered
z_name_mgate = important_x_name_ordered

ATET_FLAG = True
GATET_FLAG = True
L_CENTERING = True
SE_BOOT_ATE = False
FS_YES = True
VARIABLE_IMPORTANCE_OOB = True
_MP_RAY_SHUTDOWN = False
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
        x_name_always_in_ord=x_name_always_in_ord,
        x_name_remain_ord=x_name_remain_ord,
        z_name_list=z_name_list,
        z_name_split_ord=z_name_split_ord,
        z_name_amgate=z_name_amgate,
        z_name_mgate=z_name_mgate,
        atet_flag=ATET_FLAG,
        gatet_flag=GATET_FLAG,
        l_centering=L_CENTERING,
        se_boot_ate=SE_BOOT_ATE,
        fs_yes=FS_YES,
        variable_importance_oob=VARIABLE_IMPORTANCE_OOB,
        _mp_ray_shutdown=_MP_RAY_SHUTDOWN,
        l_centering_replication=L_CENTERING_REPLICATION)
