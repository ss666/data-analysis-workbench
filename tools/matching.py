import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier


def cem(path, feature_col_first, feature_col_last, cutpoints=None, grouping=None, ratio=0, treatment_col='treatment', id_col='id'):
    data = pd.read_csv(path)
    data.rename(columns={id_col: 'id', treatment_col: 'treatment'}, inplace=True)
    temp = data.copy()
    temp.drop_duplicates(['id', 'treatment'], inplace=True)
    temp.reset_index(drop=True, inplace=True)
    temp_X = temp.iloc[:, feature_col_first:feature_col_last]
    temp['sig_lst'] = 'sign'
    match_id = []

    for i in temp_X.columns:
        if temp_X[i].dtype == object:
            if grouping != None and i in grouping.keys():
                for j in grouping[i]:
                    temp_X[i][temp_X[i].isin(j)] = '_'.join(j)
        elif len(temp_X[i].value_counts()) > 2:
            if cutpoints != None and i in cutpoints.key():
                temp_X[i] = np.digitize(temp_X[i], cutpoints[i])
            else:
                breaks = np.ceil(np.log2(temp_X[i].count()) + 1).astype(int)
                temp_X[i] = pd.cut(temp_X[i], breaks, labels=False)
        temp['sig_lst'] = temp['sig_lst'].str.cat(temp_X[i].astype('str'), sep='-')

    for name, group in temp.groupby('sig_lst'):
        if group['treatment'].max() - group['treatment'].min() == 1:
            if ratio == 0:  # one-to-one /variable
                if group.loc[group.treatment == 1]['id'].count() >= group[group.treatment == 0]['id'].count():
                    match_id.extend(group[group.treatment == 0]['id'])
                    treatment_sample = group.loc[group.treatment == 1, 'id'].sample(group.loc[group.treatment == 0, 'id'].count(), random_state=0)
                    match_id.extend(treatment_sample)
                else:
                    match_id.extend(group[group.treatment == 1]['id'])
                    control_sample = group[group.treatment == 0]['id'].sample(group[group.treatment == 1]['id'].count(), random_state=0)
                    match_id.extend(control_sample)
# else:
    matched = data[data['id'].isin(match_id)]
    return matched


def psm(path,feature_col_first, feature_col_last,  label, model='LR', caliper=0.05, treatment_col='treatment', id_col='id'):
    df = pd.read_csv(path)
    df.rename(columns={id_col: 'id', treatment_col: 'treatment'}, inplace=True)
    temp = df.copy()
    temp.drop_duplicates(['id', 'treatment'], inplace=True)
    temp.reset_index(drop=True, inplace=True)
    temp_treatment = temp[temp.treatment == 1]
    temp_model = temp.iloc[:, feature_col_first:feature_col_last]
   #temp_model = temp.loc[:, feature_cols]
    temp_model = pd.get_dummies(temp_model)
    temp_model['treatment'] = temp['treatment']
    x_train = temp_model[temp_model.treatment == 1].iloc[:, :-1]
    y_train = temp_treatment.loc[:, label]

    # feature_importance
    feature_importance = pd.DataFrame([])
    feature_importance['column'] = x_train.columns

    if model == 'RandomForest':
        propensity_model = RandomForestClassifier(max_depth=10, class_weight='balanced', random_state=0)
        propensity_model.fit(x_train, y_train)
        feature_importance['feature_importance'] = propensity_model.feature_importances_
        feature_importance = feature_importance.sort_values(by='feature_importance', ascending=False).iloc[:top, :]

    elif model == 'LightGBM':
        propensity_model = LGBMClassifier(max_depth=6, class_weight='balanced', random_state=0)
        propensity_model.fit(x_train, y_train)
        feature_importance['feature_importance'] = propensity_model.feature_importances_
        feature_importance = feature_importance.sort_values(by='feature_importance', ascending=False)

    elif model == 'LR':
        # propensity_model=LogisticRegression(class_weight='balanced',random_state=0)
        # propensity_model.fit(x_train, y_train)
        scaler = MinMaxScaler()
        scaler.fit(x_train)
        x_scaled = scaler.transform(x_train)
        # scaler_model=
        propensity_model = LogisticRegression(class_weight='balanced', random_state=0)
        propensity_model.fit(x_scaled, y_train)
        #feature_importance['feature_importance'] = propensity_model.coef_[0].apply(abs)
        #feature_importance = feature_importance.sort_values(by='feature_importance', ascending=False)

    else:  # XGBoost
       n = len(y_train[y_train[label] == 0]) / len(y_train[y_train[label] == 1])  # scale_pos_weight
       propensity_model = XGBClassifier(scale_pos_weigh=n, max_depth=7, importance_type='weight', random_state=0)
       propensity_model.fit(x_train, y_train)
       feature_importance['feature_importance'] = propensity_model.feature_importances_
       feature_importance = feature_importance.sort_values(by='feature_importance', ascending=False)


    pscore = propensity_model.predict_proba(temp_model.iloc[:, :-1])[:, 1]
    pscore = pd.Series(pscore)

    N0, N1 = temp[temp.treatment == 0].index, temp[(temp.treatment == 1) & (temp[label] == 1)].index
    g0, g1 = pscore[temp.treatment == 0], pscore[(temp.treatment == 1) & (temp[label] == 1)]
    print(max(g0),min(g0))
    print('!!!')
    print(max(g1),min(g1))

    # order = np.random.permutation(N1)
    matches = {}
    for m in N1:
        dif = abs(g1[m] - g0)
        if dif.min() <= caliper:
            matches[m] = [dif.idxmin()]

    row = list(set([m for match in matches.values() for m in match])) + [m for m in matches.keys()]
    match_id =temp.iloc[row, :]
    match_id = match_id.id #temp.iloc[row, 0] ???
    print(match_id)
    matched = df[df['id'].isin(match_id)]
    matched = matched.iloc[:,1:]
    print(matched)

    file_dl ='./front_end/static/matching_psm_result.csv'
    matched.to_csv(file_dl, index=False)
    return file_dl
