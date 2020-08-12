from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np


def cluster(path, model, cluster_cnt):
    df = pd.read_csv(path)
    X = df.iloc[:, 1:]
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
    df = pd.read_csv(path)
    df_X_train = df.iloc[length:, 1:]
    df_y_train = df.iloc[length:, -1]
    df_X_pred = df.iloc[length+1:, 1:]
    if model =='svm':
    #X_train, X_test, y_train, y_test = train_test_split(df_X, df_y, test_size)
        clf = SVC(kernel)
    if model =='knn':
        clf = KNeighborsClassifier(n_neighbors=neighbors_cnt)

    clf.fit(df_X_train, df_y_train)
    df.iloc[length+1:, -1] = clf.predict(df_X_pred)
    file_dl = './download/classification-result.csv'
    df.to_csv(file_dl, index=False)
    return file_dl

