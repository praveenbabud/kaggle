number_of_years = len(unique(ddf['season']))
base_year = 2003 
#mxa = np.zeros((number_of_years,364,364,21), dtype=np.float32)
mxa = np.zeros((number_of_years,364,364,19), dtype=np.float32)
other_attributes = [('wfgm','lfgm'), ('wfga','lfga'), ('wfgm3','lfgm3'), ('wfga3','lfga3'), ('wftm','lftm'), ('wfta', 'lfta'), ('wor','lor'), ('wdr','ldr'), ('wast','last'), ('wto','lto'), ('wstl', 'lstl'), ('wblk', 'lblk'),  ('wpf', 'lpf')]
ratio_attributes = [('wfgm','wfga','lfgm','lfga'), ('wfgm3','wfga3','lfgm3','lfga3'), ('wftm','wfta','lftm','lfta')]
for i in range(ddf.shape[0]):
    season = ddf['season'][i]
    wteam = ddf['wteam'][i]
    lteam = ddf['lteam'][i]
    wscore = ddf['wscore'][i]
    lscore = ddf['lscore'][i]
    wteam = wteam - 1101
    lteam = lteam - 1101
    overtimes = ddf['numot'][i]
        
    season = season - base_year
    mxa[season][wteam][lteam][0] = mxa[season][wteam][lteam][0] + wscore
    mxa[season][lteam][wteam][0] = mxa[season][lteam][wteam][0] + lscore

    mxa[season][wteam][lteam][1] = mxa[season][wteam][lteam][1] + 1
    mxa[season][lteam][wteam][2] = mxa[season][lteam][wteam][2] + 1
    
    #if ddf['wloc'][i] == 'H':
    #    mxa[season][wteam][lteam][3] = mxa[season][wteam][lteam][3] - 1
    #    mxa[season][lteam][wteam][3] = mxa[season][lteam][wteam][3] + 1 
    #elif ddf['wloc'][i] == 'A':
    #    mxa[season][wteam][lteam][3] = mxa[season][wteam][lteam][3] + 1
    #    mxa[season][lteam][wteam][3] = mxa[season][lteam][wteam][3] - 1 

    #mxa[season][wteam][lteam][4] = mxa[season][wteam][lteam][3] + overtimes 
    #mxa[season][lteam][wteam][4] = mxa[season][lteam][wteam][3] + overtimes
 
    #k = 5 
    k = 3 
    for w,l in other_attributes:
        lose = ddf[l][i]
        win = ddf[w][i]
        mxa[season][wteam][lteam][k] = mxa[season][wteam][lteam][k] + win
        mxa[season][lteam][wteam][k] = mxa[season][lteam][wteam][k] + lose
        k = k + 1
    for wn,wd,ln,ld in ratio_attributes:
        wnv = ddf[wn][i]
        wdv = ddf[wd][i]
        lnv = ddf[ln][i]
        ldv = ddf[ld][i]
        mxa[season][wteam][lteam][k] = mxa[season][wteam][lteam][k] + wnv/wdv 
        mxa[season][lteam][wteam][k] = mxa[season][lteam][wteam][k] + lnv/ldv
        k = k + 1


number_of_years = len(unique(df['season']))
base_year = 1985
mx = np.zeros((number_of_years,364,364), dtype=np.float32)
for i in range(df.shape[0]):
    season = df['season'][i]
    wteam = df['wteam'][i]
    lteam = df['lteam'][i]
    wscore = df['wscore'][i]
    lscore = df['lscore'][i]
    wteam = wteam - 1101
    lteam = lteam - 1101
    season = season - base_year
    mx[season][wteam][lteam] = mx[season][wteam][lteam] + wscore
    mx[season][lteam][wteam] = mx[season][lteam][wteam] + lscore


for i in range(mx.shape[0]):
    s = sum(mx[i])
    if s > 0:
        mx[i] = mx[i]/sum(mx[i])


sx = np.zeros((number_of_years,364,1),dtype=np.float32)
for i in range(sdf.shape[0]):
    team = sdf['team'][i]
    team = team - 1101
    sd = sdf['seed'][i]
    season = sdf['season'][i]
    sd = sd[1:3]
    season = season - base_year
    sx[season][team][0] = int(sd)



years = [2011,2012,2013,2014]
teams_in_years = list()
for year in years:
    k = year - 2011
    season = year - 1985
    for j in range(364):
        if j == 0:
            teams_in_years.append(list())
        if sx[season][j][0] > 0:
            teams_in_years[k].append(j)




