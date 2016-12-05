import pandas as pd
import numpy as np 
import logistic_regression

df = pd.read_csv('train.csv')
from sklearn.cross_validation import StratifiedShuffleSplit
x = df.as_matrix((df.columns).difference(['id','target']))
y = df.as_matrix(['target'])
ny = np.zeros(y.shape,dtype=np.int64)
nym = np.zeros((y.shape[0],9),dtype=np.float32)
for i in range(y.shape[0]):
    nclass = y[i][0]
    ny[i] = int(nclass[6])
    nym[i][ny[i] - 1] = 1.0
bx = 0
by = 0 
start = 0
ab = [8,1,2,6,6,1,6,2,3]
for zz in range(9):
    end = start + sum(ny == (zz + 1)) 
    for i in range(ab[zz]):
        if zz == 0 and i == 0:
            bx = x[start : end]
            by = ny[start : end]
        else:
            bx = np.append(bx, x[start:end], axis=0)
            by = np.append(by, ny[start:end], axis=0)
    start = end

bym = np.zeros((by.shape[0],9),dtype=np.float32)
for i in range(by.shape[0]):
    bym[i][by[i] - 1] = 1.0

sss = StratifiedShuffleSplit(ny, 1, test_size=0.4, random_state=0)
for train_index, test_index in sss:
    x_train, x_test = xaa[train_index], xaa[test_index]
    y_train, y_test = ny[train_index], ny[test_index]


sss = StratifiedShuffleSplit(oy, 1, test_size=0.4, random_state=0)
for train_index, test_index in sss:
    x_train, x_test = ox[train_index], ox[test_index]
    y_train, y_test = oy[train_index], oy[test_index]

ny_train = np.zeros(y_train.shape,dtype=np.int64)
for i in range(y_train.shape[0]):
    nclass = y_train[i][0]
    ny_train[i] = int(nclass[6]) 
ny_test = np.zeros(y_test.shape,dtype=np.int64)
for i in range(y_test.shape[0]):
    nclass = y_test[i][0]
    ny_test[i] = int(nclass[6])


tdf = pd.read_csv('test.csv')
x_predict = tdf.as_matrix((tdf.columns).difference(['id']))
predictions = np.zeros((y_test.shape[0],9), dtype=np.float64)
fp = np.zeros((y_test.shape[0],1), dtype=np.float64)
from sklearn import svm
for i in range(9):
    j = i + 1
    nyj = np.array(y_train == j,dtype=np.int64)
    nyjtest = np.array(y_test == j,dtype=np.int64)
    clf  = SVC()
    nnyj = nyj.ravel()
    #thetaj = logistic_regression.solve_lr(x_train, nyj, 0)
    #a,c = logistic_regression.predict_lr(x_train,nyj,thetaj)
    #print 'cost for class in training set ' + str(j) + ' is ' + str(c)
    #a,c = logistic_regression.predict_lr(x_test,nyjtest,thetaj)
    #print 'cost for class in testing set ' + str(j) + ' is ' + str(c)
    #pred = logistic_regression.predict_nlr(x_predict,thetaj)
    #b = np.array(a >= 0.5,dtype=np.float64)
    clf.fit(x_train,nyj)
    b = clf.predict(x_test) 
    cm = confusion_matrix(nyjtest, b)
    print cm
    print sum(cm[1,1])/float(sum(cm[1]))
    predictions[:,i] = a

for i in range(y_test.shape[0]):
    k = np.argmax(predictions[i,:])
    fp[i] = k + 1





fileoutput = open('predictions.txt', 'a')
fileoutput.write('id,Class_1,Class_2,Class_3,Class_4,Class_5,Class_6,Class_7,Class_8,Class_9\n')
for i in range(x_predict.shape[0]):
    j = i + 1
    strw = str(j) + ',' + str(round((predictions[0])[i],2)) + ',' + str(round((predictions[1])[i],2)) + ',' + str(round((predictions[2])[i],2)) + ',' + str(round((predictions[3])[i],2)) + ',' + str(round((predictions[4])[i],2)) + ',' + str(round((predictions[5])[i],2)) + ',' + str(round((predictions[6])[i],2)) + ',' + str(round((predictions[7])[i],2)) + ',' + str(round((predictions[8])[i],2)) + '\n'
    fileoutput.write(strw)
