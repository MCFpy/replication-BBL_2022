# -*- coding: utf-8 -*-
"""
Created on Fri May 13 16:35:59 2022.

@author: HBodory
"""

# %% Libraries


import pandas as pd
import numpy as np
import output_functions as of  # User-defined functions


# %% Parameters

DIRECTORY_WIA = 'mcf_output/wia0/'
DIRECTORY_RHC = 'mcf_output/rhc0/'
DIRECTORY_BW = 'mcf_output/bw0/'
INPUT_FOLDERNAME = 'fig_csv/'
OUTPUT_FOLDERNAME_FIG = 'figures/'
OUTPUT_FOLDERNAME_TAB = 'tables/'

# %% Plots: Sorted IATEs minus ATE

INPUT_FILENAME = 'SortedDTH30LC1vs0_iatemate'
df = pd.read_csv(DIRECTORY_RHC + INPUT_FOLDERNAME + INPUT_FILENAME + '.csv')
fig = of.plot_sorted_iates_minus_ate(df, ylabel='change in mortality')
fig.savefig(OUTPUT_FOLDERNAME_FIG + 'fig_3.png', dpi=1000)
# %% Plots: Density of IATEs

# BW
D_BASE = 0
D_CARD = 6
FILE_NAME = DIRECTORY_BW + 'fig_csv/' + 'DensityDBIRWT'
fig = of.plot_densities_new(file_name=FILE_NAME, d_base=D_BASE,
                            d_card=D_CARD)
fig.savefig(OUTPUT_FOLDERNAME_FIG + 'fig_1.png', dpi=200)

# WIA
D_BASE = 1
D_CARD = 4
FILE_NAME = DIRECTORY_WIA + 'fig_csv/' + 'DensityEARNINGSLC'
fig = of.plot_densities_new(file_name=FILE_NAME, d_base=D_BASE,
                            d_card=D_CARD)
fig.savefig(OUTPUT_FOLDERNAME_FIG + 'fig_7.png', dpi=200)

# RHC
D_BASE = 0
D_CARD = 2
FILE_NAME = DIRECTORY_RHC + 'fig_csv/' + 'DensityDTH30LC'
fig = of.plot_densities_new(file_name=FILE_NAME, d_base=D_BASE,
                            d_card=D_CARD, ate=0.048021, ate_y=True)
fig.savefig(OUTPUT_FOLDERNAME_FIG + 'fig_5.png', dpi=200)
# %% Plots: GATE minus ATE

# BW
FLAG_CATEGORICAL = True
value_labels = ['', "Other", "", "Black", '', "Hispanic", '', "White"]
INPUT_FILENAME = 'GATEMRACEPRAllDBIRWT5vs0'
FLAG_GATE = True
label = ['race mother', 'change in birthweight']
df = pd.read_csv(DIRECTORY_BW + INPUT_FOLDERNAME + INPUT_FILENAME + '.csv')
fig = of.gen_gate_fig(df, label, categorical=FLAG_CATEGORICAL,
                      gate=FLAG_GATE, value_labels=value_labels)
fig.savefig(OUTPUT_FOLDERNAME_FIG + 'fig_2.png')

# WIA
FLAG_CATEGORICAL = False
INPUT_FILENAME = 'GATEMATEAGEAllEARNINGSLC3vs1'
label = ['age', 'change in earnings']
FLAG_GATE = False
df = pd.read_csv(DIRECTORY_WIA + INPUT_FOLDERNAME + INPUT_FILENAME + '.csv')
fig = of.gen_gate_fig(df, label, categorical=FLAG_CATEGORICAL,
                      gate=FLAG_GATE)
fig.savefig(OUTPUT_FOLDERNAME_FIG + 'fig_6.png')

# RHC
INPUT_FILENAME = 'GATEMATEMEANBP1AllDTH30LC1vs0'
FLAG_GATE = False
label = ['mean blood pressure', 'change in mortality']
df = pd.read_csv(DIRECTORY_RHC + INPUT_FOLDERNAME + INPUT_FILENAME + '.csv')
fig = of.gen_gate_fig(df, label, categorical=FLAG_CATEGORICAL,
                      gate=FLAG_GATE)
