import numpy as np
import pandas as pd
def calculate_features(filename):
    df = pd.read_csv(filename, engine='c',dtype=np.float32)

    number_of_rows, number_of_columns = df.shape

    dv = np.empty(number_of_rows,dtype=np.float32)
    slopes = np.empty(number_of_rows,dtype=np.float32)
    theta = np.empty(number_of_rows,dtype=np.float32)
    slope = 0.0
    for i in xrange(number_of_rows):
        if (i != 0):
            xdiff = df['x'][i] - df['x'][i - 1]
            if xdiff == 0:
                slope = 99999.0
            else:
                slope = (df['y'][i] - df['y'][i - 1])/xdiff
            dist = np.sqrt(pow((df['x'][i] - df['x'][i - 1]), 2) + pow((df['y'][i] - df['y'][i - 1]), 2))
            if i == 1:
                th = 0.0
            else:
                th = abs((slope - slopes[i - 1])/(1 + slope * slopes[i - 1]))
        else:
            dist = 0.0
            slope = 0.0
            th = 0.0
        dv[i] = dist
        slopes[i] = slope
        theta[i] = th 
    dvp = dv[dv > 0.0]

    av = np.empty(number_of_rows,dtype=np.float32)
    for i in xrange(dv.size):
        if (i != 0):
            acc = dv[i] - dv[i - 1]
        else:
            acc = dv[i]
        av[i] = acc

    avp = av[av > 0.0]
    avn = av[av < 0.0]
    avz = av[av == 0.0]
    ts = []
    for i in range(theta.size):
        if theta[i] > 1:
            ts.append((dv[i] + dv[i - 1])/2)
    tsm = 0.0
    if len(ts) > 0:    
        tsm = np.mean(ts)
    f_mean_acc = avp.mean()
    f_max_acc = avp.max()
    f_min_acc = avp.min()
    f_std_acc = avp.std()
    f_mean_dcc = avn.mean()
    f_max_dcc = avn.max()
    f_min_dcc = avn.min()
    f_std_dcc = avn.std()
    f_const_speed_time = avz.size
    f_trip_time = dv.size 
    f_driving_time = dvp.size
    f_mean_speed_with_stops = dv.mean()
    f_std_speed_with_stops = dv.std()
    f_mean_speed = dvp.mean()
    f_max_speed = dvp.max()
    f_min_speed = dvp.min()
    f_std_speed = dvp.std()
    f_ratio_movement_ba = np.float32(dvp.size)/ np.float32(avp.size + avn.size)
    f_tdist = dvp.sum()

    # return (dict(trip_time=f_trip_time, driving_time=f_driving_time, mean_speed_with_stops=f_mean_speed_with_stops, std_speed_with_stops=f_std_speed_with_stops, mean_speed=f_mean_speed, std_speed=f_std_speed, const_speed_time=f_const_speed_time, mean_acc=f_mean_acc, std_acc=f_std_acc, mean_dcc=f_mean_dcc, std_dcc=f_std_dcc))
    return (f_tdist, tsm,f_max_speed,f_min_speed,f_max_acc,f_min_acc,f_max_dcc,f_min_dcc,f_mean_speed_with_stops, f_std_speed_with_stops, f_mean_speed, f_std_speed, f_const_speed_time, f_mean_acc, f_std_acc, f_mean_dcc, f_std_dcc,f_ratio_movement_ba)
    #return (dict(max_speed=f_max_speed,min_speed=f_max_speed,max_acc=f_max_acc,min_acc=f_min_acc,max_dcc=f_max_dcc,min_dcc=f_min_dcc,mean_speed_with_stops=f_mean_speed_with_stops, std_speed_with_stops=f_std_speed_with_stops, mean_speed=f_mean_speed, std_speed=f_std_speed, const_speed_time=f_const_speed_time, mean_acc=f_mean_acc, std_acc=f_std_acc, mean_dcc=f_mean_dcc, std_dcc=f_std_dcc))