fileoutput.close()


def plotit(x,y,f1,f2,num,nc):
    close()
    j = 0
    disp = ['bo','go','ro','b+','g+','r+','b^','g^','r^']
    for z in range(nc):
        j = j + sum(y == z)
        for i in range(num):
            k = j + i
            plot(x[k][f1],x[k][f2],disp[y[k] - 1])


from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier

for z in range(1,101):
    for oo in range(1,50):
        clf = RandomForestClassifier(n_estimators=z)
        nx_train, ny_train = balanced_x_train(x,ny,1800)
        nny_train = ny_train.ravel()
        clf = clf.fit(nx_train, nny_train)
        testresult = clf.predict(x)
        cm = confusion_matrix(ny, testresult)
        print cm
        print oo 
        print z 
        print float(sum(cm.diagonal()))/sum(cm)


testresult = clf.predict(x_train)
cm = confusion_matrix(y_train, testresult)
print cm
print float(sum(cm.diagonal()))/sum(cm)


from sklearn.ensemble import ExtraTreesClassifier
for i in range(len(lif)):
    j = i + 1
    nx_train = np.zeros((x_train.shape[0], (x_train.shape[1] - j)), dtype=np.float64)
    nx_test = np.zeros((x_test.shape[0], (x_test.shape[1] - j)), dtype=np.float64)
    z = 0
    z1 = 0
    for k in range(x_train.shape[1]):
        if k not in  lif[0:j]:
            nx_train[:,z] = x_train[:,k]
            z = z + 1
    z = 0
    z1 = 0
    for k in range(x_test.shape[1]):
        if k not in lif[0:j]:
            nx_test[:,z] = x_test[:,k]
            z = z + 1
    clf = ExtraTreesClassifier(n_estimators=19,random_state=0)
    ny_train = y_train.ravel()
    clf = clf.fit(nx_train, ny_train)
    testresult = clf.predict(nx_test)
    cm = confusion_matrix(y_test, testresult)
    print '\nremoved features' + str(lif[:j]) + '\n' 
    print float(sum(cm.diagonal()))/sum(cm)





from sklearn.neighbors import KNeighborsClassifier
#clf = KNeighborsClassifier(n_neighbors=21,weights='uniform')
for i in range(1,21):
    clf = KNeighborsClassifier(n_neighbors=i, weights='distance');
    ny_train = y_train.ravel(); clf.fit(x_train, ny_train); testresult = clf.predict(x_test);
    cm = confusion_matrix(y_test, testresult)
    print i
    print cm
    print sum(cm.diagonal()) / float(sum(cm))
    testresult = clf.predict(x_train)
    cm = confusion_matrix(y_train, testresult)
    print cm
    print sum(cm.diagonal()) / float(sum(cm))

 
fileoutput = open('predictions.txt', 'a')
fileoutput.write('id,Class_1,Class_2,Class_3,Class_4,Class_5,Class_6,Class_7,Class_8,Class_9\n')
for i in range(preds.shape[0]):
    j = i + 1
    strw = str(j)
    for k in range(9):
        strw = strw + ',' + str(round(preds[i][k],3))
    strw = strw + '\n'
    fileoutput.write(strw)
fileoutput.close()


def plota(x,y,py,c1,f1,f2):
    for i in range(x.shape[0]):
        if y[i] == c1:
            plot(x[i,f1], x[i,f2],'bo')
        #else: 
        #    plot(x[i,f1], x[i,f2],'ro')


def writetofile(x,y,py,c1,c2):
    fileoutput = open('debug.txt','a')
    for i in range(x.shape[0]):
        if y[i] == c1:
            if y[i] == py[i]:
                wr = str(x[i]) + '\n'
                fileoutput.write(wr)
    wr = '****************\n'
    fileoutput.write(wr)
    for i in range(x.shape[0]):
        if y[i] == c1:
            if py[i] == c2:
                wr = str(x[i]) + '\n'
                fileoutput.write(wr)
    fileoutput.close()