fig.savefig(OUTPUT_FOLDERNAME_FIG + 'fig_4.png')

# %% Tables: Total and marginal group effects

NUMBER_OF_STATS = 3  # Effects and lower/upper confidence bounds.
NUMBER_OF_DECIMAL_PLACES = 2  # Decimals for statistics
MULTIPLIER_ROWS = 2  # Multiplier to print confidence intervals.

# BW

colnames = ['GATE', 'GATE-ATE']
effects = ['GATEDMAGE_CATAllDBIRWT', 'GATEMATEDMAGE_CATAllDBIRWT',
           'GATEMRACEPRAllDBIRWT', 'GATEMATEMRACEPRAllDBIRWT',
           'GATENPREVIST_CATPRAllDBIRWT', 'GATEMATENPREVIST_CATPRAllDBIRWT']

NUMBER_OF_TREATMENTS = 5
FIRST_TREATMENT_LEVEL = 0  # First level of treatment variable.
NUMBER_OF_COMBI = 15  # Number of possible treatment combinations.
params = {}
params['number_of_treatments'] = NUMBER_OF_TREATMENTS
params['number_of_stats'] = NUMBER_OF_STATS
params['first_level_of_treatment_variable'] = FIRST_TREATMENT_LEVEL
params['treatment_names'] = of.generate_treatment_names(
    FIRST_TREATMENT_LEVEL, NUMBER_OF_TREATMENTS)
params['number_of_decimal_places'] = NUMBER_OF_DECIMAL_PLACES

for tab_no, name in enumerate(effects):
    params['directory_effect'] = DIRECTORY_BW + INPUT_FOLDERNAME + name
    stats_table = of.generate_gate_table(params)
    df = of.create_dataframe_for_results(stats_table, n_1=MULTIPLIER_ROWS,
                                         n_2=NUMBER_OF_STATS)
    for i in range(0, df.shape[0], MULTIPLIER_ROWS):
        for j in range(df.shape[1]):
            df.iloc[i, j] = stats_table.iloc[int(i / MULTIPLIER_ROWS), j]
            CINT = of.create_confidence_interval(
                stats_table.iloc[int(i / MULTIPLIER_ROWS),
                                 j + NUMBER_OF_COMBI],
                stats_table.iloc[int(i / MULTIPLIER_ROWS),
                                 j + 2 * NUMBER_OF_COMBI])
            df.iloc[i + 1, j] = CINT
        if df.index[i] == int(df.index[i]):  # No decimal value if integer.
            idx_list = df.index.tolist()
            df.index = idx_list[:i] + [int(df.index[i])] + idx_list[i + 1:]
    df.to_csv(OUTPUT_FOLDERNAME_TAB + 'suppl_table_' + str(tab_no + 1) +
              '.csv')


# RHC
gate = ['GATEMEANBP1AllDTH30LC', 'GATEAPS1AllDTH30LC', 'GATECAT1PRAllDTH30LC']
gatemate = ['GATEMATEMEANBP1AllDTH30LC', 'GATEMATEAPS1AllDTH30LC',
            'GATEMATECAT1PRAllDTH30LC']

effects = gate + gatemate
varnames = ['MEANBP1', 'APS1', 'CAT1']
varlist = [[name for name in effects if var in name] for var in varnames]
NUMBER_OF_TREATMENTS = 1
FIRST_TREATMENT_LEVEL = 0  # First level of treatment variable.
NUMBER_OF_COMBI = 1  # Number of possible treatment combinations.
params = {}
params['number_of_treatments'] = NUMBER_OF_TREATMENTS
params['number_of_stats'] = NUMBER_OF_STATS
params['first_level_of_treatment_variable'] = FIRST_TREATMENT_LEVEL
params['treatment_names'] = of.generate_treatment_names(
    FIRST_TREATMENT_LEVEL, NUMBER_OF_TREATMENTS)
