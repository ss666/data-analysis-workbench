import scipy.stats as stats
import numpy as np
import pandas as pd


def chi_test(x, df, digit, group_name1, group_name2):
    df.set_index(['group_name'], inplace=True)  # preprocessing
    df = df.loc[[group_name1, group_name2], x]
    df = df.dropna()  # drop含na的行（number of na >=1)
    t = pd.crosstab(df.index, df[x])
    t_array = np.array(t)  # index is dropped
    res = stats.chi2_contingency(t_array)
    return format(res[1], f':.{digit}f')  # 0. .


def t_test(x, df, digit, group_name1, group_name2, conf):
    array1 = np.array(df.loc[group_name1, x])
    array1 = array1[~np.isnan(array1)]
    array2 = np.array(df.loc[group_name2, x])
    array2 = array2[~np.isnan(array2)]  # np.isnan() element-wise

    res_levene = stats.levene(array1, array2)

    if res_levene[1] <= conf:  # Levene检验原假设：两样本所代表总体的方差相同； p>0.05 不能拒绝原假设
        res_ttest = stats.ttest_ind(array1, array2, equal_var=False)
    else:
        res_ttest = stats.ttest_ind(array1, array2, equal_var=True)
    return format(res_ttest[1], f'0.{digit}f')


def test_attr(df, base_list, exp_list, digit, binomial, conf):
    df.set_index(['group_name'], inplace=True)
    df_test = pd.DataFrame(index=df.columns)

    # 生成series， 设置index？？

    # AA
    base_cnt = len(base_list)
    if base_cnt > 1:
         for i in range(base_cnt):
            for j in range(i + 1, base_cnt):
                df_test['p_value'] = pd.Series(df.columns).map(lambda x:
                    chi_test(x, df, digit, base_list[i], base_list[j]) if x in binomial
                    else t_test(x, df, digit, base_list[i], base_list[j], conf))
                df_test['is_sign'] = df_test['p_value'].map(lambda x: 'yes' if float(x) <= conf else 'no')

    # AB
    for exp in exp_list:
        df_test['p_value'] = pd.Series(df.columns).map(lambda x:
            chi_test(x, df, digit, 'base', exp) if exp in binomial else t_test(x, df, digit, 'base', exp, conf))
        df_test['is_sign'] = df_test['p_value'].map(lambda x: 'yes' if float(x) <= conf else 'no')
    return df_test


def agg_attr(df, base_list, exp_list, digit, binomial):
    # df.replace(0,np.nan, inplace=True): 0置为null，避免计入平均
    df_agg = df.groupby('group_name').mean().T

    def foo(group_name, x):
        if x in binomial:
            return format(df_agg.loc[x, group_name] * 100, f'0.{digit}f') + "%"
        else:
            return format(df_agg.loc[x, group_name], f'0.{digit}f')

    def delta(exp, base, x):
        if x in binomial:
            return format((df_agg.loc[x, exp] - df_agg.loc[x, base]) / df_agg.loc[x, base] * 100,
                          f'0.{digit}f') + '%'
        else:
            pass  # return format()

    features = pd.Series(df_agg.index)

    df_agg['base_avg'] = features.apply(foo, group_name='base')
    # AA
    base_cnt = len(base_list)
    if base_cnt > 1:
        for i in range(base_cnt):
            df_agg[f'{base_list[i]}_avg'] = features.apply(foo, group_name=base_list[i])
            for j in range(i + 1, base_cnt):
                df_agg[f'{base_list[j]}_avg'] = features.apply(foo, group_name=base_list[j])
                df_agg[f'delta_{base_list[j]}_to_{base_list[i]}'] = features.apply(delta, exp=base_list[j], base=base_list[i])

    # AB
    for x in exp_list:
        df_agg[f'{x}_avg'] = features.apply(foo, group_name=x)
        df_agg[f'delta_{x}_to_base(avg)'] = features.apply(delta, exp=x, base='base')

    df_agg = df_agg.iloc[:, len(base_list + exp_list):]
    return df_agg


def union_test_agg_attr(df, base_list, exp_list, digit, binomial, conf):
    # load 整体base ,计算average base
    df_base = df.loc[df[base_list]]
    df_base.group_name = 'base'
    df = pd.concat([df, df_base])

    df_test = (df, base_list, exp_list, digit, binomial, conf)
    df_agg = (df.drop(['date'], axis=1), base_list, exp_list, digit, binomial)
    df_res = df_agg.join(df_test, how='inner')
    return df_res


def ab_test(path, digit=2, binomial=[], conf=0.05):
    df = pd.read_csv(path)
    dim_list = ['date', 'group_name']
    feature_list = df.columns.values[2:].tolist()
    df.columns = dim_list + feature_list
    df[feature_list] = df[feature_list].astype(float)  # np.float

    group_list = pd.unique(df.group_name).tolist()  # .sort()
    base_list, exp_list = [], []
    for item in group_list:
        if 'base' in item:
            base_list.append(item)
        elif 'exp' in item:
            exp_list.append(item)

    df_result = union_test_agg_attr(df, base_list, exp_list, digit, binomial, conf)
    file_dl = './download/abtest-result.csv'
    df_result.to_csv(file_dl, index=False)
    return file_dl


