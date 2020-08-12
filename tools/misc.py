import scipy.stats as stats
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd


def lt_pred(path, arup, days=None, pred_days=60):
    df = pd.read_csv(path)
    def func(x, a, b):
        return a * (x ** b)

    if days is None:
        #popt, pcov = curve_fit(func, df.iloc[:len(df), 0], df.iloc[:len(df), 1])
        popt, pcov = curve_fit(func, list(range(len(df))), df.iloc[:len(df), 0])
    else:
        #popt, pcov = curve_fit(func, df.iloc[:days,0], df.iloc[:days, 1])
        popt, pcov = curve_fit(func, list(range(days+1)), df.iloc[:len(df), 0])
    x = list(range(pred_days+1)) #df.iloc[:, 0]
    y = df.iloc[:, 1]
    y_pred = [func(i, popt[0], popt[1]) for i in x]
    ltv = sum([arup*y_pred for i in y_pred])
    mse = np.mean((y-y_pred)**2)

    return mse, x, y, y_pred, ltv


def t_test(path, conf=0.05, mode=2, y=None):
    df = pd.read_csv(path)
    res = ''
    p_value = 0

    array1 = np.array(df.loc[:, 0])
    if not df.loc[:, 1].isnull().all():
        array2 = np.array(df.loc[:, 1])

    if mode == 1:
        res = stats.tttest_1samp(array1, y)
        p_value = format(res[1], f'0.2f')
    elif mode == 2:
        levene_res = stats.levene(array1, array2)
        if levene_res[1] <= conf:
            res = stats.ttest_ind(array1, array2, equal_var=False)
        else:
            res = stats.ttest_ind(array1, array2)
    else:
        stats.ttest_rel(array1, array2)

    if p_value <= conf:
        res = 'significant'
    if p_value > conf:
        res = 'not significant'

    return res, p_value


def chi_test(path, conf=0.05):
    #df = df.loc[[exp_group_name, base_group_name], [x]] ## 列表用list引用而非str, 否则会得到series, 生成crosstab时会报错
    df = pd.read_csv(path)
    df = df.dropna()
    pivot_table = pd.crosstab(df.iloc[:, 0], df.iloc[:, 1])
    res = stats.chi2_contingency(np.array(pivot_table))
    p_value=res[1]

    if p_value <= conf:
        res = 'significant'
    if p_value > conf:
        res = 'not significant'

    p_value = format(res[1], f'0.2f')
    return res, p_value