#trainingset5 = np.zeros((tddf.shape[0],43),dtype=np.float32)
trainingset5 = np.zeros((tddf.shape[0],39),dtype=np.float32)
resultset5 = np.zeros((tddf.shape[0],1),dtype=np.float32)
for i in range(tddf.shape[0]):
    highteam = 0
    lowteam = 0
    season = tddf['season'][i]
    if tddf['wteam'][i] > tddf['lteam'][i]:
        lowteam = tddf['lteam'][i] - 1101
        highteam = tddf['wteam'][i] - 1101
        resultset5[i][0] = 0
    else:
        lowteam = tddf['wteam'][i] - 1101
        highteam = tddf['lteam'][i] - 1101
        resultset5[i][0] = 1 
    #trainingset5[i][42] = sx[season - 1985][highteam] - sx[season - 1985][lowteam] 
    trainingset5[i][38] = sx[season - 1985][highteam] - sx[season - 1985][lowteam] 
    season = season - base_year
    #for z in range(21):
    #    z1 = z + 21 
    for z in range(19):
        z1 = z + 19 
        if mxa[season][highteam][lowteam][z] > 0:
            trainingset5[i][z] = mxa[season][lowteam][highteam][z]/mxa[season][highteam][lowteam][z]
        else:
            trainingset5[i][z] = mxa[season][lowteam][highteam][z]
        if sum(mxa[season,highteam,:,z]) > 0:
            if sum(mxa[season,lowteam,:,z]) > 0:
                trainingset5[i][z1] = (sum(mxa[season,lowteam,:,z])/sum(mxa[season,lowteam,:,z] > 0)) * (sum(mxa[season,highteam,:,z] > 0)/sum(mxa[season,highteam,:,z]))
        elif sum(mxa[season,lowteam,:,z]) > 0:
            trainingset5[i][z1] = sum(mxa[season,lowteam,:,z]) / sum(mxa[season,lowteam,:,z] > 0)


    

testingset = np.zeros((tdf.shape[0],3),dtype=np.float32)
for i in range(ss.shape[0]):
    ids = ss['id'][i] 
    season = int(ids[0:4])
    lowteam = int(ids[5:9])
    highteam = int(ids[10:14])
    season = season - base_year
    lowteam = lowteam - 1101
    highteam = highteam - 1101
    testingset[i][0] = sx[season][highteam] - sx[season][lowteam] 
    if mx[season][highteam][lowteam] > 0:
        testingset[i][1] = mx[season][lowteam][highteam]/mx[season][highteam][lowteam] 
    if sum(mx[season][highteam]) > 0:
        testingset[i][2] = sum(mx[season][lowteam])/sum(mx[season][highteam])




trainingset = np.zeros((tdf.shape[0],5),dtype=np.float32)
resultset = np.zeros((tdf.shape[0],1),dtype=np.float32)
resultsetl = np.zeros((tdf.shape[0],1),dtype=np.float32)
resultseth = np.zeros((tdf.shape[0],1),dtype=np.float32)
for i in range(tdf.shape[0]):
    highteam = 0
    lowteam = 0
    season = tdf['season'][i]
    season = season - base_year
    if tdf['wteam'][i] > tdf['lteam'][i]:
        lowteam = tdf['lteam'][i] - 1101
        highteam = tdf['wteam'][i] - 1101
        resultset[i][0] = 0
        resultsetl[i][0] = tdf['lscore'][i] 
        resultseth[i][0] = tdf['wscore'][i] 
    else:
        lowteam = tdf['wteam'][i] - 1101
        highteam = tdf['lteam'][i] - 1101
        resultset[i][0] = 1 
        resultsetl[i][0] = tdf['wscore'][i] 
        resultseth[i][0] = tdf['lscore'][i] 
    trainingset[i][0] = sx[season][highteam] - sx[season][lowteam] 
    if mx[season][highteam][lowteam][0] > 0:
        trainingset[i][1] = mx[season][lowteam][highteam][0]/mx[season][highteam][lowteam][0]
    if sum(mx[season,highteam,:,0]) > 0:
        trainingset[i][2] = sum(mx[season,lowteam,:,0])/sum(mx[season,highteam,:,0])
    trainingset[i][3] = mx[season][lowteam][highteam][1] - mx[season][highteam][lowteam][1]
    trainingset[i][4] = mx[season][lowteam][highteam][2] - mx[season][highteam][lowteam][2]
    

testingset = np.zeros((tdf.shape[0],3),dtype=np.float32)










