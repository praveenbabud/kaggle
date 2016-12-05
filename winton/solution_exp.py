import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.cross_validation import train_test_split

df = pd.read_csv('train.csv',dtype=np.float64)
df = df.fillna(0.0)
dfm = df.as_matrix()

#scaling down the weights

dfm[:,209] = dfm[:,209] / 1000000.0
dfm[:,210] = dfm[:,209] / 1000000.0

df_train, df_non_train = train_test_split(dfm, test_size=0.4, random_state=131)
df_test, df_final_test = train_test_split(df_non_train, test_size=0.25, random_state=131)

# 0 is ID
# 1 : 25 is features
# 26 : 27 is D-2 and D-1
# 28 : 146 is Ret2 to Ret120
# 147 : 206 is Ret121 to Ret180
# 207 : 208 is D+1 and D+2
# 209 : 210 is IntraDay and Daily weights
expavgcols = [119,60,30,15,7,3,1]
def create_trainingset(df_train1, wtf):
    clf = [] # has predicts 1 for Ret_121 to Ret_180 and 1 for D+1 and 1 for D+2
# lets first make a model for Ret_121 to Ret_180
# need to create X and Y
# x is from 1 to 146 + itr_clf    
# y is 147 + itr_clf
   
    xtomodel = np.zeros((df_train1.shape[0] * 60, 34),np.float32) 
    ytomodel = np.zeros((df_train1.shape[0] * 60, 1),np.float32) 
    for itr in range(df_train1.shape[0]):
        yindex = 147
        wt = df_train1[itr, 209]
        if wtf == 0:
            wt = 1
        expavg119 = nexpavg(df_train1[itr,28:207], 119) 
        expavg60 = nexpavg(df_train1[itr,28:207], 60) 
        expavg30 = nexpavg(df_train1[itr,28:207], 30) 
        expavg15 = nexpavg(df_train1[itr,28:207], 15) 
        expavg7 = nexpavg(df_train1[itr,28:207], 7) 
        expavg3 = nexpavg(df_train1[itr,28:207], 3)
        for itr60 in range(60):
            row = itr * 60 + itr60
            for itr27 in range(27):
                xtomodel[row, itr27] = df_train1[itr, 1+itr27]
            xtomodel[row,27] = expavg119[118 + itr60]
            xtomodel[row,28] = expavg60[118 + itr60]
            xtomodel[row,29] = expavg30[118 + itr60]
            xtomodel[row,30] = expavg15[118 + itr60]
            xtomodel[row,31] = expavg7[118 + itr60]
            xtomodel[row,32] = expavg3[118 + itr60]
            xtomodel[row,33] = df_train1[itr, yindex + itr60 - 1]
            ytomodel[row,0] = df_train1[itr, yindex + itr60] 
            xtomodel[row,:] = xtomodel[row,:] * wt 
            ytomodel[row,:] = ytomodel[row,:] * wt 
    tclf = linear_model.LinearRegression()
    tclf.fit(xtomodel, ytomodel)
    clf.append(tclf)
    xtomodel1 = np.zeros((df_train1.shape[0], 33),np.float32) 
    ytomodel1 = np.zeros((df_train1.shape[0], 1),np.float32) 
    xtomodel2 = np.zeros((df_train1.shape[0], 34),np.float32) 
    ytomodel2 = np.zeros((df_train1.shape[0], 1),np.float32) 
    for itr in range(df_train1.shape[0]):
        yindex = 147
        wt = df_train1[itr, 210]
        if wtf == 0:
            wt = 1
        expavg179 = nexpavg(df_train1[itr,28:207], 179) 
        expavg90 = nexpavg(df_train1[itr,28:207], 90) 
        expavg45 = nexpavg(df_train1[itr,28:207], 45) 
        expavg22 = nexpavg(df_train1[itr,28:207], 22) 
        expavg11 = nexpavg(df_train1[itr,28:207], 11) 
        expavg5 = nexpavg(df_train1[itr,28:207], 5)
        row = itr
        for itr27 in range(27):
            xtomodel1[row, itr27] = df_train1[itr, 1+itr27]
            xtomodel2[row, itr27] = df_train1[itr, 1+itr27]
        xtomodel1[row,27] = expavg179[178]
        xtomodel1[row,28] = expavg90[178]
        xtomodel1[row,29] = expavg45[178]
        xtomodel1[row,30] = expavg22[178]
        xtomodel1[row,31] = expavg11[178]
        xtomodel1[row,32] = expavg5[178]
        
        xtomodel2[row,27] = expavg179[178]
        xtomodel2[row,28] = expavg90[178]
        xtomodel2[row,29] = expavg45[178]
        xtomodel2[row,30] = expavg22[178]
        xtomodel2[row,31] = expavg11[178]
        xtomodel2[row,32] = expavg5[178]
        xtomodel2[row,33] = df_train1[itr, 207]
        ytomodel1[row,0] = df_train1[itr, 207]
        ytomodel2[row,0] = df_train1[itr, 208]
        xtomodel1[row,:] = xtomodel1[row,:] * wt 
        ytomodel1[row,0] = ytomodel1[row,0] * wt 
        xtomodel2[row,:] = xtomodel2[row,:] * wt 
        ytomodel2[row,0] = ytomodel2[row,0] * wt 
    tclf = linear_model.LinearRegression()
    tclf.fit(xtomodel1, ytomodel1)
    clf.append(tclf)
    tclf = linear_model.LinearRegression()
    tclf.fit(xtomodel2, ytomodel2)
    clf.append(tclf)
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
    for itr in range(df_train1.shape[0]):
        exp119l = nexpavg(df_train1[itr, 27:],119)
        exp119 = exp119l[118]
        exp60l = nexpavg(df_train1[itr, 27:],60)
        exp60 = exp60l[118]
        exp30l = nexpavg(df_train1[itr, 27:],30)
        exp30 = exp30l[118]
        exp15l = nexpavg(df_train1[itr, 27:],15)
        exp15 = exp15l[118]
        exp7l = nexpavg(df_train1[itr, 27:],7)
        exp7 = exp7l[118]
        exp3l = nexpavg(df_train1[itr, 27:],3)
        exp3 = exp3l[118]
        exp179l = nexpavg(df_train1[itr, 27:],179)
        exp179 = exp179l[118]
        exp90l = nexpavg(df_train1[itr, 27:],90)
        exp90 = exp90l[118]
        exp45l = nexpavg(df_train1[itr, 27:],45)
        exp45 = exp45l[118]
        exp22l = nexpavg(df_train1[itr, 27:],22)
        exp22 = exp22l[118]
        exp11l = nexpavg(df_train1[itr, 27:],11)
        exp11 = exp11l[118]
        exp5l = nexpavg(df_train1[itr, 27:],5)
        exp5 = exp5l[118]

        for itr60 in range(60):
            if itr60 > 0:
                exp119 = (exp119 * (1.0 - 2.0/120.0)) + (2.0/120.0 * predictions[itr, itr60 - 1]) 
                exp60 = (exp60 * (1.0 - 2.0/61.0)) + (2.0/61.0 * predictions[itr, itr60 - 1]) 
                exp30 = (exp30 * (1.0 - 2.0/31.0)) + (2.0/31.0 * predictions[itr, itr60 - 1]) 
                exp15 = (exp15 * (1.0 - 2.0/16.0)) + (2.0/16.0 * predictions[itr, itr60 - 1]) 
                exp7 = (exp7 * (1.0 - 2.0/8.0)) + (2.0/8.0 * predictions[itr, itr60 - 1]) 
                exp3 = (exp3 * (1.0 - 2.0/4.0)) + (2.0/4.0 * predictions[itr, itr60 - 1])
                exp179 = (exp179 * (1.0 - 2.0/120.0)) + (2.0/120.0 * predictions[itr, itr60 - 1]) 
                exp90 = (exp90 * (1.0 - 2.0/61.0)) + (2.0/61.0 * predictions[itr, itr60 - 1]) 
                exp45 = (exp45 * (1.0 - 2.0/31.0)) + (2.0/31.0 * predictions[itr, itr60 - 1]) 
                exp22 = (exp22 * (1.0 - 2.0/16.0)) + (2.0/16.0 * predictions[itr, itr60 - 1]) 
                exp11 = (exp11 * (1.0 - 2.0/8.0)) + (2.0/8.0 * predictions[itr, itr60 - 1]) 
                exp5 = (exp5 * (1.0 - 2.0/4.0)) + (2.0/4.0 * predictions[itr, itr60 - 1])
            xtopredict = np.zeros((1,34), np.float64)
            xtopredict[0,:27] = df_train1[itr, 1:28]
            xtopredict[0,27] = exp119
            xtopredict[0,28] = exp60
            xtopredict[0,29] = exp30
            xtopredict[0,30] = exp15
            xtopredict[0,31] = exp7
            xtopredict[0,32] = exp3
            xtopredict[0,33] = predictions[itr, itr60 - 1]
            tp = clf[0].predict(xtopredict)
            predictions[itr, itr60] = tp.flatten()
        for itr2 in range(2):
            if itr2 > 0:
                xtopredict = np.zeros((1,34), np.float64)
            else:
                xtopredict = np.zeros((1,33), np.float64)
            xtopredict[0,:27] = df_train1[itr, 1:28]
            xtopredict[0,27] = exp179
            xtopredict[0,28] = exp90
            xtopredict[0,29] = exp45
            xtopredict[0,30] = exp22
            xtopredict[0,31] = exp11
            xtopredict[0,32] = exp5
            tp = 0.0
            if itr2 > 0:
                xtopredict[0,33] = predictions[itr, 60]
                tp = clf[2].predict(xtopredict)
            else:
                tp = clf[1].predict(xtopredict)
            predictions[itr, 60 + itr2] = tp.flatten()
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

dft = pd.read_csv('test_2.csv',dtype=np.float64)
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





fileoutput = open('predictions_exp_no_wt.txt', 'a')
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