lif = [82,55,24,44,46,79,3,47,59,74,80,92,11,13,15,39,43,61,66,20,21,87,1,10,30,38,50,70,71,76,90,4,9,12,14,51,53,85,0,31,35,57,62,81,91,8,28,40,41,45,54,68,75,23,83,7,16,19,22,25,26,29,32,33,37,42,48,49,52,58,60,64,65,67,69,72,73,77,78,86,88,89]

from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
bagging = BaggingClassifier(KNeighborsClassifier(), max_samples=0.5, max_features=0.5)



clf = RandomForestClassifier(n_estimators=100)
ny_train = y_train.ravel()
clf = clf.fit(x_train, ny_train)
testresult = clf.predict(x_test)
cm = confusion_matrix(y_test, testresult)
print cm
print float(sum(cm.diagonal()))/sum(cm)
testresult = clf.predict(x)
cm = confusion_matrix(ny, testresult)
print cm
print float(sum(cm.diagonal()))/sum(cm)




for z in range(2,101):
    clf = RandomForestClassifier(n_estimators=250)
    ny_train = y_train.ravel()
    clf = clf.fit(x_train, ny_train)
    testresult = clf.predict(x_test)
    cm = confusion_matrix(y_test, testresult)
    print cm
    print float(sum(cm.diagonal()))/sum(cm)



predictions = np.zeros((y_test.shape[0],9), dtype=np.float64)
fp = np.zeros((y_test.shape[0],1), dtype=np.float64)
for i in range(9):
    j = i + 1
    nyj = np.array(y_train == j,dtype=np.int64)
    clf = RandomForestClassifier(n_estimators=19)
    nnyj = nyj.ravel()
    clf = clf.fit(x_train, nnyj)
    pred = clf.predict_proba(x_test)
    predictions[:,i] = pred[:,1]
for i in range(y_test.shape[0]):
    k = np.argmax(predictions[i,:])
    fp[i] = k + 1

def balanced_x_train(x_train,y_train,size):
    nx_train = np.zeros((size*9,x_train.shape[1]), dtype=np.float64)
    ny_train = np.zeros((size*9,1), dtype=np.float64)
    z = np.random.choice(x_train.shape[0],x_train.shape[0],replace=False)
    for i in range(9):
        j = 0
        for k in z:
            if y_train[k] == (i+1):
                nx_train[i*size + j,:] = x_train[k,:]
                ny_train[i*size + j,0] = i + 1 
                j = j + 1
            if j == size:
                break
    return (nx_train,ny_train)


clf = svm.SVC(kernel="linear", C=1)
ny_train = y_train.ravel()
clf.fit(x_train,ny_train)
testresult = clf.predict(x_test)
cm = confusion_matrix(y_test,testresult)



svc = SVC(kernel="linear", C=1)
rfe = RFE(estimator=svc, n_features_to_select=85, step=0.40)
ny_train = y_train.ravel()
rfe.fit(x_train, ny_train)


from sklearn.feature_selection import VarianceThreshold


def scale_features(x):
    xs = np.zeros(x.shape,dtype=np.float64)
    for i in range(x.shape[1]):
        max_min_range  = float(np.max(x[:,i]) - np.min(x[:,i]))
        xs[:,i] = x[:,i]/max_min_range
    return xs


def transform_features(x):
    xt = np.zeros((x.shape[0], 2*x.shape[1]), np.float64)
    for i in range(x.shape[0]):
        xt[i,0:x.shape[1]] = x[i,:]
        xt[i,x.shape[1]:2*x.shape[1]] = np.array(x[i,:] == 0, dtype=np.float64)
    return xt


            
def plotm(x,y,py,v1,v2,start,num,fs):
    z = 1
    for i in range(x.shape[0]):
        if y[i] == v1 and py[i] == v2:
            plot(range(10),x[i,fs:(fs + 10)] + start + z, 'b-')
            z = z + 1
        if z == num:
            break