params['number_of_decimal_places'] = NUMBER_OF_DECIMAL_PLACES

for idx_range8, varname in enumerate(varnames):
    for idx_name, name in enumerate(varlist[idx_range8]):
        params['directory_effect'] = DIRECTORY_RHC + INPUT_FOLDERNAME + name
        stats_table = of.generate_gate_table(params)
        df = of.create_dataframe_for_results(stats_table, n_1=MULTIPLIER_ROWS,
                                             n_2=NUMBER_OF_STATS)
        df_index = df.index
        df.index = range(df.shape[0])
        for i in range(0, df.shape[0], MULTIPLIER_ROWS):
            for j in range(df.shape[1]):
                df.iloc[i, j] = stats_table.iloc[int(i / MULTIPLIER_ROWS), j]
                CINT = of.create_confidence_interval(
                    stats_table.iloc[int(i / MULTIPLIER_ROWS),
                                     j + NUMBER_OF_COMBI],
                    stats_table.iloc[int(i / MULTIPLIER_ROWS),
                                     j + 2 * NUMBER_OF_COMBI])
                df.iloc[i + 1, j] = CINT
        if idx_name == 0:
            df_new = pd.DataFrame(data=np.empty((df.shape[0], len(colnames))),
                                  columns=colnames)
        df_new.iloc[:, idx_name] = df
    df_new.index = df_index
    for i in range(0, len(df), MULTIPLIER_ROWS):
        if df_new.index[i] == int(df_new.index[i]):  # No decimal values.
            idx_list = df_new.index.tolist()
            df_new.index = idx_list[:i] + [int(df_new.index[i])] + \
                idx_list[i + 1:]
    df_new.to_csv(OUTPUT_FOLDERNAME_TAB + 'suppl_table_tab_' +
                  str(idx_range8 + 7) + '.csv')

# WIA

colnames = ['GATE', 'GATE-ATE']
effects = ['GATEAGEAllEARNINGSLC', 'GATEMATEAGEAllEARNINGSLC',
           'GATEUCAllEARNINGSLC', 'GATEMATEUCAllEARNINGSLC']
NUMBER_OF_TREATMENTS = 4
FIRST_TREATMENT_LEVEL = 1  # First level of treatment variable.
NUMBER_OF_COMBI = 6  # Number of possible treatment combinations.
params = {}
params['number_of_treatments'] = NUMBER_OF_TREATMENTS
params['number_of_stats'] = NUMBER_OF_STATS
params['first_level_of_treatment_variable'] = FIRST_TREATMENT_LEVEL
params['treatment_names'] = of.generate_treatment_names(
    FIRST_TREATMENT_LEVEL, NUMBER_OF_TREATMENTS)
params['number_of_decimal_places'] = NUMBER_OF_DECIMAL_PLACES

for no, name in enumerate(effects):
    params['directory_effect'] = DIRECTORY_WIA + INPUT_FOLDERNAME + name
    stats_table = of.generate_gate_table(params)
    df = of.create_dataframe_for_results(stats_table, n_1=MULTIPLIER_ROWS,
                                         n_2=NUMBER_OF_STATS)
    for i in range(0, df.shape[0], MULTIPLIER_ROWS):
        for j in range(df.shape[1]):
            df.iloc[i, j] = stats_table.iloc[int(i / MULTIPLIER_ROWS), j]
            CINT = of.create_confidence_interval(
                stats_table.iloc[int(i / MULTIPLIER_ROWS),
                                 j + NUMBER_OF_COMBI],
                stats_table.iloc[int(i / MULTIPLIER_ROWS),
                                 j + 2 * NUMBER_OF_COMBI])
            df.iloc[i + 1, j] = CINT
        if df.index[i] == int(df.index[i]):  # No decimal value if integer.
            idx_list = df.index.tolist()
            df.index = idx_list[:i] + [int(df.index[i])] + idx_list[i + 1:]
    df.to_csv(OUTPUT_FOLDERNAME_TAB + 'suppl_table_tab_'
              + str(no + 10) + '.csv')
