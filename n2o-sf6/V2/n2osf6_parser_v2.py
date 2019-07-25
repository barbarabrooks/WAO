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
   df["N2O_ppb"].fillna(-1.00e+20, inplace = True)
   df["SF6_ppt"].fillna(-1.00e+20, inplace = True)
   
   n2o = df.loc[:, 'N2O_ppb':'N2O_ppb':1].values
   flag_n2o = df.loc[:, 'N2O_Flag':'N2O_Flag':1].values
   sf6 = df.loc[:, 'SF6_ppt':'SF6_ppt':1].values
   flag_sf6 = df.loc[:, 'SF6_Flag':'SF6_Flag':1].values
   
   data.n2o = np.array(n2o)
   data.flag_n2o = np.array(flag_n2o)
   data.sf6 = np.array(sf6)
   data.flag_sf6 = np.array(flag_sf6)
   
   ii = np.where(data.n2o <= 0)
   data.flag_n2o[ii] = 2 
   ii = np.where(data.n2o > 9000)
   data.flag_n2o[ii] = 2 
   ii = np.where(data.sf6 <= 0)
   data.flag_sf6[ii] = 2 
   ii = np.where(data.sf6 > 9000)
   data.flag_sf6[ii] = 2 
   
   return data