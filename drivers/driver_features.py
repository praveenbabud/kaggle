import numpy as np
import pandas as pd
import calculate_features
import os
from scipy.stats import multivariate_normal

def driver_trips(driver_number):
    number_of_trips = 200
    df = np.zeros((200,18), dtype=np.float32)
    for i in range(1,number_of_trips + 1, 1):
        filename = 'drivers/' + str(driver_number) + '/' + str(i) + '.csv'
        fdict = calculate_features.calculate_features(filename)
        df[i - 1] = fdict 
    #for col in range(df.shape[1]):
        #df[:,col] = (df[:,col] - df[:,col].mean())/(df[:,col].max() - df[:,col].min())
    return df 



def calculate_cluster_distance_matrix(clusters,distance_matrix):
    cdm = np.zeros((len(clusters), len(clusters)),dtype=np.float32)
    for i in range(len(clusters)):
        for j in range(len(clusters)):
            if i < j:
                if cdm[i,j] == 0:
                    nodes_in_a = clusters[i]
                    nodes_in_b = clusters[j]
                    d = calculate_cluster_distance(distance_matrix,nodes_in_a, nodes_in_b) 
                    cdm[i,j] = d
                    cdm[j,i] = d
    return cdm 


def calculate_cluster_distance(distance_matrix,src,tgt):
    v = -1
    for i in range(len(src)):
        for j in range(len(tgt)):
            if v == -1:
                v = distance_matrix[src[i],tgt[j]]
            elif v < distance_matrix[src[i],tgt[j]]:
                v = distance_matrix[src[i],tgt[j]]
    return v
                
def min_of_matrix(dfm, cluster_list):
    row = -1
    col = -1
    val = -1
    for i in cluster_list:
        for j in cluster_list:
            if (i < j):
                if val == -1:
                    val = dfm[i,j]
                    row = i
                    col = j
                elif val > dfm[i,j]:
                    val = dfm[i,j]
                    row = i
                    col = j
    return (row, col, val)

def calculate_distance_matrix(dfm):
    distance_matrix = np.zeros((dfm.shape[0],dfm.shape[0]), dtype=np.float32)
    for i in range(dfm.shape[0]):
        for j in range(dfm.shape[0]):
            if i != j:
                if distance_matrix[i,j] == 0:
                    d = sum(pow((dfm[i] - dfm[j]),2))
                    distance_matrix[i,j] = d
                    distance_matrix[j,i] = d
    return distance_matrix

def merge_b_to_a_cluster_distance_matrix(cdm, b, a,cluster_list):
    cdm[a,b] = 0.0
    cdm[b,a] = 0.0
    for i in cluster_list:
        if i != a and i != b:
            cdm[a, i] = min(cdm[a,i], cdm[b,i])
            cdm[i, a] = cdm[a, i]
    cdm[b,:] = 0.0
    cdm[:,b] = 0.0


def run_everything():
    all_drivers = os.listdir('./drivers')
    first_driver = 0
    fileoutput = open('output.txt', 'a')
    for driver_number in all_drivers:
        if driver_number.isdigit() == False:
            continue
        dfm = driver_trips(int(driver_number))
        cmat = np.cov(dfm.T)
        meanarray = np.zeros(dfm.shape[1], dtype=np.float32)
        for i in range(dfm.shape[1]):
            meanarray[i] = (dfm[:,i]).mean()
        probs = np.zeros(dfm.shape[0], dtype=np.float32)
        for i in range(dfm.shape[0]):
            probs[i] = multivariate_normal.logpdf(dfm[i], mean=meanarray, cov=cmat,allow_singular=True)
        maxprobs = probs.max()
        for i in range(dfm.shape[0]):
            t = probs[i]/maxprobs
            if t > 1:
                t = 1
            elif t < 0:
                t = 0
            t = round(t,2) 
            probs[i] = t
        if first_driver == 0:
            fileoutput.write('driver_trip,prob\n')
            first_driver = 1
        for i in range(len(probs)):
            strw = driver_number +  '_' + str(i+1) + ',' + str(probs[i]) + '\n'
            fileoutput.write(strw)
    fileoutput.close()


def caliberate():
    df = pd.read_csv("aacoutput.txt", engine='c')
    fileoutput = open('coutput.txt', 'a')
    fileoutput.write('driver_trip,prob\n')
    number_of_rows, number_of_columns = df.shape
    driver = np.empty(200, dtype=np.float32)
    for i in range(number_of_rows):
        if i % 200 == 0:
            j = i + 200
            driver = df['prob'][i : j]
        tp = 0.0
        if df['prob'][i] > driver.mean():
            tp = 0.5 + (df['prob'][i] - driver.mean())/((driver.max() - driver.mean()) * 2)
        elif df['prob'][i] < driver.mean():
            tp = 0.5 * (driver.mean() - df['prob'][i])/(driver.mean() - driver.min())
        else:
            tp = 0.5
        if tp > 1.0:
            tp = 1.0
        elif tp < 0.0:
            tp = 0.0
        tp = round(tp,2) 
        strw = df['driver_trip'][i] +  ',' + str(tp) + '\n'
        fileoutput.write(strw)
    fileoutput.close()




def run_everything_cparser(df,dfm):
    first_driver = 0
    fileoutput = open('coutput.txt', 'a')
    j = dfm.shape[0]/200
    for z in range(j):
        driver = df['driver'][z * 200]
        dfmd = dfm[(z*200) : (z+1 * 200)]
        cmat = np.cov(dfmd.T)
        meanarray = np.zeros(dfmd.shape[1], dtype=np.float32)
        for i in range(dfmd.shape[1]):
            meanarray[i] = (dfmd[:,i]).mean()
        probs = np.zeros(dfmd.shape[0], dtype=np.float32)
        for i in range(dfmd.shape[0]):
            probs[i] = multivariate_normal.logpdf(dfmd[i], mean=meanarray, cov=cmat,allow_singular=True)
        maxprobs = probs.max()
        for i in range(dfmd.shape[0]):
            t = probs[i]/maxprobs
            if t > 1:
                t = 1
            elif t < 0:
                t = 0
            t = round(t,2) 
            probs[i] = t
        if first_driver == 0:
            fileoutput.write('driver_trip,prob\n')
            first_driver = 1
        for i in range(len(probs)):
            strw = str(driver) +  '_' + str(i+1) + ',' + str(probs[i]) + '\n'
            fileoutput.write(strw)
    fileoutput.close()


    



