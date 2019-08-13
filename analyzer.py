import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import pandas as pd
import seaborn as sb



df = pd.read_csv('dump-2019-04-25-09-00-48.csv')
select = ['name','time','FPA','FPB','FPC','Q1','Q2','Q3']
X = np.array(df.drop(select, axis=1))
kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(X)
df['KM-Classes'] = kmeans.labels_


print(df['KM-Classes'].value_counts())
'''
print(df.dtypes)

print(df['P1'].value_counts())
print(df['P2'].value_counts())
print(df['P3'].value_counts())
'''
