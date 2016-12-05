import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

df = pd.read_csv('train.csv')

rcols = df.columns.difference(['Id','Cover_Type'])

rcols = [u'Elevation', u'Aspect', u'Slope', u'Horizontal_Distance_To_Hydrology', u'Vertical_Distance_To_Hydrology', u'Horizontal_Distance_To_Roadways', u'Hillshade_9am', u'Hillshade_Noon', u'Hillshade_3pm', u'Horizontal_Distance_To_Fire_Points']
rcols = ['Slope']
from sklearn import cross_validation

dfm = df.as_matrix(columns=rcols)
dfr = df.as_matrix(columns=['Cover_Type'])
maxlist = []
for colname in rcols:
  teemp = max(df[colname])
  if (teemp == 0):
    teemp = 1
  teemp = teemp + 1
  maxlist.append(teemp)


ndfm = dfm.astype(dtype=np.float16)
ndfm = ndfm / maxlist
X_train, X_test, y_train, y_test = cross_validation.train_test_split(ndfm, dfr, test_size=0.4, random_state=536)

from sklearn import tree
clf = tree.DecisionTreeClassifier(criterion='gini',max_depth=8)
clf.fit(X_train, y_train)

from sklearn.externals.six import StringIO

with open("iris.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)

testresult = clf.predict(X_test)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, testresult)
import os
import pydot 

from sklearn.externals.six import StringIO  
import pydot 
dot_data = StringIO() 
tree.export_graphviz(clf, out_file=dot_data) 
graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
graph.write_pdf("iris.pdf") 




close();fig = plt.figure();ax = fig.add_subplot(1,1,1);df.plot(x='Elevation', y='Slope',ax=ax, kind='scatter');

results = clf.predict(dfm)
plt.scatter(df[idx, 'Elevation'], df[idx, 'Slope'], c=plot_colors[i])
al = [1,2,3,4,5,6,7]
al = [2]
plot_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k'] 
close();fig = plt.figure();ax1 = fig.add_subplot(2,1,1);ax2 = fig.add_subplot(2,1,2);
for i in al:
    ct = (df['Cover_Type']).as_matrix()
    idx = (ct == i) & (ct == results)
    idx = pd.Series(idx)
    dft = df[idx];
    dft.plot(ax= ax1, x='Elevation', y='Slope',c=plot_colors[0], kind='scatter')
    idx = (ct == i) & (ct != results)
    idx = pd.Series(idx); dft = df[idx]; dft.plot(ax= ax2, x='Elevation', y='Slope', c=plot_colors[1], kind='scatter');

results = clf.predict(X_train)
al = [2]
plot_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k'] 
close();fig = plt.figure();ax1 = fig.add_subplot(2,1,1);ax2 = fig.add_subplot(2,1,2);
for i in al:
    ct = y_train
    idx = (ct == i) & (ct == results)
    idx = idx
    dft = X_train[idx];
    dft.plot(ax= ax1, x='Elevation', y='Slope',c=plot_colors[0], kind='scatter')
    idx = (ct == i) & (ct != results)
    idx = pd.Series(idx);
    dft = X_train[idx]
    dft.plot(ax= ax2, x='Elevation', y='Slope', c=plot_colors[1], kind='scatter')


al = [1]
al = [1,2,3,4,5,6,7]
al = [2,7]
al = [2]
plot_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k'] 
close();fig = plt.figure();ax = fig.add_subplot(1,1,1);
for i in al:
    ct = (df['Cover_Type']).as_matrix()
    idx = (ct == i)
    idx = pd.Series(idx)
    dft = df[idx];
    dft.plot(ax= ax, x='Horizontal_Distance_To_Hydrology', y='Vertical_Distance_To_Hydrology', c=plot_colors[i-1], kind='scatter')

#trying neighbours

from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier(n_neighbors=21,weights='distance')


X_train, X_test, y_train, y_test = cross_validation.train_test_split(ndfm, dfr, test_size=0.1, random_state=536)
clf = KNeighborsClassifier(n_neighbors=11, weights='distance');
ny_train = y_train.ravel(); clf.fit(X_train, ny_train); testresult = clf.predict(X_test);
cm = confusion_matrix(y_test, testresult)
cm
cm.diagonal()
sum(cm.diagonal())
sum(cm.diagonal()) / float(sum(cm))






testresult = clf.predict(X_train)
cm = confusion_matrix(y_train, testresult)
cm




#trying svm

from sklearn import svm

clf = svm.SVC(C=0.9, kernel='linear', cache_size=1000,random_state=536,tol=0.01,max_iter=500)
ny_train = y_train.ravel()
clf.fit(X_train, ny_train)
testresult = clf.predict(X_test) 
cm = confusion_matrix(y_test, testresult)
cm
cm.diagonal()
sum(cm.diagonal())
sum(cm.diagonal()) / 6048.0



#trying bayes

from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)
testresult = gnb.predict(X_test)
cm = confusion_matrix(y_test, testresult)
cm

#bagging

from sklearn.ensemble import BaggingClassifier;
from sklearn.metrics import confusion_matrix;
clf = BaggingClassifier(n_estimators = 5, max_samples = 0.2, bootstrap = False)
ny_train = y_train.ravel()
clf = clf.fit(X_train, ny_train)
testresult = clf.predict(X_test)
cm = confusion_matrix(y_test,testresult)
cm


(base_estimator=None, n_estimators=10, max_samples=1.0, max_features=1.0, bootstrap=True, bootstrap_features=False, oob_score=False, n_jobs=1, random_state=None, verbose=0)¶

#random forests

from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier()
clf = clf.fit(X_train, y_train)
testresult = clf.predict(X_test)
cm = confusion_matrix(y_test, testresult)
cm




submission:code
testdata = pd.read_csv('/Users/praveenbabudevabhaktuni/kaggle/forest_cover_type_prediction/test.csv')
rcols = df.columns.difference(['Id','Cover_Type'])
testdatam = testdata.as_matrix(columns=rcols)
ntestdatam = testdatam.astype(dtype=np.float16)
ntestdatam = ntestdatam / maxlist
testresult = clf.predict(ntestdatam)
fileoutput = open('/Users/praveenbabudevabhaktuni/kaggle/forest_cover_type_prediction/output.txt', 'w')
fileoutput.write('Id,Cover_Type\n')
z = 15121
for x in testresult:
    strw = str(z) + ',' + str(x) + '\n'
    fileoutput.write(strw)
    z = z + 1

fileoutput.close()