f1 = 51
f2 = 83
for i in range(x_test.shape[0]):
    if y_test[i] == 3 and py[i] == 3:
        figure(1)
        plot(x_test[i,f1],x_test[i,f2],'bo')
    elif y_test[i] == 3 and py[i] == 2:
        figure(2)
        plot(x_test[i,f1],x_test[i,f2], 'g^')
    elif y_test[i] == 2 and py[i] == 2:
        figure(3)
        plot(x_test[i,f1],x_test[i,f2], 'r+')


def plotall(x,y,z1):
    #z1 = range(a,b)
    k = 0
    z = 1
    tmp = np.zeros((1,93*5),dtype=np.float64)
    for i in range(x.shape[0]):
        if y[i] == z1[k]:
            for m in range(93*5):
                if m%5 == 0:
                    tmp[0,m] = x[i,m/5] 
            plot(range(93*5),tmp[0,:] + (k*35) + z, 'b-')
            z = z + 1
        if z == 25:
            z = 0
            k = k + 1
        if k == len(z1):
            break


def transform_features(x):
    xt = np.zeros((x.shape[0],93 * 46), np.float64)
    for i in range(x.shape[0]):
        k = 0
        for j in range((x.shape[1] - 1)):
            xt[i,k: k + (92 - j)] = x[i,(j + 1):x.shape[1]] * x[i,j]
            k = k + 92 - j
    return xt



def plotallcom(x,y,py,a,b,c):
    z = 1
    k = c + 10
    gap = 5
    tot = gap * x.shape[1]
    tmp = np.zeros((1,tot),dtype=np.float64) 
    for i in range(x.shape[0]):
        if y[i] == a and py[i] == a:
            for xi in range(tot):
                if xi%gap == 0:
                    tmp[0,xi] = x[i,xi/gap] 
            plot(range(tot),tmp[0,:] + z, 'b-')
            z = z + 1
        if z == c:
            break
    z = 1
    for i in range(x.shape[0]):
        if y[i] == b and py[i] == b:
            for xi in range(tot):
                if xi%gap == 0:
                    tmp[0,xi] = x[i,xi/gap] 
            plot(range(tot),tmp[0,:] + k + z, 'b-')
            z = z + 1
        if z == c:
            break
    z = 1
    for i in range(x.shape[0]):
        if y[i] == a and py[i] == b:
            for xi in range(tot):
                if xi%gap == 0:
                    tmp[0,xi] = x[i,xi/gap] 
            plot(range(tot),tmp[0,:] + 2*k + z, 'b-')
            z = z + 1
        if z == c:
            break
    z = 1
    for i in range(x.shape[0]):
        if y[i] == b and py[i] == a:
            for xi in range(tot):
                if xi%gap == 0:
                    tmp[0,xi] = x[i,xi/gap] 
            plot(range(tot),tmp[0,:] + 3*k + z, 'b-')
            z = z + 1
        if z == c:
            break



