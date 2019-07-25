def parse_time_v2(pd, np, df, data):
   import time 
   import calendar
    
   DT = []
   ET = []
   DoY = []
   
   ds = df.loc[:, 'Date':'Date':1].values #extract date from data frame
   
   for i in range(0, len(ds)):
      tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
		 
   data.DT = np.array(DT)
   data.DoY = np.array(DoY)
   data.ET = np.array(ET)
    
   return data
   
def parse_data_v2(pd, np, df, data):
   #remove any nans from data
   df["NO2_ppb"].fillna(-1.00e+20, inplace = True)
   
   no2 = df.loc[:, 'NO2_ppb':'NO2_ppb':1].values
   flag = df.loc[:, 'NO2_Flag':'NO2_Flag':1].values
   
   data.no2 = np.array(no2)
   data.flag = np.array(flag)

   ii = np.where(data.no2 <= 0)
   data.flag[ii] = 2 
   ii = np.where(data.no2 > 9000)
   data.flag[ii] = 2    
   return data