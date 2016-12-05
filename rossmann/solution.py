df = pd.read_csv('train.csv')
dfm = np.zeros((df.shape[0],14), dtype=np.int32)

dfm[:,0] = df['Store']
dfm[:,1] = df['DayOfWeek']
dfm[:,2] = df['Sales']
dfm[:,3] = df['Customers']
dfm[:,4] = df['Open']
dfm[:,5] = df['Promo']
dfm[:,6] = df['SchoolHoliday']
#date will be in 3 columns year month day
#StateHoliday will be in 4 columns a,b,c,0
for i in range(df.shape[0]):
    year, month, day = df['Date'][i].split('-')
    dfm[i,7] = year
    dfm[i,8] = month
    dfm[i,9] = day
    if df['StateHoliday'][i] == "a":
        dfm[i,10] = 1   
        dfm[i,11] = 0   
        dfm[i,12] = 0   
        dfm[i,13] = 0   
    elif df['StateHoliday'][i] == "b":
        dfm[i,10] = 0   
        dfm[i,11] = 1   
        dfm[i,12] = 0   
        dfm[i,13] = 0   
    elif df['StateHoliday'][i] == "c":
        dfm[i,10] = 0
        dfm[i,11] = 0
        dfm[i,12] = 1  
        dfm[i,13] = 0
    else:
        dfm[i,10] = 0
        dfm[i,11] = 0
        dfm[i,12] = 0  
        dfm[i,13] = 1 


def plotstore(dfm,x,y,store):
    close()
    for z in range(dfm.shape[0]):
        if dfm[z][0] == store:
            plot(dfm[z][x], dfm[z][y],'bo')



