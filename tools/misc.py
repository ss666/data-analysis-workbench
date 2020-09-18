import scipy.stats as stats
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd

import time
from functools import wraps
def timeit(test_func):
    @wraps(test_func)
    def time_logging():
        t1 = time.time() * 1000
        test_func()
        t2 = time.time() * 1000
        print(t2 - t1)
    return time_logging()


def lt_pred(path, arup, days=None, pred_days=60):
    df = pd.read_csv(path)
    def func(x, a, b):
        return a * (x ** b)

    if days is None:
        #popt, pcov = curve_fit(func, df.iloc[:len(df), 0], df.iloc[:len(df), 1])
        popt, pcov = curve_fit(func, list(range(len(df)))[1:], df.iloc[:len(df), 1])
    else:
        #popt, pcov = curve_fit(func, df.iloc[:days,0], df.iloc[:days, 1])
        popt, pcov = curve_fit(func, list(range(days+2))[1:], df.iloc[:(days+1), 1])
    x = list(range(pred_days+2))[1:] #df.iloc[:, 0]
    y = df.iloc[:, 1].tolist()
    y_pred = [func(i, popt[0], popt[1]) for i in x]
    ltv = sum([arup*i for i in y_pred])
    base_cnt = df.iloc[0, 1]
   # mse = np.mean((y-y_pred)**2)

    return x,y,y_pred,ltv,base_cnt


def t_test(path, alpha, mode, y):
    df = pd.read_csv(path)
    hypo_res = ''
    p_value = 0

    array1 = np.array(df.iloc[:, 0])
    array2 = None #have a look
    if df.shape[1] > 1:
        array2 = np.array(df.iloc[:, 1])

    if mode == 1:
        res = stats.ttest_1samp(array1, y)
    elif mode == 2:
        levene_res = stats.levene(array1, array2)
        if levene_res[1] <= alpha:
            res = stats.ttest_ind(array1, array2, equal_var=False)
        else:
            res = stats.ttest_ind(array1, array2)
    else:
        stats.ttest_rel(array1, array2)
    p_value = res[1]

    if p_value <= alpha:
        hypo_res = 'significant'
    if p_value > alpha:
        hypo_res = 'not significant'  #not separated
    p_value = format(res[1], f'0.3f')
    print(p_value, hypo_res)
    return hypo_res, p_value


def chi_test(path, alpha=0.05):
    #df = df.loc[[exp_group_name, base_group_name], [x]]
    df = pd.read_csv(path)
    df = df.dropna()
    pivot_table = pd.crosstab(df.iloc[:, 0], df.iloc[:, 1])
    res = stats.chi2_contingency(np.array(pivot_table))
    p_value = res[1]

    if p_value <= alpha:
        res = 'significant'
    if p_value > alpha:
        res = 'not significant'
    p_value = format(res[1], f'0.2f')

    return res, p_value



