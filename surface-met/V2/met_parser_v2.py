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
   df["Relative_Humidity"].fillna(-1.00e+20, inplace = True) 
   df["Temperature"].fillna(-1.00e+20, inplace = True) 
   df["Irradiance"].fillna(-1.00e+20, inplace = True) 
   df["Net_Irradiance"].fillna(-1.00e+20, inplace = True) 
   df["Wind_Speed"].fillna(-1.00e+20, inplace = True) 
   df["Wind_Direction"].fillna(-1.00e+20, inplace = True) 
   df["Atmospheric_pressure"].fillna(-1.00e+20, inplace = True) 
   
   rh = df.loc[:, 'Relative_Humidity':'Relative_Humidity':1].values
   flag_rh = df.loc[:, 'Relative_Humidity_Flag':'Relative_Humidity_Flag':1].values
   tt = df.loc[:, 'Temperature':'Temperature':1].values
   flag_tt = df.loc[:, 'Temperature_Flag':'Temperature_Flag':1].values
   rad = df.loc[:, 'Irradiance':'Irradiance':1].values
   flag_rad = df.loc[:, 'Irradiance_Flag':'Irradiance_Flag':1].values
   net_rad = df.loc[:, 'Net_Irradiance':'Net_Irradiance':1].values
   flag_net_rad = df.loc[:, 'Net_Irradiance_Flag':'Net_Irradiance_Flag':1].values
   ws = df.loc[:, 'Wind_Speed':'Wind_Speed':1].values
   flag_ws = df.loc[:, 'Wind_Speed_Flag':'Wind_Speed_Flag':1].values
   wd = df.loc[:, 'Wind_Direction':'Wind_Direction':1].values
   flag_wd = df.loc[:, 'Wind_Direction_Flag':'Wind_Direction_Flag':1].values
   pp = df.loc[:, 'Atmospheric_pressure':'Atmospheric_pressure':1].values
   flag_pp = df.loc[:, 'Atmospheric_pressure_Flag':'Atmospheric_pressure_Flag':1].values
   
   data.rh = np.array(rh)
   data.flag_rh = np.array(flag_rh)
   data.tt = np.array(tt) + 273.15
   data.flag_tt = np.array(flag_tt)
   data.rad = np.array(rad)
   data.flag_rad = np.array(flag_rad)
   data.net_rad = np.array(net_rad)
   data.flag_net_rad = np.array(flag_net_rad)
   data.ws = np.array(ws)
   data.flag_ws = np.array(flag_ws)
   data.wd = np.array(wd)
   data.flag_wd = np.array(flag_wd)
   data.pp = np.array(pp)
   data.flag_pp = np.array(flag_pp)
   
   #QC data
   ii = np.where(data.rh <= 0)
   data.flag_rh[ii] = 2
   ii = np.where(data.rh > 100)
   data.flag_rh[ii] = 2
   
   ii = np.where(data.tt <= 243)
   data.flag_tt[ii] = 2
   ii = np.where(data.tt > 323)
   data.flag_tt[ii] = 2
   
   ii = np.where(data.rad <= 0)
   data.flag_rad[ii] = 2
   ii = np.where(data.rad > 1000)
   data.flag_rad[ii] = 2
   
   ii = np.where(data.net_rad <= -1000)
   data.flag_net_rad[ii] = 2
   ii = np.where(data.net_rad > 1000)
   data.flag_net_rad[ii] = 2
   
   ii = np.where(data.ws <= 0)
   data.flag_ws[ii] = 2
   data.flag_wd[ii] = 2
   ii = np.where(data.ws > 50)
   data.flag_ws[ii] = 3
   
   ii = np.where(data.wd <= 0)
   data.flag_wd[ii] = 3
   ii = np.where(data.wd > 360)
   data.flag_wd[ii] = 3
   
   ii = np.where(data.pp <= 500)
   data.flag_pp[ii] = 2
   ii = np.where(data.pp > 1200)
   data.flag_pp[ii] = 2
   	       
   return data