testingset = np.zeros((68*67*2,3),dtype=np.float32)
i = 0
y = 0
for yearlist in teams_in_years:
    for teamx in yearlist:
        for teamy in yearlist:
            if teamx < teamy:
                highteam = teamy
                lowteam = teamx
                season = y + 2011
                season = season - base_year
                testingset[i][0] = sx[season - 1985][highteam] - sx[season - 1985][lowteam] 
                season = season - base_year
                if mx[season][highteam][lowteam] > 0:
                    testingset[i][1] = mx[season][lowteam][highteam]/mx[season][highteam][lowteam] 
                if sum(mx[season][highteam]) > 0:
                    testingset[i][2] = sum(mx[season][lowteam])/sum(mx[season][highteam])
                i = i + 1
    y = y + 1


testingset5 = np.zeros((68*67*2,39),dtype=np.float32)
i = 0
y = 0
for yearlist in teams_in_years:
    for teamx in yearlist:
        for teamy in yearlist:
            if teamx < teamy:
                highteam = teamy
                lowteam = teamx
                season = y + 2011
                testingset5[i][38] = sx[season - 1985][highteam] - sx[season - 1985][lowteam] 
                season = season - base_year
                for z in range(19):
                    z1 = z + 19 
                    if mxa[season][highteam][lowteam][z] > 0:
                        testingset5[i][z] = mxa[season][lowteam][highteam][z]/mxa[season][highteam][lowteam][z]
                    else:
                        testingset5[i][z] = mxa[season][lowteam][highteam][z]
                    if sum(mxa[season,highteam,:,z]) > 0:
                        if sum(mxa[season,lowteam,:,z]) > 0:
                            testingset5[i][z1] = (sum(mxa[season,lowteam,:,z])/sum(mxa[season,lowteam,:,z] > 0)) * (sum(mxa[season,highteam,:,z] > 0)/sum(mxa[season,highteam,:,z]))
                    elif sum(mxa[season,lowteam,:,z]) > 0:
                        testingset5[i][z1] = sum(mxa[season,lowteam,:,z]) / sum(mxa[season,lowteam,:,z] > 0)
                i = i + 1
    y = y + 1



fileoutput = open('coutput.txt', 'a')
fileoutput.write('id,pred\n')
i = 0
y = 0
for yearlist in teams_in_years:
    for teamx in yearlist:
        for teamy in yearlist:
            if teamx < teamy:
                highteam = teamy
                lowteam = teamx
                season = y + 2011
                pv1 = np.round(p5[i][0],2)
                pv2 = np.round(p[i][0],2)
                pv =  (pv1 + pv2)/2.0
                strw = str(season) + '_' + str((teamx + 1101)) +  '_' + str((teamy + 1101)) + ',' + str(np.round(pv,2)) + '\n'
                fileoutput.write(strw)
                i = i + 1
    y = y + 1
fileoutput.close()






number_of_years = len(unique(df['season']))
base_year = 1985
mx = np.zeros((number_of_years,364,364,3), dtype=np.float32)
for i in range(df.shape[0]):
    season = df['season'][i]
    wteam = df['wteam'][i]
    lteam = df['lteam'][i]
    wscore = df['wscore'][i]
    lscore = df['lscore'][i]
    wteam = wteam - 1101
    lteam = lteam - 1101
    season = season - base_year
    mx[season][wteam][lteam][0] = mx[season][wteam][lteam][0] + wscore
    mx[season][lteam][wteam][0] = mx[season][lteam][wteam][0] + lscore
    mx[season][wteam][lteam][1] = mx[season][wteam][lteam][1] + 1
    mx[season][lteam][wteam][2] = mx[season][lteam][wteam][2] + 1 



********************************
2015
********************************
sdf2015 = pd.read_csv('tourney_seeds_2015.csv')
sx2015 = np.zeros((364,1),dtype=np.float32)
for i in range(sdf2015.shape[0]):
    team = sdf2015['team'][i]
    team = team - 1101
    sd = sdf['seed'][i]
    sd = sd[1:3]
    sx2015[team][0] = int(sd)


teams_in_2015 = []
for i in range(sx2015.shape[0]):
    if sx2015[i][0] > 0:
        teams_in_2015.append(i)

