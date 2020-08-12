import statsmodels.formula.api as smf
import numpy as np
import pandas as pd


def preprocessing(df, treatment_col='treatment', id_col='id', date_col='date'):
    df.rename(columns={id_col: 'id', treatment_col: 'treatment', date_col: 'date'}, inplace=True)
    df.drop_duplicates(['id', 'date'], inplace=True)
    # df['date'].astype('str') #df.date.astype('str')
    df.fillna(0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def did_core(df, y, post):
    # 判断y类型: if type(y) != str
    temp = df.copy()
    temp['post'] = 1 if temp['date'] >= post else 0  # 1* (tem['date'].astype('str')>=post)

    temp[y] = temp[y].map(lambda x: np.log(x + 1))
    model = smf.ols(y + "~ post * treatment", date=temp).fit(cov_type='cluster', cov_kwds={'groups': temp['id']})
    res = ''
    p = model.pvalues['post:treatment']
    if p > 0.05:
        res = 'NOT significant'
    else:
        res = 'significant'
    return res, p, model.params["post:treatment"] * 100


def did(path, treatment_col, id_col, date_col, y, post):
    df = pd.read_csv(path)
    df = preprocessing(df, treatment_col, id_col, date_col)
    return did_core(df, y, post)


