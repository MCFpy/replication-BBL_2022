# -*- coding: utf-8 -*-
"""
Created on Fri May 13 16:39:43 2022.

@author: HBodory
"""

# %% Libraries


import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import seaborn as sns
import pandas as pd
import numpy as np


# %% Functions


def plot_sorted_iates_minus_ate(data, ylabel='effect size'):
    """
    Line plot.

    Plot deviations of sorted IATEs from ATE with confidence bands.

    Parameters
    ----------
    data: PANDAS DATAFRAME
        Data to plot effects and confindence band.

    Returns
    -------
    fig: FIGURE
    """
    plt.rcParams['axes.labelsize'] = 'xx-large'
    plt.rcParams['xtick.labelsize'] = 'xx-large'
    plt.rcParams['ytick.labelsize'] = 'xx-large'
    plt.rcParams['text.color'] = 'black'
    plt.rcParams['legend.fontsize'] = 'xx-large'
    fig, axs = plt.subplots()
    axs.plot(data.index, data.effects, '-')
    axs.fill_between(data.index, data.upper, data.lower, alpha=0.2)
    plt.hlines(0, colors='red', xmin=0, xmax=len(data), linestyles='solid')
    fig.set_size_inches(12.5, 10.5, forward=True)
    plt.xlabel('index of the ordered IATEs')
    plt.ylabel(ylabel)
    plt.legend(['IATE-ATE',  '90%-CI'], loc='upper center',
               fancybox=False, shadow=False, ncol=10)
    plt.rcParams.update(plt.rcParamsDefault)  # Default settings.
    return fig


def gen_data_densities(file_name, d_card, d_base):
    """
    Create dataframe, which contains densities for all treatment comparisons.

    Parameters
    ----------
    file_name: STRING
        First part of the string to locate the file with the stored densities
        of the IATEs.
    d_card: INTEGER
        Number of treatment states.
    d_base: INTEGER
        Baseline treatment in the analysis of treatment effects.
    Returns
    -------
    data: PANDAS DATAFRAME
    """
    if d_card - d_base == 1:
        d_level = d_base + 1
        data = pd.read_csv(file_name + str(d_level) + 'vs' + str(d_base) +
                           '_iate.csv')
        data['d'] = d_level
    else:
        for d_level in range(d_base + 1, d_base + d_card):
            if d_level == d_base + 1:
                data = pd.read_csv(file_name + str(d_level) + 'vs' +
                                   str(d_base) + '_iate.csv')
                data['d'] = d_level
            else:
                data_temp = pd.read_csv(file_name + str(d_level) + 'vs' +
                                        str(d_base) + '_iate.csv')
                data_temp['d'] = d_level
                data = data.append(data_temp)
                data.reset_index(drop=True, inplace=True)
    for d_level in range(d_base + 1, d_base + d_card):
        if (data.loc[data.d == d_level, 'grid'] == data.grid.min()).sum() == 0:
            data = data.append({'d': d_level, 'grid': data.grid.min(),
                                'density': 0.0}, ignore_index=True)
        if (data.loc[data.d == d_level, 'grid'] == data.grid.max()).sum() == 0:
            data = data.append({'d': d_level, 'grid': data.grid.max(),
                                'density': 0.0}, ignore_index=True)
    return data


def plot_densities_new(file_name, d_card, d_base, ate=0, ate_y=False):
    """
    Create (multiple) density plots.

    Plot multiple densities of IATEs. The IATEs use the group with the
    smallest level in the treatment variable as comparison group.

    Parameters
    ----------
    file_name: STRING
        First part of the string to locate the file with the stored densities
        of the IATEs.
    d_card: INTEGER
        Number of treatment states.
    d_base: INTEGER
        Baseline treatment in the analysis of treatment effects.
    ate: FLOAT
        Float of the ATE.
    ate_y: BOOLEAN
        Boolean to control if the ATE is added as a vertical line in the
        figure.

    Returns
    -------
    fig: FIGURE
    """
    data = pd.DataFrame(gen_data_densities(file_name, d_card, d_base))
    plt.rcParams['axes.labelsize'] = 'xx-large'
    plt.rcParams['xtick.labelsize'] = 'xx-large'
    plt.rcParams['ytick.labelsize'] = 'xx-large'
    plt.rcParams['text.color'] = 'black'
    plt.rcParams['legend.fontsize'] = 'xx-large'
    sns.set_style('whitegrid')
    fig = plt.subplots()
    fig = sns.lineplot(x="grid", y="density", hue="d", data=data,
                       palette="tab10", alpha=0.2, )
    fig = fig.get_figure()
    fig.set_size_inches(12.5, 10.5, forward=True)
    if d_card - d_base != 1:
        for d_level in range(d_base + 1, d_base + d_card):
            plt.fill_between(data.grid[data.d == d_level],
                             data.density[data.d == d_level], alpha=0.2)
    else:
        plt.fill_between(data.grid[data.d == d_base + 1],
                         data.density[data.d == d_base + 1],
                         alpha=0.2)
    if ate_y:
        l_ate = plt.axvline(x=ate, color='b')
    children = plt.gca().get_children()
    plt.xlabel("IATE")
    plt.ylabel("density")
    plt.ylim(ymin=0)
    if ate_y:
        plt.legend([children[d] for d in range(0, d_card - 1)] + [l_ate],
                   ['T' + str(d) + '-T0' for d in range(d_base + 1, d_base +
                    d_card)] + ['ATE'],
                   loc='upper right', fancybox=False, shadow=False, ncol=10)
    else:
        plt.legend([children[d] for d in range(0, d_card - 1)],
                   ['T' + str(d) + '-T' + str(d_base) for d in
                   range(d_base + 1, d_base + d_card)],
                   loc='upper right',
                   fancybox=False, shadow=False, ncol=1)
    return fig


