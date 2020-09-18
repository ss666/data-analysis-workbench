import scipy.stats as stats
import numpy as np
import pandas as pd


def chi_test(x, df, group_name1, group_name2, digit):
    #df.set_index(['group_name'], inplace=True)  # preprocessing
    df = df.loc[[group_name1, group_name2], x]
    df = df.dropna()  # drop含na的行（number of na >=1)
    t = pd.crosstab(df.index, df.values)
    t_array = np.array(t)  # index is dropped
    res_chitest = stats.chi2_contingency(t_array)
    return format(res_chitest[1], f'.{digit}f')


def t_test(x, df, group_name1, group_name2, digit, alpha):
    array1 = np.array(df.loc[group_name1, x])
    array1 = array1[~np.isnan(array1)]
    array2 = np.array(df.loc[group_name2, x])
    array2 = array2[~np.isnan(array2)]  # np.isnan() element-wise

    res_levene = stats.levene(array1, array2)

    if res_levene[1] <= alpha:  # Levene检验原假设：两样本所代表总体的方差相同； p>0.05 不能拒绝原假设
        res_ttest = stats.ttest_ind(array1, array2, equal_var=False)
    else:
        res_ttest = stats.ttest_ind(array1, array2, equal_var=True)
    return format(res_ttest[1], f'0.{digit}f')


def test_attr(df, base_list, exp_list, digit, binomial, alpha):
    df.set_index(['group_name'], inplace=True)
    df_test = pd.DataFrame(index=df.columns)

    # AA
    base_cnt = len(base_list)
    if base_cnt > 1:
        for i in range(base_cnt):
            for j in range(i + 1, base_cnt):
                df_test[f'p value for {base_list[j]} to {base_list[i]}'] = pd.Series(df.columns, index=df.columns).map(lambda x:
                    chi_test(x, df, base_list[i], base_list[j], digit) if x in binomial
                    else t_test(x, df, base_list[i], base_list[j], digit, alpha))
                df_test[f'is sign. for {base_list[j]} to {base_list[i]}'] = df_test[f'p value for {base_list[j]} to {base_list[i]}'].map(lambda x: 'yes' if float(x) <= alpha else 'no')

    # AB
    for exp in exp_list:
        df_test[f'p value for {exp} to base(avg)'] = pd.Series(df.columns, index =df.columns).map(lambda x:
            chi_test(x, df, 'base', exp, digit) if exp in binomial else t_test(x, df, 'base', exp, digit, alpha))
        df_test[f'is sign. for {exp} to base(avg)'] = df_test[f'p value for {exp} to base(avg)'].map(lambda x: 'yes' if float(x) <= alpha else 'no')
    return df_test


def agg_attr(df, base_list, exp_list, digit, binomial):
    # df.replace(0,np.nan, inplace=True): 0置为null，避免计入平均
    df_agg = df.groupby('group_name').mean().T

    def foo(x, group_name):
        if x in binomial:
            return format(df_agg.loc[x, group_name] * 100, f'0.{digit}f') + "%"
        else:
            return format(df_agg.loc[x, group_name], f'0.{digit}f')

    def delta(x, exp, base):
        if x in binomial:
            return format((df_agg.loc[x, exp] - df_agg.loc[x, base]) * 100,
                          f'0.{digit}f') + 'pp'
        else:
            return format((df_agg.loc[x, exp] - df_agg.loc[x, base]) / df_agg.loc[x, base] * 100,
                          f'0.{digit}f') + '%'

    features = pd.Series(df_agg.index, index=df_agg.index) #index????
    df_agg['base_avg'] = features.apply(foo, group_name='base')

    # AA
    base_cnt = len(base_list)
    if base_cnt > 1:
        for i in range(base_cnt):
            df_agg[f'{base_list[i]} avg'] = features.apply(foo, group_name=base_list[i])
            for j in range(i + 1, base_cnt):
                df_agg[f'{base_list[j]} avg'] = features.apply(foo, group_name=base_list[j])
                df_agg[f'delta {base_list[j]} to {base_list[i]}'] = features.apply(delta, exp=base_list[j], base=base_list[i])

    # AB
    for x in exp_list:
        df_agg[f'{x} avg'] = features.apply(foo, group_name=x)
        df_agg[f'delta {x} to base(avg)'] = features.apply(delta, exp=x, base='base')

    df_agg = df_agg.iloc[:, len(base_list + exp_list)+1:]  #plus 1 or not
    return df_agg


def union_test_agg_attr(df, base_list, exp_list, digit, binomial, alpha):
    df_base = df.loc[df.group_name.str.contains('base')] #loc[df.group_name in base_list] #.copy()
    df_base.group_name = 'base'
    df = pd.concat([df, df_base])

    df_test = test_attr(df, base_list, exp_list, digit, binomial, alpha)
    df_agg = agg_attr(df.drop(['date'], axis=1), base_list, exp_list, digit, binomial)
    df_res = df_agg.join(df_test, how='inner')


    columns_list = ['base_avg']
    for exp in exp_list:
        columns_list += [f'{exp} avg', f'delta {exp} to base(avg)', f'p value for {exp} to base(avg)', f'is sign. for {exp} to base(avg)']
    base_cnt = len(base_list)
    if base_cnt > 1:
        for base in base_list:
            columns_list.append(f'{base} avg')
        for i in range(base_cnt):
            for j in range(i + 1, base_cnt):
                columns_list += [f'delta {base_list[j]} to {base_list[i]}', f'p value for {base_list[j]} to {base_list[i]}', f'is sign. for {base_list[j]} to {base_list[i]}']
    df_res = df_res.loc[:, columns_list]

    return df_res


def ab_test(path, digit=2, binomial=[], alpha=0.05):
    df = pd.read_csv(path)
    dim_list = ['date', 'group_name']
    feature_list = df.columns.values[2:].tolist()
    df.columns = dim_list + feature_list
    df[feature_list] = df[feature_list].astype(float)  # np.float

    group_list = pd.unique(df.group_name).tolist()
    group_list.sort()
    base_list, exp_list = [], []
    for item in group_list:
        if 'base' in item:
            base_list.append(item)
        elif 'exp' in item:
            exp_list.append(item)

    df_result = union_test_agg_attr(df, base_list, exp_list, digit, binomial, alpha)
    df_result.insert(0, 'metrics', df_result.index)
    #df_result_index = pd.DataFrame(index=df.columns[2:])
    #df_result = df_result_index.join(df_result_data, how='inner')
    file_dl ='./front_end/static/abtest_result.csv'
    df_result.to_csv(file_dl, index=False)
    return file_dl

