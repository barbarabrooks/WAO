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
   df["CH4_ppb"].fillna(-1.00e+20, inplace = True)
   df["N2O_ppb"].fillna(-1.00e+20, inplace = True)
   df["CO_ppb"].fillna(-1.00e+20, inplace = True)
   
   ch4 = df.loc[:, 'CH4_ppb':'CH4_ppb':1].values
   flag_ch4 = df.loc[:, 'CH4_Flag':'CH4_Flag':1].values
   n2o = df.loc[:, 'N2O_ppb':'N2O_ppb':1].values
   flag_n2o = df.loc[:, 'N2O_Flag':'N2O_Flag':1].values
   co = df.loc[:, 'CO_ppb':'CO_ppb':1].values
   flag_co = df.loc[:, 'CO_Flag':'CO_Flag':1].values
   
   data.ch4 = np.array(ch4)
   data.flag_ch4 = np.array(flag_ch4)
   data.n2o = np.array(n2o)
   data.flag_n2o = np.array(flag_n2o)
   data.co = np.array(co)
   data.flag_co = np.array(flag_co)
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(data.ch4 <= 0)
   data.flag_ch4[ii] = 2
   ii = np.where(data.ch4 > 9000)
   data.flag_ch4[ii] = 2
   ii = np.where(data.n2o <= 0)
   data.flag_n2o[ii] = 2
   ii = np.where(data.n2o > 9000)
   data.flag_n2o[ii] = 2
   ii = np.where(data.co <= 0)
   data.flag_co[ii] = 2
   ii = np.where(data.co > 9000)
   data.flag_co[ii] = 2
		       
   return data