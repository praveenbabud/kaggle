import numpy as np
import pandas as pd
import calculate_features
import os

def driver_trips(driver_number):
    number_of_trips = 200
    df = np.zeros((200,15), dtype=np.float32)
    for i in range(1,number_of_trips + 1, 1):
        filename = 'drivers/' + str(driver_number) + '/' + str(i) + '.csv'
        fdict = calculate_features.calculate_features(filename)
        df[i - 1] = fdict 
    for col in range(df.shape[1]):
        df[:,col] = (df[:,col] - df[:,col].mean())/(df[:,col].max() - df[:,col].min())
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
        #dfm = df.as_matrix()
        clusters = list()
        cluster_list = range(200) 
        n = 200 
        for i in range(n):
            clusters.append([i])
        distance_matrix = calculate_distance_matrix(dfm)                    
        cdm = calculate_cluster_distance_matrix(clusters, distance_matrix)
        for i in range(n):
            row, col, val = min_of_matrix(cdm, cluster_list)
            clusters[row].extend(clusters[col])
            clusters[col] = []
            merge_b_to_a_cluster_distance_matrix(cdm,col,row,cluster_list) 
            cluster_list.remove(col)
            #nclusters = list()
            #for j in range(len(clusters)):
            #    if len(clusters[j]) > 0:
            #        nclusters.append(clusters[j])
            #clusters = nclusters
            shall_we_stop = 0
            for j in cluster_list:
                if len(clusters[j]) > n/2:
                    shall_we_stop = 1
                    break
            if shall_we_stop == 1:
                break 
        max_len_cluster = 0
        for j in cluster_list:
            if len(clusters[j]) > len(clusters[max_len_cluster]):
                max_len_cluster = j 
        cg = []
        for i in range(len(clusters[max_len_cluster])):
            if i == 0:
                cg = dfm[clusters[max_len_cluster][i]]
            else:
                cg = cg + dfm[clusters[max_len_cluster][i]]
        cg = cg/len(clusters[max_len_cluster])
        dist_from_cg = list()
        for i in range(dfm.shape[0]):
            dist_from_cg.append(sum(pow((dfm[i] - cg),2)))
        min_dist = min(dist_from_cg)
        max_dist = max(dist_from_cg)
        prob_list = list()
        for i in range(dfm.shape[0]):
            t = 1 - sum(pow((dfm[i] - cg),2))/max_dist
            if t > 1:
                t = 1
            elif t < 0:
                t = 0
            t = round(t,2) 
            prob_list.append(t)
        if first_driver == 0:
            fileoutput.write('driver_trip,prob\n')
            first_driver = 1
        for i in range(len(prob_list)):
            strw = driver_number +  '_' + str(i+1) + ',' + str(prob_list[i]) + '\n'
            fileoutput.write(strw)
    fileoutput.close()