zv = [0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7]
zv = [0.5,0.75,1.0,1.25,1.5,1.75,2.0,2.25,2.5,2.75,3.0,3.25,3.5,3.75,4.0,4.25,4.5,4.75,5.0,6.0,7.0,8.0,9.0,10.0,15.0,20.0,25.0,30.0]
def doitnow(x, ny, z):
    zv = [0.5,0.75,0.8,0.85,0.9,0.95,1.0,1.25,1.5,1.75,2.0]
    zv = [0.7,0.75,0.8,0.85,0.9,0.95,1.0,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7]
    zv = [z]
    for zvalue in zv:
        start = 0
        end = 0
        outliers = np.zeros((x.shape[0],1),dtype=np.bool)
        for z in range(9):
            #print "working on class " + str(z+1) + '\n'
            end = start + sum(ny == (z + 1)) 
            #print "start: " + str(start) + " end: " + str(end) 
            x1 = x[start : end]
            sda = np.zeros((x1.shape[1],1),np.float64)
            totalsda = np.zeros((x1.shape[0],1),np.float64)
            mua = np.zeros((x1.shape[1],1),np.float64)
            for i in range(x1.shape[1]):
                a = x1[:,i]
                b = a > 0
                c = a[b]
                sda[i,0] = np.std(c)
                mua[i,0] = np.mean(c)
            for i in range(x1.shape[0]):
                tot = 0.0
                atri = 0
                for j in range(x1.shape[1]):
                    if x1[i,j] != 0:
                        if sda[j,0] == 0.0:
                            #tot = max(tot , 0.0)
                            tot = tot + 0.0
                        else:
                            #tot = max(tot , abs((x1[i,j] - mua[j,0])/sda[j,0]))
                            tot = tot + abs((x1[i,j] - mua[j,0])/sda[j,0])
                        atri = atri + 1
                totalsda[i,0] = tot/atri
                #totalsda[i,0] = tot
            outliers[start:end,0] = totalsda[:,0] <= zvalue
            start = end
        ox = x[outliers.flatten(),]
        oy = ny[outliers.flatten(),]
        clf = RandomForestClassifier(n_estimators=100)
        #clf = ExtraTreesClassifier(n_estimators=100)
        ny_train = oy.ravel()
        clf = clf.fit(ox, ny_train)
        testresult = clf.predict(x)
        cm = confusion_matrix(ny, testresult)
        f1=open('./testfile', 'a')
        print >> f1, cm
        print >> f1, float(sum(cm.diagonal()))/sum(cm)
        print >> f1, "percentage of training set is : " + str(float(len(oy))/float(len(ny)))
        print >> f1, "zvalue is : " + str(zvalue)
        print >> f1, str((float(sum(cm.diagonal()))/sum(cm)) - (float(len(oy))/float(len(ny))))
        print >> f1, "percentage on test data :" + str(((float(sum(cm.diagonal()))/sum(cm)) - (float(len(oy))/float(len(ny))))/(1.0 - (float(len(oy))/float(len(ny)))))
        f1.close()
        cp = testresult.flatten() == ny.flatten()
        return (outliers, cp)



def doitnow1(x, ny):
    fdata = 1
    fdatay = 1
    x1 = x.copy()
    ny1 = ny.copy()
    zv = [0.75, 0.75, 0.9, 0.85, 1.05,1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5]
    zv = [0.39, 0.43, 0.51, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]
    zv = [0.39, 0.43, 0.45, 0.47, 0.49, 0.51, 0.53, 0.55, 0.57, 0.59, 0.61, 0.63, 0.65, 0.67,0.69,0.71,0.73,0.75]
    zv1 = [0.39, 0.43, 0.45, 0.47, 0.49, 0.51, 0.53, 0.55, 0.57, 0.59, 0.61, 0.63, 0.65, 0.67,0.69,0.71,0.73,0.75]
    zv2 = [0.39, 0.43, 0.45, 0.47, 0.49, 0.51, 0.53, 0.55, 0.57, 0.59, 0.61, 0.63, 0.65, 0.67,0.69,0.71,0.73,0.75]
    for i in range(20):
        pdata, cp = doitnow(x1, ny1, zv[i])
        if i == 0:
            fdata = x1[pdata.flatten()]
            fdatay = ny1[pdata.flatten()]
        else:
            fdata = np.append(fdata, x1[pdata.flatten()], axis=0) 
            fdatay = np.append(fdatay, ny1[pdata.flatten()], axis=0)
        clf = RandomForestClassifier(n_estimators=100)
        clf = clf.fit(fdata, fdatay)
        testresult = clf.predict(x)
        cm = confusion_matrix(ny, testresult)
        print cm
        print float(sum(cm.diagonal()))/sum(cm)
        print float(len(fdatay))/float(len(ny))
        zv1[i] = float(sum(cm.diagonal()))/sum(cm)
        zv2[i] = float(len(fdatay))/float(len(ny))
        if i > 0:
            print 'percent again in overall perf for 1% increase in input data'
            print (zv1[i] - zv1[i-1])/(zv2[i] - zv2[i-1])
        print '*************'
        #wp = cp == False
        #x1 = x1[wp]
        #ny1 = ny1[wp]
        x1 = x1[(pdata == False).flatten()]
        ny1 = ny1[(pdata == False).flatten()]






