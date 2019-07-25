def parse_time_v2(pd, np, df, data):
   import time
   import calendar   
    
   DT = []
   ET = []
   DoY = []
   
   ds = df.loc[:, 'TimeEnding':'TimeEnding':1].values #extract date from data frame
   
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
   df["PM1"].fillna(-1.00e+20, inplace = True) 
   df["PM2.5"].fillna(-1.00e+20, inplace = True) 
   df["PM4"].fillna(-1.00e+20, inplace = True) 
   df["PM10"].fillna(-1.00e+20, inplace = True) 
   df["PC"].fillna(-1.00e+20, inplace = True) 
   df["TSP"].fillna(-1.00e+20, inplace = True) 
   
   pm1 = df.loc[:, 'PM1':'PM1':1].values
   flag_pm1 = df.loc[:, 'PM1_Flag':'PM1_Flag':1].values
   pm25 = df.loc[:, 'PM2.5':'PM2.5':1].values
   flag_pm25 = df.loc[:, 'PM2.5_Flag':'PM2.5_Flag':1].values
   pm4 = df.loc[:, 'PM4':'PM4':1].values
   flag_pm4 = df.loc[:, 'PM4_Flag':'PM4_Flag':1].values
   pm10 = df.loc[:, 'PM10':'PM10':1].values
   flag_pm10 = df.loc[:, 'PM10_Flag':'PM10_Flag':1].values
   pm_tot = df.loc[:, 'PC':'PC':1].values
   flag_pm_tot = df.loc[:, 'PC_Flag':'PC_Flag':1].values
   n = df.loc[:, 'TSP':'TSP':1].values
   flag_n = df.loc[:, 'TSP_Flag':'TSP_Flag':1].values
   
   data.pm1 = np.array(pm1)
   data.flag_pm1 = np.array(flag_pm1)
   data.pm25 = np.array(pm25)
   data.flag_pm25 = np.array(flag_pm25)
   data.pm4 = np.array(pm4)
   data.flag_pm4 = np.array(flag_pm4)
   data.pm10 = np.array(pm10)
   data.flag_pm10 = np.array(flag_pm10)
   data.pm_tot = np.array(pm_tot)
   data.flag_pm_tot = np.array(flag_pm_tot)
   data.n = np.array(n)
   data.flag_n = np.array(flag_n)
   
   #flag any data < 0 cannot have a -'ve concentration
   ii = np.where(data.pm1 <= 0)
   data.flag_pm1[ii] = 2
   ii = np.where(data.pm1 > 9000)
   data.flag_pm1[ii] = 2
   ii = np.where(data.pm25 <= 0)
   data.flag_pm25[ii] = 2
   ii = np.where(data.pm25 > 9000)
   data.flag_pm25[ii] = 2
   ii = np.where(data.pm4 <= 0)
   data.flag_pm4[ii] = 2
   ii = np.where(data.pm4 > 9000)
   data.flag_pm4[ii] = 2
   ii = np.where(data.pm10 <= 0)
   data.flag_pm10[ii] = 2
   ii = np.where(data.pm10 > 9000)
   data.flag_pm10[ii] = 2
   ii = np.where(data.pm_tot <= 0)
   data.flag_pm_tot[ii] = 2
   ii = np.where(data.pm_tot > 9000)
   data.flag_pm_tot[ii] = 2
   ii = np.where(data.n <= 0)
   data.flag_n[ii] = 2
   ii = np.where(data.n > 9000)
   data.flag_n[ii] = 2
		       
   return data