def gen_gate_fig(data, label, categorical=True, gate=True, value_labels=None):
    """
    Create line plot for GATEs (minus ATE) with confidence band.

    Parameters
    ----------
    data : PANDAS DATAFRAME
        Data for plots.
    xlabel : STRING
        Label of x-axis.
    categorical : BOOLEAN, optional.
        Flag for categorical variable. The default is True.

    Returns
    -------
    fig : FIGURE
    """
    xlabel = label[0]
    ylabel = label[1]
    plt.rcParams['axes.labelsize'] = 'xx-large'
    plt.rcParams['xtick.labelsize'] = 'xx-large'
    plt.rcParams['ytick.labelsize'] = 'xx-large'
    plt.rcParams['text.color'] = 'black'
    plt.rcParams['legend.fontsize'] = 'xx-large'
    fig, axs = plt.subplots()
    if categorical:
        axs.plot(data.z_values, data.effects, 'o')
        axs.set_xticklabels(value_labels)
        plt.plot([data.z_values, data.z_values], [data.upper, data.lower],
                 '-', color='tab:blue')
        plt.plot([data.z_values - 0.1, data.z_values + 0.1],
                 [data.upper, data.upper], color='tab:blue')
        plt.plot([data.z_values - 0.1, data.z_values + 0.1],
                 [data.lower, data.lower], color='tab:blue')
        blue_line = mlines.Line2D([], [], marker='o')
    else:
        axs.plot(data.z_values, data.effects, '-')
        axs.fill_between(data.z_values, data.upper, data.lower, alpha=0.2)
    ate = plt.hlines(data.ate, colors='red', xmin=data.z_values.min(),
                     xmax=data.z_values.max(), linestyles='solid')
    fig.set_size_inches(12.5, 10.5, forward=True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if gate:
        if categorical:
            plt.legend([blue_line, ate], ["90%-CI GATE", "ATE"],
                       loc='upper right',
                       fancybox=False, shadow=False, ncol=10)
        else:
            plt.legend(['GATE', '90%-CI', 'ATE'], loc='upper center',
                       fancybox=False,
                       shadow=False, ncol=10)
    else:
        if categorical:
            plt.legend([blue_line, ate], ["90%-CI GATE-ATE"],
                       loc='upper right',
                       fancybox=False, shadow=False, ncol=10)
        else:
            plt.legend(['GATE', '90%-CI'], loc='upper center',
                       fancybox=False,
                       shadow=False, ncol=10)
    return fig


def generate_treatment_names(x_int, y_int):
    """
    Generate names for comparisons of treatment levels.

    Parameters
    ----------
    x_int : INTEGER
        Smallest level of treatment variable.
    y_int : INTEGER
        Number of treatment and control levels.

    Returns
    -------
    columns : LIST
        List of strings with all possible combinations of treatment levels.

    """
    columns = []
    for j in range(x_int, y_int):
        for i in range(x_int + 1, y_int + 1):
            if i <= j:
                pass
            else:
                columns.append(str(i) + " vs. " + str(j))
    return columns


def generate_gate_table(params, label_row=False):
    """
    Generate a dataframe.

    The dataframe includes the effects and confidence bounds for all possible
    combinations of treatment levels.

    Parameters
    ----------
    params : DICTIONARY
        number_of_treatments : INTEGER
            Number of treatment and control levels.
        directory_effect : STRING
            Directory.
        number_of_stats : INTEGER
            Number of statistics in dataframe.
        first_level_of_treatment_variable : INTEGER
            Lowest integer.
        treatment_names : STRING
            Names for comparisons of treatment groups.
        number_of_decimal_places: INTEGER
            Digits after decimal point for effects and confidence bounds.
    label_row : BOOLEAN, optional
        User-defined index for new dataframe. The default is False.

    Returns
    -------
    df : PANDAS DATAFRAME
        New dataframe.

    """
    d_count = 1 + params['number_of_treatments']
    name = params['directory_effect']
    d_start = params['first_level_of_treatment_variable']

    for j in range(1 + d_start, d_count):
        for i in range(j, d_count):
            if i == j:
                data = pd.DataFrame(pd.read_csv(name + str(i) + "vs" +
                                    str(j-1) + ".csv"))  # Ensure right class
                if 'x_values' in data.columns:
                    data = data.rename(columns={'x_values': 'z_values'})
                data['d'] = i
            else:
                dat = pd.DataFrame(pd.read_csv(name + str(i) + "vs" +
                                   str(j-1) + ".csv"))  # Ensure right class
                if 'x_values' in dat.columns:
                    dat = dat.rename(columns={'x_values': 'z_values'})
                dat['d'] = i
                data = data.append(dat)
        if j == 1 + d_start:
            data_0 = np.array(data.pivot(index='z_values', columns="d",
                                         values="effects"))
            data_lower = np.array(data.pivot(index='z_values', columns="d",
                                             values="lower"))
            data_upper = np.array(data.pivot(index='z_values', columns="d",
                                             values="upper"))
        else:
            data_0 = np.concatenate([data_0,
                                     data.pivot(index='z_values',
                                                columns="d",
                                                values="effects")],
                                    axis=1)
            data_lower = np.concatenate([data_lower,
                                         data.pivot(index='z_values',
                                                    columns="d",
                                                    values="lower")],
                                        axis=1)
            data_upper = np.concatenate([data_upper,
                                         data.pivot(index='z_values',
                                                    columns="d",
                                                    values="upper")],
                                        axis=1)

    results = np.concatenate((data_0, data_lower, data_upper), axis=1)
    df_new = pd.DataFrame(np.round(results,
                                   params['number_of_decimal_places']))
    df_new.columns = params['number_of_stats'] * params['treatment_names']
    if not label_row:
        df_new.index = data.z_values
    else:
        df_new.index = label_row
    return df_new


def create_dataframe_for_results(data, n_1=2, n_2=3):
    """
    Create an empty dataframe.

    Parameters
    ----------
    data : PANDAS DATAFRAME
        Dateframe with treatment effects and confidence bounds.
    n_1 : INTEGER, optional
        Multiplier to increase the number of rows. The default is 2.
    n_2 : INTEGER, optional
        Constant by which the number of columns has to be divided to obtain
        the number of columns with treatment effects only . The default is 3.

    Returns
    -------
    df_empty : PANDAS DATAFRAME
        Empty DataFrame with index and column names.

    """
    nrows = n_1 * data.shape[0]  # Number of rows for new dataframe.
    ncols = int(data.shape[1] / n_2)  # Number of columns for new dataframe.
    matrix = np.empty([nrows, ncols])
    df_empty = pd.DataFrame(matrix)
    df_empty.columns = data.columns[:ncols]
    df_empty['idx'] = ''
    for i in range(0, len(df_empty), n_1):
        df_empty.loc[i, 'idx'] = data.index[int(i / n_1)]
    df_empty.set_index('idx', inplace=True)
    return df_empty


def create_confidence_interval(x_var, y_var):
    """
    Create confidence interval as string in squared brackets.

    Parameters
    ----------
    x_var : FLOAT
        Lower bound of a confidence interval.
    y_var : FLOAT
        Upper bound of a confidence interval.

    Returns
    -------
    STRING
        Confidence interval as string in squared brackets.

    """
    return '[' + str(x_var) + ', ' + str(y_var) + ']'


def compute_significance_stats(data):
    """
    Indicate evaluation points with significant effects.

    Parameters
    ----------
    data : PANDAS DATAFRAME
        Effects, confidence intervals, evaluation points.

    Returns
    -------
    counter : INTEGER.
        Number of evaluation points with significant effects.
    zvalues : LIST.
        Evaluation points with significant effects.

    """
    counter = 0
    zvalues = list()
    for i in range(data.shape[0]):
        condition = (data.loc[i, 'ate'] > data.loc[i, 'upper']) or \
            (data.loc[i, 'ate'] < data.loc[i, 'lower'])
        counter += 1 if condition else False
        zvalues = zvalues.append(data.loc[i,
                                 'z_values']) if condition else False
    return counter, zvalues