fdata = np.append(np.append(np.append(x[pdata1.flatten()], x2[pdata2.flatten()], axis = 0), np.append(x3[pdata3.flatten()], x4[pdata4.flatten()], axis = 0), axis = 0), np.append(x5[pdata5.flatten()], x6, axis=0), axis = 0)
fdatay = np.append(np.append(np.append(ny[pdata1.flatten()], ny2[pdata2.flatten()], axis = 0), np.append(ny3[pdata3.flatten()], ny4[pdata4.flatten()], axis = 0), axis = 0), np.append(ny5[pdata5.flatten()], ny6, axis=0), axis = 0)


fdata = np.append(x[pdata1.flatten()], x2, axis = 0)
fdatay = np.append(ny[pdata1.flatten()], ny2, axis = 0)


fdata = np.append(np.append(x[pdata1.flatten()], x2[pdata2.flatten()], axis = 0), x3, axis = 0)
fdatay = np.append(np.append(ny[pdata1.flatten()], ny2[pdata2.flatten()], axis = 0), ny3, axis = 0)


fdata = np.append(x[pdata1.flatten()], x2[pdata2.flatten()], axis = 0)
fdatay = np.append(ny[pdata1.flatten()], ny2[pdata2.flatten()], axis = 0)








fdata = np.append(x[apdata1.flatten()], ax2, axis = 0)
fdatay = np.append(ny[apdata1.flatten()], any2, axis = 0)


fdata = np.append(np.append(x[apdata1.flatten()], ax2[apdata2.flatten()], axis = 0), ax3, axis = 0)
fdatay = np.append(np.append(ny[apdata1.flatten()], any2[apdata2.flatten()], axis = 0), any3, axis = 0)



def doitpercent(x, ny, z):
    zv = z
    for zvalue in zv:
        start = 0
        end = 0
        outliers = np.zeros((x.shape[0],1),dtype=np.bool)
        for z in range(9):
            #print "working on class " + str(z+1) + '\n'
            end = start + sum(ny == (z + 1)) 
            #print "start: " + str(start) + " end: " + str(end) 
            x1 = x[start : end]
            sda = np.zeros((x1.shape[1],1),np.float64)
            totalsda = np.zeros((x1.shape[0],1),np.float64)
            tsl = np.zeros((x1.shape[0],1),np.bool)
            mua = np.zeros((x1.shape[1],1),np.float64)
            for i in range(x1.shape[1]):
                a = x1[:,i]
                b = a > 0
                c = a[b]
                sda[i,0] = np.std(c)
                mua[i,0] = np.mean(c)
            for i in range(x1.shape[0]):
                tot = 0.0
                atri = 0
                for j in range(x1.shape[1]):
                    if x1[i,j] != 0:
                        if sda[j,0] == 0.0:
                            #tot = max(tot , 0.0)
                            tot = tot + 0.0
                        else:
                            #tot = max(tot , abs((x1[i,j] - mua[j,0])/sda[j,0]))
                            tot = tot + abs((x1[i,j] - mua[j,0])/sda[j,0])
                        atri = atri + 1
                totalsda[i,0] = tot/atri
                #totalsda[i,0] = tot
            sortorder = totalsda.argsort(axis = 0)
            count = np.int((zvalue * x1.shape[0])/100.0)
            if count == 0:
                count = 1
            for i in range(x1.shape[0]):
                if i < count:
                    tsl[sortorder[i]] = True
                #if (x1.shape[0] - i) < (2 * count):
                #    tsl[sortorder[i]] = True
            #outliers[start:end,0] = totalsda[:,0] <= zvalue
            outliers[start:end,0] = tsl.flatten()
            start = end
        ox = x[outliers.flatten(),]
        oy = ny[outliers.flatten(),]
        clf = RandomForestClassifier(n_estimators=250)
        #clf = ExtraTreesClassifier(n_estimators=100)
        ny_train = oy.ravel()
        clf = clf.fit(ox, ny_train)
        testresult = clf.predict(x)
        cm = confusion_matrix(ny, testresult)
        f1=open('./testfile', 'a')
        print >> f1, cm
        print >> f1, float(sum(cm.diagonal()))/sum(cm)
        print >> f1, "percentage of training set is : " + str(float(len(oy))/float(len(ny)))
        print >> f1, "zvalue is : " + str(zvalue)
        print >> f1, str((float(sum(cm.diagonal()))/sum(cm)) - (float(len(oy))/float(len(ny))))
        print >> f1, "percentage on test data :" + str(((float(sum(cm.diagonal()))/sum(cm)) - (float(len(oy))/float(len(ny))))/(1.0 - (float(len(oy))/float(len(ny)))))
        f1.close()
        #cp = testresult.flatten() == ny.flatten()
        #return (outliers, cp)

