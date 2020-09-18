import statsmodels.formula.api as smf
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
        print('did time: ', t2 - t1)
    return time_logging()

def preprocessing(df, treatment_col, id_col, date_col):
    df.rename(columns={id_col: 'id', treatment_col: 'treatment', date_col: 'date'}, inplace=True)
    df.drop_duplicates(['id', 'date'], inplace=True)
    # df['date'].astype('str') #df.date.astype('str')
    df.fillna(0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def did_core(df, y, post):
    # 判断y类型: if type(y) != str
    temp = df.copy()
    temp['post'] = 1 * (temp['date'].astype('str') >= post) #1 if (temp['date'] >= post) else 0  #

    temp[y] = temp[y].map(lambda x: np.log(x + 1))
    model = smf.ols(y + "~ post * treatment", data=temp).fit(cov_type='cluster', cov_kwds={'groups': temp['id']})
    res = ''
    p = model.pvalues['post:treatment']
    effect = format(model.params["post:treatment"] * 100, f'.2f')+'%'
    if p > 0.05:
        res = 'NOT significant'
    else:
        res = 'significant'
    print('***did effect and p:', effect, p)
    return res, p, effect


def did(path, y, post, treatment_col, id_col, date_col):
    df = pd.read_csv(path)
    df = preprocessing(df, treatment_col, id_col, date_col)
    return did_core(df, y, post)


