import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.cross_validation import train_test_split

df = pd.read_csv('train.csv',dtype=np.float64)
df = df.fillna(0.0)
dfm = df.as_matrix()

#scaling down the weights

#dfm[:,209] = dfm[:,209] / 1000000.0
#dfm[:,210] = dfm[:,209] / 1000000.0

df_train, df_non_train = train_test_split(dfm, test_size=0.4, random_state=131)
df_test, df_final_test = train_test_split(df_non_train, test_size=0.25, random_state=131)

# 0 is ID
# 1 : 25 is features
# 26 : 27 is D-2 and D-1
# 28 : 146 is Ret2 to Ret120
# 147 : 206 is Ret121 to Ret180
# 207 : 208 is D+1 and D+2
# 209 : 210 is IntraDay and Daily weights

def create_models(df_train1, scaleto): 
    how_many = 62
    clf = [] # has 62 predicts Ret_121 to Ret_180 and D+1 and D+2
# lets first make a model for Ret_121
# need to create X and Y
# x is from 1 to 146 + itr_clf    
# y is 147 + itr_clf
    
    for itr_clf in range(how_many):
        yindex = 147 + itr_clf 
        xtomodel = df_train1[:, 1:yindex]
        #xtotest = df_test[:, 1:yindex]
        ytomodel = df_train1[:, yindex:(yindex + 1)]
        #ytotest = df_test[:, yindex:(yindex + 1)]

        wtindex = 209 
        if itr_clf >= 60:
            wtindex = 210
        for i in range(xtomodel.shape[0]):
            wt = 1.0
            wt = df_train1[i, wtindex] ** scaleto
            #wt = wt ** 2
            #wt = df_train[i, wtindex] * df_train[i, wtindex]
            #wt = df_train[i, wtindex]
            xtomodel[i,:] = xtomodel[i,:] * wt 
            ytomodel[i,:] = ytomodel[i,:] * wt 

        tclf = linear_model.LinearRegression()
        tclf.fit(xtomodel, ytomodel)
        clf.append(tclf)
        #dlog = "Done with " + str(itr_clf + 1)
        #print dlog
    return clf

def navg(array, n):
    ret = array.copy()
    for z in range(len(array)):
        zplusone = z + 1
        if zplusone >= n:
            tot = 0.0
            for i in range(n):
                tot = tot + array[z - i]
            ret[z] = tot/n
        else:
            tot = 0.0
            for i in range(zplusone):
                tot = tot + array[i]
            ret[z] = tot/zplusone
    return ret


def plotxy(dfm,x,y,rows):
    close()
    for z in range(rows):
        plot(dfm[z][x], dfm[z][y],'bo')

def plotrow(dfp,row):
    close()
    x = 0
    for z in range(26,209):
        #plot(x, dfp[row,z],'bo')
        #plot(x, dfp[row,z],'bl')
        x = x + 1


def wmae(df_train1, predictions):
    #predictions in N by 62 array
    # 147 to 208 are the actual values in df_train array
    n = df_train1.shape[0] * 62
    ret_val = 0.0
    dtindex = 147
    for z in range(df_train1.shape[0]):
        for i in range(62):
            wtindex = 210
            if i < 60:
                wtindex = 209
            ret_val = ret_val + abs(df_train1[z,(dtindex + i)] - predictions[z,i]) * df_train1[z, wtindex]
    return ret_val/n

def predict_future(df_train1,clf):
    predictions = np.zeros((df_train1.shape[0],62),dtype=np.float64)
    for i in range(62):
        xpredict = np.zeros((df_train1.shape[0], 146 + i), dtype=np.float64)
        xpredict[:,0:146] = df_train1[:,1:147]
        if i > 0:
            for z in range(i):
                xpredict[:,(146 + z)] = predictions[:, z]
        tp = clf[i].predict(xpredict)
        predictions[:,i] = tp.flatten()
    return predictions


scaleto_vector = [1.0,0.5,0.3334,0.25,0.2,0.1667]
scaleto_vector = [0]
for i in scaleto_vector:
    clf = create_models(df_train,i)
    predictions = predict_future(df_train, clf)
    merror = wmae(df_train, predictions)
    dlog = "Error with train " + str(i) + " is " + str(merror)
    print dlog
    merror = wmae(df_test, predictions)
    dlog = "Error with test " + str(i) + " is " + str(merror)
    print dlog

dft = pd.read_csv('test.csv',dtype=np.float64)
dft = dft.fillna(0.0)
dftm = dft.as_matrix()

predictions = np.zeros((dftm.shape[0],62),dtype=np.float64)
for i in range(62):
    xpredict = np.zeros((dftm.shape[0], 146 + i), dtype=np.float64)
    xpredict[:,0:146] = dftm[:,1:147]
    if i > 0:
        for z in range(i):
            xpredict[:,(146 + z)] = predictions[:, z]
    tp = clf[i].predict(xpredict)
    predictions[:,i] = tp.flatten() 





fileoutput = open('predictions.txt', 'a')
fileoutput.write('Id,Predicted\n')
for i in range(predictions.shape[0]):
    id = 1 + i
    for j in range(62):
        sub_id = j + 1
        strw = str(id) + '_' + str(sub_id) + ',' + str(predictions[i,j]) + '\n'
        fileoutput.write(strw)
fileoutput.close()
 
def nexpavg(array, n):
    ret = array.copy()
    k = 1.0 * 2/(n + 1)
    prev = 0.0
    prev_is_set = 0
    for z in range(len(array)):
        if prev_is_set == 0:
            prev = array[z]
            prev_is_set = 1
        else:
            prev = (k * array[z]) + ((1 - k) * prev)
        ret[z] = prev
    return ret