from sklearn import svm

def find_optimum_data(x, ny):
    prev_pref = 0.0
    poutliers = 0.0
    pcp = 0.0
    for zvalue in range(1,100):
        start = 0
        end = 0
        outliers = np.zeros((x.shape[0],1),dtype=np.bool)
        for z in range(9):
            #print "working on class " + str(z+1) + '\n'
            end = start + sum(ny == (z + 1)) 
            #print "start: " + str(start) + " end: " + str(end) 
            x1 = x[start : end]
            sda = np.zeros((x1.shape[1],1),np.float64)
            totalsda = np.zeros((x1.shape[0],1),np.float64)
            tsl = np.zeros((x1.shape[0],1),np.bool)
            mua = np.zeros((x1.shape[1],1),np.float64)
            for i in range(x1.shape[1]):
                a = x1[:,i]
                b = a > 0
                c = a[b]
                sda[i,0] = np.std(c)
                mua[i,0] = np.mean(c)
            for i in range(x1.shape[0]):
                tot = 0.0
                atri = 0
                for j in range(x1.shape[1]):
                    if x1[i,j] != 0:
                        if sda[j,0] == 0.0:
                            #tot = max(tot , 0.0)
                            tot = tot + 0.0
                        else:
                            #tot = max(tot , abs((x1[i,j] - mua[j,0])/sda[j,0]))
                            tot = tot + abs((x1[i,j] - mua[j,0])/sda[j,0])
                        atri = atri + 1
                totalsda[i,0] = tot/atri
                #totalsda[i,0] = tot
            sortorder = totalsda.argsort(axis = 0)
            count = np.int((zvalue * x1.shape[0])/100.0)
            if count == 0:
                count = 1
            for i in range(x1.shape[0]):
                if i < count:
                    tsl[sortorder[i]] = True
            outliers[start:end,0] = tsl.flatten()
            start = end
        ox = x[outliers.flatten(),]
        oy = ny[outliers.flatten(),]
        #clf = svm.SVC()
        clf = RandomForestClassifier(n_estimators=100)
        #clf = ExtraTreesClassifier(n_estimators=100)
        ny_train = oy.ravel()
        clf = clf.fit(ox, ny_train)
        testresult = clf.predict(x)
        cm = confusion_matrix(ny, testresult)
        curr_perf = float(sum(cm.diagonal()))/sum(cm)
        f1=open('./testfile', 'a')
        print >> f1, cm
        print >> f1, curr_perf
        print >> f1, "percentage of training set is : " + str(float(len(oy))/float(len(ny)))
        print >> f1, "zvalue is : " + str(zvalue)
        print >> f1, str((float(sum(cm.diagonal()))/sum(cm)) - (float(len(oy))/float(len(ny))))
        print >> f1, "percentage on test data :" + str(((float(sum(cm.diagonal()))/sum(cm)) - (float(len(oy))/float(len(ny))))/(1.0 - (float(len(oy))/float(len(ny)))))
        f1.close()
        if zvalue == 1:
            prev_perf = float(sum(cm.diagonal()))/sum(cm)
        else:
            if (curr_perf - prev_perf) < 0.01:
                return (poutliers, pcp)
        prev_perf = float(sum(cm.diagonal()))/sum(cm)
        pcp = testresult.flatten() == ny.flatten()
        poutliers = outliers


from sklearn.metrics import log_loss


