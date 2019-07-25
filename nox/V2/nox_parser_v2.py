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
   df["NO_ppb"].fillna(-1.00e+20, inplace = True)
   df["NO2_ppb"].fillna(-1.00e+20, inplace = True)
   df["NOx_ppb"].fillna(-1.00e+20, inplace = True)
   
   no = df.loc[:, 'NO_ppb':'NO_ppb':1].values
   flag_no = df.loc[:, 'NO_Flag':'NO_Flag':1].values
   no2 = df.loc[:, 'NO2_ppb':'NO2_ppb':1].values
   flag_no2 = df.loc[:, 'NO2_Flag':'NO2_Flag':1].values
   nox = df.loc[:, 'NOx_ppb':'NOx_ppb':1].values
   flag_nox = df.loc[:, 'NOx_Flag':'NOx_Flag':1].values
   
   data.no = np.array(no)
   data.flag_no = np.array(flag_no)
   data.no2 = np.array(no2)
   data.flag_no2 = np.array(flag_no2)
   data.nox = np.array(nox)
   data.flag_nox = np.array(flag_nox)

   ii = np.where(data.no <= 0)
   data.flag_no[ii] = 2 
   ii = np.where(data.no > 9000)
   data.flag_no[ii] = 2
   ii = np.where(data.no2 <= 0)
   data.flag_no2[ii] = 2 
   ii = np.where(data.no2 > 9000)
   data.flag_no2[ii] = 2
   ii = np.where(data.nox <= 0)
   data.flag_nox[ii] = 2 
   ii = np.where(data.nox > 9000)
   data.flag_nox[ii] = 2
   
   return data