ddf2015 = pd.read_csv('regular_season_detailed_results_2015.csv')
#mxa2015 = np.zeros((364,364,19), dtype=np.float32)
mxa2015 = np.zeros((364,364,21), dtype=np.float32)
other_attributes = [('wfgm','lfgm'), ('wfga','lfga'), ('wfgm3','lfgm3'), ('wfga3','lfga3'), ('wftm','lftm'), ('wfta', 'lfta'), ('wor','lor'), ('wdr','ldr'), ('wast','last'), ('wto','lto'), ('wstl', 'lstl'), ('wblk', 'lblk'),  ('wpf', 'lpf')]
ratio_attributes = [('wfgm','wfga','lfgm','lfga'), ('wfgm3','wfga3','lfgm3','lfga3'), ('wftm','wfta','lftm','lfta')]
for i in range(ddf2015.shape[0]):
    season = ddf2015['season'][i]
    wteam = ddf2015['wteam'][i]
    lteam = ddf2015['lteam'][i]
    wscore = ddf2015['wscore'][i]
    lscore = ddf2015['lscore'][i]
    overtimes = ddf2015['numot'][i]
    wteam = wteam - 1101
    lteam = lteam - 1101
    season = season - base_year
    mxa2015[wteam][lteam][0] = mxa2015[wteam][lteam][0] + wscore
    mxa2015[lteam][wteam][0] = mxa2015[lteam][wteam][0] + lscore

    mxa2015[wteam][lteam][1] = mxa2015[wteam][lteam][1] + 1
    mxa2015[lteam][wteam][2] = mxa2015[lteam][wteam][2] + 1
    if ddf2015['wloc'][i] == 'H':
        mxa2015[wteam][lteam][3] = mxa2015[wteam][lteam][3] - 1
        mxa2015[lteam][wteam][3] = mxa2015[lteam][wteam][3] + 1 
    elif ddf['wloc'][i] == 'A':
        mxa2015[wteam][lteam][3] = mxa2015[wteam][lteam][3] + 1
        mxa2015[lteam][wteam][3] = mxa2015[lteam][wteam][3] - 1 

    mxa2015[wteam][lteam][4] = mxa2015[wteam][lteam][3] + overtimes 
    mxa2015[lteam][wteam][4] = mxa2015[lteam][wteam][3] + overtimes
    #k = 3
    k = 5
    for w,l in other_attributes:
        lose = ddf2015[l][i]
        win = ddf2015[w][i]
        mxa2015[wteam][lteam][k] = mxa2015[wteam][lteam][k] + win
        mxa2015[lteam][wteam][k] = mxa2015[lteam][wteam][k] + lose
        k = k + 1
    for wn,wd,ln,ld in ratio_attributes:
        wnv = ddf2015[wn][i]
        wdv = ddf2015[wd][i]
        lnv = ddf2015[ln][i]
        ldv = ddf2015[ld][i]
        mxa2015[wteam][lteam][k] = mxa2015[wteam][lteam][k] + wnv/wdv
        mxa2015[lteam][wteam][k] = mxa2015[lteam][wteam][k] + lnv/ldv
        k = k + 1


#testingset2015 = np.zeros((34*67,39),dtype=np.float32)
testingset2015 = np.zeros((34*67,43),dtype=np.float32)
i = 0
yearlist = teams_in_2015
for teamx in yearlist:
    for teamy in yearlist:
        if teamx < teamy:
            highteam = teamy
            lowteam = teamx
            testingset2015[i][42] = sx2015[highteam] - sx2015[lowteam] 
            for z in range(21):
                z1 = z + 21 
                if mxa2015[highteam][lowteam][z] > 0:
                    testingset2015[i][z] = mxa2015[lowteam][highteam][z]/mxa2015[highteam][lowteam][z]
                else:
                    testingset2015[i][z] = mxa2015[lowteam][highteam][z]
                if sum(mxa2015[highteam,:,z]) > 0:
                    if sum(mxa2015[lowteam,:,z]) > 0:
                        testingset2015[i][z1] = (sum(mxa2015[lowteam,:,z])/sum(mxa2015[lowteam,:,z] > 0)) * (sum(mxa2015[highteam,:,z] > 0)/sum(mxa2015[highteam,:,z]))
                elif sum(mxa2015[lowteam,:,z]) > 0:
                    testingset2015[i][z1] = sum(mxa2015[lowteam,:,z]) / sum(mxa2015[lowteam,:,z] > 0)
            i = i + 1



fileoutput = open('coutput2015.txt', 'a')
fileoutput.write('id,pred\n')
k = 0
yearlist = teams_in_2015
for teamx in yearlist:
    for teamy in yearlist:
        if teamx < teamy:
            highteam = teamy 
            lowteam = teamx
            pv = np.round(pr2015[k][0],2)
            strw = '2015' + '_' + str((lowteam + 1101)) +  '_' + str((highteam + 1101)) + ',' + str(pv) + '\n'
            fileoutput.write(strw)
            k = k + 1
fileoutput.close()



apl = np.zeros((tdf.shape[0],1),dtype=np.float32)
aph = np.zeros((tdf.shape[0],1),dtype=np.float32)
for i in range(tdf.shape[0]):
    if tdf['wteam'][i] > tdf['lteam'][i]:
        apl[i] = tdf['lscore'][i]
        aph[i] = tdf['wscore'][i]
    else:
        apl[i] = tdf['wscore'][i]
        aph[i] = tdf['lscore'][i]