def use_find_optimum_data(x, ny, nym):
    fdata = 1
    fdatay = 1
    x1 = x.copy()
    ny1 = ny.copy()
    zv1 = [0.39, 0.43, 0.45, 0.47, 0.49, 0.51, 0.53, 0.55, 0.57, 0.59, 0.61, 0.63, 0.65, 0.67,0.69,0.71,0.73,0.75]
    zv2 = [0.39, 0.43, 0.45, 0.47, 0.49, 0.51, 0.53, 0.55, 0.57, 0.59, 0.61, 0.63, 0.65, 0.67,0.69,0.71,0.73,0.75]
    pdata, cp = find_optimum_data(x1, ny1)
    fdata = x1[pdata.flatten()]
    fdatay = ny1[pdata.flatten()]
    x2 = x1[(pdata == False).flatten()]
    ny2 = ny1[(pdata == False).flatten()]
    clf8 = 0.0
    clf9 = 0.0
    clf85 = 0.0
    clf95 = 0.0
    flag8 = 0
    flag9 = 0
    flag85 = 0
    flag95 = 0
    for i in range(1000):
        #clf = svm.SVC(probability=True)
        clf = RandomForestClassifier(n_estimators=100)
        clf = clf.fit(fdata, fdatay)
        testresult = clf.predict(x)
        preds = clf.predict_proba(x)
        cm = confusion_matrix(ny, testresult)
        cp = testresult.flatten() == ny.flatten()
        print cm
        print i
        print float(sum(cm.diagonal()))/sum(cm)
        rs = np.sum(preds, axis=1)
        for zp in range(preds.shape[0]):
            preds[zp] = preds[zp] / rs[zp]
        rs = np.sum(preds, axis=1)
        for zp in range(preds.shape[0]):
            preds[zp] = preds[zp] / rs[zp]
        rs = np.sum(preds, axis=1)
        for zp in range(preds.shape[0]):
            preds[zp] = preds[zp] / rs[zp]
        print 'log loss is incorrect predictions' + str(log_loss(nym[(cp == False).flatten()], preds[(cp == False).flatten()]))
        print 'log loss is correct predictions' + str(log_loss(nym[(cp == True).flatten()], preds[(cp == True).flatten()]))
        print 'log loss is' + str(log_loss(nym, preds))
        print float(len(fdatay))/float(len(ny))
        tpreal = float(len(fdatay))/float(len(ny))
        #tpreal =  ((float(sum(cm.diagonal()))/sum(cm)) - (float(len(fdatay))/float(len(ny))))/(1.0 - (float(len(fdatay))/float(len(ny))))
        print "percentage on test data :" + str(((float(sum(cm.diagonal()))/sum(cm)) - (float(len(fdatay))/float(len(ny))))/(1.0 - (float(len(fdatay))/float(len(ny)))))
        curr1  = float(sum(cm.diagonal()))/sum(cm)
        curr2  = float(len(fdatay))/float(len(ny))
        if i > 0:
            print 'percent again in overall perf for 1% increase in input data'
            tp = (curr1 - prev1)/(curr2 - prev2)
            print tp
            if (flag8 == 0 and tpreal > 0.8):
                clf8 = clf
                flag8 = 1
            if (flag85 == 0 and tpreal > 0.85):
                clf85 = clf
                flag85 = 1
            if (flag9 == 0 and tpreal > 0.9):
                clf9 = clf
                flag9 = 1
            if (flag95 == 0 and tpreal > 0.95):
                clf95 = clf
                flag95 = 1
                return (clf8, clf85, clf9, clf95)
        print '*************'
        prev1  = float(sum(cm.diagonal()))/sum(cm)
        prev2  = float(len(fdatay))/float(len(ny))
        if prev1 == 1.0:
            return clf
        cp = testresult.flatten() == ny.flatten()
        x3 = x1[(cp == False).flatten()]
        ny3 = ny1[(cp == False).flatten()]
        wpdata, wcp = find_optimum_data(x3, ny3)
        fdata = np.append(fdata, x3[wpdata.flatten()], axis=0) 
        fdatay = np.append(fdatay, ny3[wpdata.flatten()], axis=0)
        #x2 = x2[(wpdata == False).flatten()]
        #ny2 = ny2[(wpdata == False).flatten()]



