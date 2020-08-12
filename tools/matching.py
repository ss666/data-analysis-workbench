import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
#from lightgbm import LGBMClassifier
#from xgboost import XGBClassifier


def CEM(path, feature_col_first, feature_col_last, cutpoints, ratio=0):
    data = pd.read_csv(path)
    temp = data.copy()
    temp.drop_duplicates(['id', 'treatment'], inplace=True)
    temp.reset_index(drop=True, inplace=True)
    temp_X = temp.iloc[:, feature_col_first:feature_col_last]
    temp['sig_lst'] = 'sign'
    match_id = []

    for i in temp_X.columns:
        if len(temp_X[i].value_counts()) > 2:
            if cutpoints != None and i in cutpoints.key():
                temp_X[i] = np.digitize(temp_X[i], cutpoints[i])
            else:
                breaks = np.ceil(np.log2(temp_X[i].count()) + 1)
                temp_X[i] = pd.cut(temp_X[i], breaks, labels=False)
        temp['sig_lst'] = temp['sig_lst'].str.cat(temp_X[i].astype('str'), sep='-')

    for name, group in temp.groupby('sig_lst'):
        if group['treatment'].max() - group['treatment'].min == 1:
            if ratio==0:  # one-to-one /variable
                if group[group.treatment == 1]['id'].count() >= group[group.treatment == 0].count():
                    match_id.extend(group[group.treatment == 0]['id'])
                    treatment_sample = group[group.treatment == 1, 'id'].sample(group[group.treatment == 0, 'id'].count(),random_state=0)
                    match_id.extend(treatment_sample)
                else:
                    match_id.extend(group[group.treatment == 1]['id'])
                    control_sample = group[group.treatment == 0]['id'].sample(group[group.treatment == 1]['id'].count(),random_state=0)
                    match_id.extend(control_sample)
# else:
    matched = data[data['id'].isin(match_id)]
    return matched


def PSM(path, feature_cols, model, label, caliper=0.05, top=10):
    df = pd.read_csv(path)
    temp = df.copy()
    temp.drop_duplicates(['id', 'treatment'], inplace=True)
    temp.reset_index(drop=True, inplace=True)
    temp_treatment = temp[temp.treatment == 1]

    temp_model = temp.iloc[:, feature_cols]
    temp_model = pd.get_dummies(temp_model)
    temp_model['treatment'] = temp['treatment']
    x_train = temp_model[temp_model.treatment == 1].iloc[:, :-1]
    y_train = temp_model[temp_model.treatment == 1].iloc[:, [label]]

    # feature_importance
    feature_importance = pd.DataFrame([])
    feature_importance['column'] = x_train.columns

    if model == 'RandomForest':
        propensity_model = RandomForestClassifier(max_depth=10, class_weight='balanced', random_state=0)
        propensity_model.fit(x_train, y_train)
        feature_importance['feature_importance'] = propensity_model.feature_importances_
        feature_importance = feature_importance.sort_values(by='feature_importance', ascending=False).iloc[:top, :]

    elif model == 'LightGBM':
        #propensity_model = LGBMClassifier(max_depth=6, class_weight='balanced', random_state=0)
        #propensity_model.fit(x_train, y_train)
        #feature_importance['feature_importance'] = propensity_model.feature_importances_
        #feature_importance = feature_importance.sort_values(by='feature_importance', ascending=False)
        pass

    elif model == 'LR':
        # propensity_model=LogisticRegression(class_weight='balanced',random_state=0)
        # propensity_model.fit(x_train, y_train)
        scaler = MinMaxScaler()
        scaler.fit(x_train)
        x_scaled = scaler.transform(x_train)
        # scaler_model=
        propensity_model = LogisticRegression(class_weight='balanced', random_state=0)
        propensity_model.fit(x_scaled, y_train)
        feature_importance['feature_importance'] = propensity_model.coef_[0].apply(abs)
        feature_importance = feature_importance.sort_values(by='feature_importance', ascending=False)

    else:  # XGBoost
      #  n = len(y_train[y_train[label] == 0]) / len(y_train[y_train[label] == 1])  # scale_pos_weight
      #  propensity_model = XGBClassifier(scale_pos_weigh=n, max_depth=7, class_weight='balanced', random_state=0)
      # propensity_model.fit(x_train, y_train)
      #  feature_importance['feature_importance'] = propensity_model.feature_importances_
      #  feature_importance = feature_importance.sort_values(by='feature_importance', ascending=False)
      pass

    pscore = propensity_model.predict_proba(temp_model.iloc[:, :-1])[:, 1]
    pscore = pd.Series(pscore)

    N0, N1 = temp[temp.treatment == 0].index, temp[(temp.treatment == 1) & (temp[label] == 1)].index
    g0, g1 = pscore[temp.treatment == 0], pscore[(temp.treatment == 1) & (temp[label] == 1)]

    # order = np.random.permutation(N1)
    matches = {}
    for m in N1:
        dif = abs(g1[m] - g0)
        if dif.min() <= caliper:
            matches[m] = [dif.idxmin()]

    row = list(set([m for match in matches.values() for m in match])) + [m for m in matches.keys()]
    match_id = temp.ix[row, 'id']
    matched = df[df['id'].isin(match_id)]

    return matched, pscore, match_id, feature_importance
