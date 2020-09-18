from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn import preprocessing
import pandas as pd

import time
from functools import wraps
from sklearn.metrics import roc_auc_score
def timeit(test_func):
    @wraps(test_func)
    def time_logging():
        t1 = time.time() * 1000
        test_func()
        t2 = time.time() * 1000
        print('ml time: ',t2 - t1)
    return time_logging()


def cluster(path, model, cluster_cnt):
    df = pd.read_csv(path)
    X = df.iloc[:, 1:]
    X = preprocessing.scale(X)
    if model == 'kmeans':
        clst = KMeans(n_clusters=cluster_cnt, max_iter=1000)
        clst.fit(X)
    if model == 'hc':   #bottom-up approach
        clst = AgglomerativeClustering(n_clusters=cluster_cnt, linkages='average')
        clst.fit(X)
    # a,b =enumerate(kmeans_model.labels_)
    ss = silhouette_score(X, clst.labels_, metric='euclidean')
    df['label_pred'] = clst.labels_
    file_dl = './download/clustering-result.csv'
    df.to_csv(file_dl, index=False)
    return ss


def classify(path, model, length, kernel, neighbors_cnt):
    print(path,model,length,kernel)
    df = pd.read_csv(path).sample(frac=1)
    df_X_train = df.iloc[length:, 1:-1]
    df_y_train = df.iloc[length:, -1]
    df_X_pred = df.iloc[length+1:, 1:-1]
    scaler = preprocessing.StandardScaler().fit(df_X_train)
    df_X_train= scaler.transform(df_X_train)
    df_X_pred = scaler.transform(df_X_pred)
    if model =='svm':
    #X_train, X_test, y_train, y_test = train_test_split(df_X, df_y, test_size)
        clf = SVC(kernel)
    if model =='knn':
        clf = KNeighborsClassifier(n_neighbors=neighbors_cnt)

    clf.fit(df_X_train, df_y_train)
    df.iloc[length+1:, -1] = clf.predict(df_X_pred)
    print('ml evaluation metric:', roc_auc_score(df.iloc[length+1:, -1], clf.predict_proba(df.iloc[length+1:, 1:-1]), average='macro', multi_class='ovo'))
    file_dl = './front_end/static/classification_result.csv'
    df.to_csv(file_dl, index=False)
    return file_dl

