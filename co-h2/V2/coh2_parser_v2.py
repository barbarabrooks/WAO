def parse_time_v2(pd, np, df, data):
   import time 
   import calendar
    
   DT = []
   ET = []
   DoY = []
   
   ds = df.loc[:, 'Date':'Date':1].values #extract date from data frame
   
   for i in range(0, len(ds)):
      tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
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
   df["CO_ppb"].fillna(-1.00e+20, inplace = True)
   df["H2_ppb"].fillna(-1.00e+20, inplace = True)
   
   co = df.loc[:, 'CO_ppb':'CO_ppb':1].values
   flag_co = df.loc[:, 'CO_Flag':'CO_Flag':1].values
   h2 = df.loc[:, 'H2_ppb':'H2_ppb':1].values
   flag_h2 = df.loc[:, 'H2_Flag':'H2_Flag':1].values
   
   data.co = np.array(co)
   data.flag_co = np.array(flag_co)
   data.h2 = np.array(h2)
   data.flag_h2 = np.array(flag_h2)
		       
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(data.co <= 0)
   data.flag_co[ii] = 2
   ii = np.where(data.co > 9000)
   data.flag_co[ii] = 2
   
   ii = np.where(data.h2 <= 0)
   data.flag_h2[ii] = 2 
   ii = np.where(data.h2 > 9000)
   data.flag_h2[ii] = 2
   
   return data