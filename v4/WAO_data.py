def ncas_ceilometer_2(fn_in, data, logfile):
   import numpy as np
   import WAO_ceilometer as WAOC

   #parse the data  
   data = WAOC.ceil_parse_v2(fn_in, data)      
   
   return data
         
def ncas_co2_1(fn_in, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   from datetime import datetime
   import calendar   
   
   try:
      df = pd.read_csv(fn_in)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn_in, ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn_in + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   
   X = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag = np.array(df.loc[:, header[2]:header[2]:1].values)
   
   data.mole_frac = np.array([])
   data.mass_frac = np.array([])
   data.mole_conc = np.array([])
   data.mass_conc = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X <= 0)
   data.flag[ii] = 2
   ii = np.where(X > 9000)
   data.flag[ii] = 3
   
   #valid max and min values
   XX = X
   np.putmask(XX, data.flag != 1, np.nan)
   data.min_dat = np.float32(np.nanmin(XX))
   data.max_dat = np.float32(np.nanmax(XX))
   
   if 'mol-1' in header[1]:
      data.mole_frac = X
      if 'mmol' in header[1]:
         data.unit = '1e-3'
         data.practical_units = 'mmol mol-1'
      if 'micro' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'micro mol mol-1'   
      if 'nmol' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'nmol-1'
      if 'mpol' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'pmol mol-1'         
   if 'pp' in header[1]:
      data.mass_frac = X
      if 'ppm' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'ppm'
      if 'ppb' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'ppb'
      if 'ppt' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'ppt'
   if 'mol m-3' in header[1]: 
      data.mole_conc = X  
      data.unit = 'mol m-3'
   if 'kg m-3' in header[1]:
      data.mass_conc = X
      data.unit = 'kg m-3'
   
   return data    
         
def ncas_ftir_1(fn_in, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   from datetime import datetime
   import calendar   
   
   try:
      df = pd.read_csv(fn_in)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn_in, ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn_in + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
     
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   df[header[3]].fillna(-1.00e+20, inplace = True) 
   df[header[5]].fillna(-1.00e+20, inplace = True) 
   df[header[7]].fillna(-1.00e+20, inplace = True) 
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   X2 = np.array(df.loc[:, header[3]:header[3]:1].values)
   data.flag2 = np.array(df.loc[:, header[4]:header[4]:1].values)
   X3 = np.array(df.loc[:, header[5]:header[5]:1].values)
   data.flag3 = np.array(df.loc[:, header[6]:header[6]:1].values)
   X4 = np.array(df.loc[:, header[7]:header[7]:1].values)
   data.flag4 = np.array(df.loc[:, header[8]:header[8]:1].values)
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   
   ii = np.where(X2 <= 0)
   data.flag2[ii] = 2
   ii = np.where(X2 > 9000)
   data.flag2[ii] = 3
   
   ii = np.where(X3 <= 0)
   data.flag3[ii] = 2
   ii = np.where(X3 > 9000)
   data.flag3[ii] = 3
   
   ii = np.where(X4 <= 0)
   data.flag4[ii] = 2
   ii = np.where(X4 > 9000)
   data.flag4[ii] = 3
   
   #valid max and min values
   XX = X1
   np.putmask(XX, data.flag1 != 1, np.nan)
   data.min_dat1 = np.float32(np.nanmin(XX))
   data.max_dat1 = np.float32(np.nanmax(XX))
   
   XX = X2
   np.putmask(XX, data.flag2 != 1, np.nan)
   data.min_dat2 = np.float32(np.nanmin(XX))
   data.max_dat2 = np.float32(np.nanmax(XX))
   
   XX = X3
   np.putmask(XX, data.flag3 != 1, np.nan)
   data.min_dat3 = np.float32(np.nanmin(XX))
   data.max_dat3 = np.float32(np.nanmax(XX))
   
   XX = X4
   np.putmask(XX, data.flag4 != 1, np.nan)
   data.min_dat4 = np.float32(np.nanmin(XX))
   data.max_dat4 = np.float32(np.nanmax(XX))
   
   data.mole_frac1 = np.array([])
   data.mass_frac1 = np.array([])
   data.mole_conc1 = np.array([])
   data.mass_conc1 = np.array([])
   
   if 'mol-1' in header[1]:
      data.mole_frac1 = X1
      if 'mmol' in header[1]:
         data.unit1 = '1e-3'
         data.practical_units1 = 'mmol mol-1'
      if 'micro' in header[1]:
         data.unit1 = '1e-6'
         data.practical_units1 = 'micro mol mol-1'   
      if 'nmol' in header[1]:
         data.unit1 = '1e-9'
         data.practical_units1 = 'nmol-1'
      if 'mpol' in header[1]:
         data.unit1 = '1e-12'
         data.practical_units1 = 'pmol mol-1'         
   if 'pp' in header[1]:
      data.mass_frac1 = X1
      if 'ppm' in header[1]:
         data.unit1 = '1e-6'
         data.practical_units1 = 'ppm'
      if 'ppb' in header[1]:
         data.unit1 = '1e-9'
         data.practical_units1 = 'ppb'
      if 'ppt' in header[1]:
         data.unit1 = '1e-12'
         data.practical_units1 = 'ppt'
   if 'mol m-3' in header[1]: 
      data.mole_conc1 = X1  
      data.unit1 = 'mol m-3'
   if 'kg m-3' in header[1]:
      data.mass_conc1 = X1
      data.unit1 = 'kg m-3'
   
   data.mole_frac2 = np.array([])
   data.mass_frac2 = np.array([])
   data.mole_conc2 = np.array([])
   data.mass_conc2 = np.array([])
   
   if 'mol-1' in header[3]:
      data.mole_frac2 = X2
      if 'mmol' in header[3]:
         data.unit2 = '1e-3'
         data.practical_units2 = 'mmol mol-1'
      if 'micro' in header[3]:
         data.unit2 = '1e-6'
         data.practical_units2 = 'micro mol mol-1'   
      if 'nmol' in header[3]:
         data.unit2 = '1e-9'
         data.practical_units2 = 'nmol-1'
      if 'mpol' in header[3]:
         data.unit2 = '1e-12'
         data.practical_units2 = 'pmol mol-1'         
   if 'pp' in header[3]:
      data.mass_frac2 = X2
      if 'ppm' in header[3]:
         data.unit2 = '1e-6'
         data.practical_units2 = 'ppm'
      if 'ppb' in header[3]:
         data.unit2 = '1e-9'
         data.practical_units2 = 'ppb'
      if 'ppt' in header[3]:
         data.unit2 = '1e-12'
         data.practical_units2 = 'ppt'
   if 'mol m-3' in header[3]: 
      data.mole_conc2 = X2  
      data.unit2 = 'mol m-3'
   if 'kg m-3' in header[3]:
      data.mass_conc2 = X2
      data.unit2 = 'kg m-3'
   
   data.mole_frac3 = np.array([])
   data.mass_frac3 = np.array([])
   data.mole_conc3 = np.array([])
   data.mass_conc3 = np.array([])
   
   if 'mol-1' in header[5]:
      data.mole_frac3 = X3
      if 'mmol' in header[5]:
         data.unit3 = '1e-3'
         data.practical_units3 = 'mmol mol-1'
      if 'micro' in header[5]:
         data.unit3 = '1e-6'
         data.practical_units3 = 'micro mol mol-1'   
      if 'nmol' in header[5]:
         data.unit3 = '1e-9'
         data.practical_units3 = 'nmol-1'
      if 'mpol' in header[5]:
         data.unit3 = '1e-12'
         data.practical_units3 = 'pmol mol-1'         
   if 'pp' in header[5]:
      data.mass_frac3 = X3
      if 'ppm' in header[5]:
         data.unit3 = '1e-6'
         data.practical_units3 = 'ppm'
      if 'ppb' in header[5]:
         data.unit3 = '1e-9'
         data.practical_units3 = 'ppb'
      if 'ppt' in header[5]:
         data.unit3 = '1e-12'
         data.practical_units3 = 'ppt'
   if 'mol m-3' in header[5]: 
      data.mole_conc3 = X3  
      data.unit3 = 'mol m-3'
   if 'kg m-3' in header[5]:
      data.mass_conc3 = X3
      data.unit3 = 'kg m-3'
   
   data.mole_frac4 = np.array([])
   data.mass_frac4 = np.array([])
   data.mole_conc4 = np.array([])
   data.mass_conc4 = np.array([])
   
   if 'mol-1' in header[7]:
      data.mole_frac4 = X4
      if 'mmol' in header[7]:
         data.unit4 = '1e-3'
         data.practical_units4 = 'mmol mol-1'
      if 'micro' in header[7]:
         data.unit4 = '1e-6'
         data.practical_units4 = 'micro mol mol-1'   
      if 'nmol' in header[7]:
         data.unit4 = '1e-9'
         data.practical_units4 = 'nmol-1'
      if 'mpol' in header[7]:
         data.unit4 = '1e-12'
         data.practical_units4 = 'pmol mol-1'         
   if 'pp' in header[7]:
      data.mass_frac4 = X4
      if 'ppm' in header[7]:
         data.unit4 = '1e-6'
         data.practical_units4 = 'ppm'
      if 'ppb' in header[7]:
         data.unit4 = '1e-9'
         data.practical_units4 = 'ppb'
      if 'ppt' in header[7]:
         data.unit4 = '1e-12'
         data.practical_units4 = 'ppt'
   if 'mol m-3' in header[7]: 
      data.mole_conc4 = X4  
      data.unit4 = 'mol m-3'
   if 'kg m-3' in header[7]:
      data.mass_conc4 = X4
      data.unit4 = 'kg m-3'
 
   return data 
         
def ncas_ghg_gc_fid_1(fn_in, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   from datetime import datetime
   import calendar   
   
   try:
      df = pd.read_csv(fn_in)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn_in, ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn_in + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   
   X = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag = np.array(df.loc[:, header[2]:header[2]:1].values)
   
   data.mole_frac = np.array([])
   data.mass_frac = np.array([])
   data.mole_conc = np.array([])
   data.mass_conc = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X <= 0)
   data.flag[ii] = 2
   ii = np.where(X > 9000)
   data.flag[ii] = 3
   
   #valid max and min values
   XX = X
   np.putmask(XX, data.flag != 1, np.nan)
   data.min_dat = np.float32(np.nanmin(XX))
   data.max_dat = np.float32(np.nanmax(XX))
   
   if 'mol-1' in header[1]:
      data.mole_frac = X
      if 'mmol' in header[1]:
         data.unit = '1e-3'
         data.practical_units = 'mmol mol-1'
      if 'micro' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'micro mol mol-1'   
      if 'nmol' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'nmol-1'
      if 'mpol' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'pmol mol-1'         
   if 'pp' in header[1]:
      data.mass_frac = X
      if 'ppm' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'ppm'
      if 'ppb' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'ppb'
      if 'ppt' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'ppt'
   if 'mol m-3' in header[1]: 
      data.mole_conc = X  
      data.unit = 'mol m-3'
   if 'kg m-3' in header[1]:
      data.mass_conc = X
      data.unit = 'kg m-3'
   
   return data 

def ncas_ghg_gc_ecd_1(fn_in, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   from datetime import datetime
   import calendar   
   
   try:
      df = pd.read_csv(fn_in)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn_in, ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn_in + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   # this code has to be able to read in two different types of file
   # n20 and sf6 header has length 5
   # sf6 only header has length 3
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   if len(header) == 5:
      df[header[3]].fillna(-1.00e+20, inplace = True)
      
   X = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag = np.array(df.loc[:, header[2]:header[2]:1].values)
   if len(header) == 5:
      X1 = np.array(df.loc[:, header[3]:header[3]:1].values)
      data.flag1 = np.array(df.loc[:, header[4]:header[4]:1].values)
   
   data.mole_frac = np.array([])
   data.mass_frac = np.array([])
   data.mole_conc = np.array([])
   data.mass_conc = np.array([])
   if len(header) == 5:
      data.mole_frac1 = np.array([])
      data.mass_frac1 = np.array([])
      data.mole_conc1 = np.array([])
      data.mass_conc1 = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X <= 0)
   data.flag[ii] = 2
   ii = np.where(X > 9000)
   data.flag[ii] = 3
   if len(header) == 5:
      #flag any data < 0 cannot have a -'ve gas concentration
      ii = np.where(X1 <= 0)
      data.flag1[ii] = 2
      ii = np.where(X1 > 9000)
      data.flag1[ii] = 3
   
   #valid max and min values
   XX = X
   np.putmask(XX, data.flag != 1, np.nan)
   data.min_dat = np.float32(np.nanmin(XX))
   data.max_dat = np.float32(np.nanmax(XX))
   if len(header) == 5:
      XX = X1
      np.putmask(XX, data.flag1 != 1, np.nan)
      data.min_dat1 = np.float32(np.nanmin(XX))
      data.max_dat1 = np.float32(np.nanmax(XX))
   
   if 'mol-1' in header[1]:
      data.mole_frac = X
      if 'mmol' in header[1]:
         data.unit = '1e-3'
         data.practical_units = 'mmol mol-1'
      if 'micro' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'micro mol mol-1'   
      if 'nmol' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'nmol-1'
      if 'mpol' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'pmol mol-1'         
   if 'pp' in header[1]:
      data.mass_frac = X
      if 'ppm' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'ppm'
      if 'ppb' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'ppb'
      if 'ppt' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'ppt'
   if 'mol m-3' in header[1]: 
      data.mole_conc = X  
      data.unit = 'mol m-3'
   if 'kg m-3' in header[1]:
      data.mass_conc = X
      data.unit = 'kg m-3'
      
   if len(header) == 5:  
      if 'mol-1' in header[3]:
         data.mole_frac1 = X1
         if 'mmol' in header[3]:
            data.unit1 = '1e-3'
            data.practical_units1 = 'mmol mol-1'
         if 'micro' in header[3]:
            data.unit1 = '1e-6'
            data.practical_units1 = 'micro mol mol-1'   
         if 'nmol' in header[3]:
            data.unit1 = '1e-9'
            data.practical_units1 = 'nmol-1'
         if 'mpol' in header[3]:
            data.unit1 = '1e-12'
            data.practical_units1 = 'pmol mol-1'         
      if 'pp' in header[3]:
         data.mass_frac1 = X1
         if 'ppm' in header[3]:
            data.unit1 = '1e-6'
            data.practical_units1 = 'ppm'
         if 'ppb' in header[3]:
            data.unit1 = '1e-9'
            data.practical_units1 = 'ppb'
         if 'ppt' in header[3]:
            data.unit1 = '1e-12'
            data.practical_units1 = 'ppt'
      if 'mol m-3' in header[3]: 
         data.mole_conc1 = X1  
         data.unit1 = 'mol m-3'
      if 'kg m-3' in header[3]:
         data.mass_conc1 = X1
         data.unit1 = 'kg m-3'   
   
   return data 
         
def ncas_o2_1(fn_in, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   from datetime import datetime
   import calendar   
   
   try:
      df = pd.read_csv(fn_in)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn_in, ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn_in + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   
   X = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag = np.array(df.loc[:, header[2]:header[2]:1].values)
   
   data.O2N2 = np.array(X)
   
   # -'ve data here is valid
   ii = np.where(X >= 0)
   data.flag[ii] = 2
   ii = np.where(X > 9000)
   data.flag[ii] = 3
   
   #valid max and min values
   XX = X
   np.putmask(XX, data.flag != 1, np.nan)
   data.min_dat = np.float32(np.nanmin(XX))
   data.max_dat = np.float32(np.nanmax(XX))
   
   return data

def ncas_rga3_1(fn_in, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   from datetime import datetime
   import calendar   
   
   try:
      df = pd.read_csv(fn_in)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn_in, ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn_in + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   # this code has to be able to read in two different types of file
   # h2 and co header has length 5
   # h2 only header has length 3
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   if len(header) == 5:
      df[header[3]].fillna(-1.00e+20, inplace = True)
      
   X = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag = np.array(df.loc[:, header[2]:header[2]:1].values)
   if len(header) == 5:
      X1 = np.array(df.loc[:, header[3]:header[3]:1].values)
      data.flag1 = np.array(df.loc[:, header[4]:header[4]:1].values)
   
   data.mole_frac = np.array([])
   data.mass_frac = np.array([])
   data.mole_conc = np.array([])
   data.mass_conc = np.array([])
   if len(header) == 5:
      data.mole_frac1 = np.array([])
      data.mass_frac1 = np.array([])
      data.mole_conc1 = np.array([])
      data.mass_conc1 = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X <= 0)
   data.flag[ii] = 2
   ii = np.where(X > 9000)
   data.flag[ii] = 3
   if len(header) == 5:
      #flag any data < 0 cannot have a -'ve gas concentration
      ii = np.where(X1 <= 0)
      data.flag1[ii] = 2
      ii = np.where(X1 > 9000)
      data.flag1[ii] = 3
   
   #valid max and min values
   XX = X
   np.putmask(XX, data.flag != 1, np.nan)
   data.min_dat = np.float32(np.nanmin(XX))
   data.max_dat = np.float32(np.nanmax(XX))
   if len(header) == 5:
      XX = X1
      np.putmask(XX, data.flag1 != 1, np.nan)
      data.min_dat1 = np.float32(np.nanmin(XX))
      data.max_dat1 = np.float32(np.nanmax(XX))
   
   if 'mol-1' in header[1]:
      data.mole_frac = X
      if 'mmol' in header[1]:
         data.unit = '1e-3'
         data.practical_units = 'mmol mol-1'
      if 'micro' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'micro mol mol-1'   
      if 'nmol' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'nmol-1'
      if 'mpol' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'pmol mol-1'         
   if 'pp' in header[1]:
      data.mass_frac = X
      if 'ppm' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'ppm'
      if 'ppb' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'ppb'
      if 'ppt' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'ppt'
   if 'mol m-3' in header[1]: 
      data.mole_conc = X  
      data.unit = 'mol m-3'
   if 'kg m-3' in header[1]:
      data.mass_conc = X
      data.unit = 'kg m-3'
      
   if len(header) == 5:  
      if 'mol-1' in header[3]:
         data.mole_frac1 = X1
         if 'mmol' in header[3]:
            data.unit1 = '1e-3'
            data.practical_units1 = 'mmol mol-1'
         if 'micro' in header[3]:
            data.unit1 = '1e-6'
            data.practical_units1 = 'micro mol mol-1'   
         if 'nmol' in header[3]:
            data.unit1 = '1e-9'
            data.practical_units1 = 'nmol-1'
         if 'mpol' in header[3]:
            data.unit1 = '1e-12'
            data.practical_units1 = 'pmol mol-1'         
      if 'pp' in header[3]:
         data.mass_frac1 = X1
         if 'ppm' in header[3]:
            data.unit1 = '1e-6'
            data.practical_units1 = 'ppm'
         if 'ppb' in header[3]:
            data.unit1 = '1e-9'
            data.practical_units1 = 'ppb'
         if 'ppt' in header[3]:
            data.unit1 = '1e-12'
            data.practical_units1 = 'ppt'
      if 'mol m-3' in header[3]: 
         data.mole_conc1 = X1  
         data.unit1 = 'mol m-3'
      if 'kg m-3' in header[3]:
         data.mass_conc1 = X1
         data.unit1 = 'kg m-3'   
   
   return data 
        
def uea_42i_nox_1(fn_in, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   from datetime import datetime
   import calendar   
   
   try:
      df = pd.read_csv(fn_in)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn_in, ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn_in + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)

   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   df[header[3]].fillna(-1.00e+20, inplace = True) 
   df[header[5]].fillna(-1.00e+20, inplace = True) 
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   X2 = np.array(df.loc[:, header[3]:header[3]:1].values)
   data.flag2 = np.array(df.loc[:, header[4]:header[4]:1].values)
   X3 = np.array(df.loc[:, header[5]:header[5]:1].values)
   data.flag3 = np.array(df.loc[:, header[6]:header[6]:1].values)
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   
   ii = np.where(X2 <= 0)
   data.flag2[ii] = 2
   ii = np.where(X2 > 9000)
   data.flag2[ii] = 3
   
   ii = np.where(X3 <= 0)
   data.flag3[ii] = 2
   ii = np.where(X3 > 9000)
   data.flag3[ii] = 3
   
   #valid max and min values
   XX = X1
   np.putmask(XX, data.flag1 != 1, np.nan)
   data.min_dat1 = np.float32(np.nanmin(XX))
   data.max_dat1 = np.float32(np.nanmax(XX))
   
   XX = X2
   np.putmask(XX, data.flag2 != 1, np.nan)
   data.min_dat2 = np.float32(np.nanmin(XX))
   data.max_dat2 = np.float32(np.nanmax(XX))
   
   XX = X3
   np.putmask(XX, data.flag3 != 1, np.nan)
   data.min_dat3 = np.float32(np.nanmin(XX))
   data.max_dat3 = np.float32(np.nanmax(XX))
   
   data.mole_frac1 = np.array([])
   data.mass_frac1 = np.array([])
   data.mole_conc1 = np.array([])
   data.mass_conc1 = np.array([])
   
   if 'mol-1' in header[1]:
      data.mole_frac1 = X1
      if 'mmol' in header[1]:
         data.unit1 = '1e-3'
         data.practical_units1 = 'mmol mol-1'
      if 'micro' in header[1]:
         data.unit1 = '1e-6'
         data.practical_units1 = 'micro mol mol-1'   
      if 'nmol' in header[1]:
         data.unit1 = '1e-9'
         data.practical_units1 = 'nmol-1'
      if 'mpol' in header[1]:
         data.unit1 = '1e-12'
         data.practical_units1 = 'pmol mol-1'         
   if 'pp' in header[1]:
      data.mass_frac1 = X1
      if 'ppm' in header[1]:
         data.unit1 = '1e-6'
         data.practical_units1 = 'ppm'
      if 'ppb' in header[1]:
         data.unit1 = '1e-9'
         data.practical_units1 = 'ppb'
      if 'ppt' in header[1]:
         data.unit1 = '1e-12'
         data.practical_units1 = 'ppt'
   if 'mol m-3' in header[1]: 
      data.mole_conc1 = X1  
      data.unit1 = 'mol m-3'
   if 'kg m-3' in header[1]:
      data.mass_conc1 = X1
      data.unit1 = 'kg m-3'
   
   data.mole_frac2 = np.array([])
   data.mass_frac2 = np.array([])
   data.mole_conc2 = np.array([])
   data.mass_conc2 = np.array([])
   
   if 'mol-1' in header[3]:
      data.mole_frac2 = X2
      if 'mmol' in header[3]:
         data.unit2 = '1e-3'
         data.practical_units2 = 'mmol mol-1'
      if 'micro' in header[3]:
         data.unit2 = '1e-6'
         data.practical_units2 = 'micro mol mol-1'   
      if 'nmol' in header[3]:
         data.unit2 = '1e-9'
         data.practical_units2 = 'nmol-1'
      if 'mpol' in header[3]:
         data.unit2 = '1e-12'
         data.practical_units2 = 'pmol mol-1'         
   if 'pp' in header[3]:
      data.mass_frac2 = X2
      if 'ppm' in header[3]:
         data.unit2 = '1e-6'
         data.practical_units2 = 'ppm'
      if 'ppb' in header[3]:
         data.unit2 = '1e-9'
         data.practical_units2 = 'ppb'
      if 'ppt' in header[3]:
         data.unit2 = '1e-12'
         data.practical_units2 = 'ppt'
   if 'mol m-3' in header[3]: 
      data.mole_conc2 = X2  
      data.unit2 = 'mol m-3'
   if 'kg m-3' in header[3]:
      data.mass_conc2 = X2
      data.unit2 = 'kg m-3'
   
   data.mole_frac3 = np.array([])
   data.mass_frac3 = np.array([])
   data.mole_conc3 = np.array([])
   data.mass_conc3 = np.array([])
   
   if 'mol-1' in header[5]:
      data.mole_frac3 = X3
      if 'mmol' in header[5]:
         data.unit3 = '1e-3'
         data.practical_units3 = 'mmol mol-1'
      if 'micro' in header[5]:
         data.unit3 = '1e-6'
         data.practical_units3 = 'micro mol mol-1'   
      if 'nmol' in header[5]:
         data.unit3 = '1e-9'
         data.practical_units3 = 'nmol-1'
      if 'mpol' in header[5]:
         data.unit3 = '1e-12'
         data.practical_units3 = 'pmol mol-1'         
   if 'pp' in header[5]:
      data.mass_frac3 = X3
      if 'ppm' in header[5]:
         data.unit3 = '1e-6'
         data.practical_units3 = 'ppm'
      if 'ppb' in header[5]:
         data.unit3 = '1e-9'
         data.practical_units3 = 'ppb'
      if 'ppt' in header[5]:
         data.unit3 = '1e-12'
         data.practical_units3 = 'ppt'
   if 'mol m-3' in header[5]: 
      data.mole_conc3 = X3  
      data.unit3 = 'mol m-3'
   if 'kg m-3' in header[5]:
      data.mass_conc3 = X3
      data.unit3 = 'kg m-3'

   return data    
         
def uea_43i_so2_1(fn_in, data, logfile):
   import pandas as pd
   import numpy as np
   import time
   from datetime import datetime
   import calendar   
   
   try:
      df = pd.read_csv(fn_in)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn_in, ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn_in + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   
   X = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag = np.array(df.loc[:, header[2]:header[2]:1].values)
   
   data.mole_frac = np.array([])
   data.mass_frac = np.array([])
   data.mole_conc = np.array([])
   data.mass_conc = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X <= 0)
   data.flag[ii] = 2
   ii = np.where(X > 9000)
   data.flag[ii] = 3
   
   #valid max and min values
   XX = X
   np.putmask(XX, data.flag != 1, np.nan)
   data.min_dat = np.float32(np.nanmin(XX))
   data.max_dat = np.float32(np.nanmax(XX))
   
   if 'mol-1' in header[1]:
      data.mole_frac = X
      if 'mmol' in header[1]:
         data.unit = '1e-3'
         data.practical_units = 'mmol mol-1'
      if 'micro' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'micro mol mol-1'   
      if 'nmol' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'nmol-1'
      if 'mpol' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'pmol mol-1'         
   if 'pp' in header[1]:
      data.mass_frac = X
      if 'ppm' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'ppm'
      if 'ppb' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'ppb'
      if 'ppt' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'ppt'
   if 'mol m-3' in header[1]: 
      data.mole_conc = X  
      data.unit = 'mol m-3'
   if 'kg m-3' in header[1]:
      data.mass_conc = X
      data.unit = 'kg m-3'
   
   return data 
      
def uea_49i_o3_1(fn_in, data, logfile):
   import pandas as pd
   import numpy as np
   import time
   from datetime import datetime
   import calendar   
   
   try:
      df = pd.read_csv(fn_in)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn_in, ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn_in + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   
   X = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag = np.array(df.loc[:, header[2]:header[2]:1].values)
   
   data.mole_frac = np.array([])
   data.mass_frac = np.array([])
   data.mole_conc = np.array([])
   data.mass_conc = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X <= 0)
   data.flag[ii] = 2
   ii = np.where(X > 9000)
   data.flag[ii] = 3
   
   #valid max and min values
   XX = X
   np.putmask(XX, data.flag != 1, np.nan)
   data.min_dat = np.float32(np.nanmin(XX))
   data.max_dat = np.float32(np.nanmax(XX))
   
   if 'mol-1' in header[1]:
      data.mole_frac = X
      if 'mmol' in header[1]:
         data.unit = '1e-3'
         data.practical_units = 'mmol mol-1'
      if 'micro' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'micro mol mol-1'   
      if 'nmol' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'nmol-1'
      if 'mpol' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'pmol mol-1'         
   if 'pp' in header[1]:
      data.mass_frac = X
      if 'ppm' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'ppm'
      if 'ppb' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'ppb'
      if 'ppt' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'ppt'
   if 'mol m-3' in header[1]: 
      data.mole_conc = X  
      data.unit = 'mol m-3'
   if 'kg m-3' in header[1]:
      data.mass_conc = X
      data.unit = 'kg m-3'
   
   return data 
         
def uea_aws_1and2(fn_in, data, logfile):
   import pandas as pd
   import numpy as np
   import time
   from datetime import datetime
   import calendar   
   
   try:
      df = pd.read_csv(fn_in)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn_in, ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn_in + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   df[header[3]].fillna(-1.00e+20, inplace = True) 
   df[header[5]].fillna(-1.00e+20, inplace = True) 
   df[header[7]].fillna(-1.00e+20, inplace = True) 
   df[header[9]].fillna(-1.00e+20, inplace = True) 
   df[header[11]].fillna(-1.00e+20, inplace = True) 
   df[header[13]].fillna(-1.00e+20, inplace = True)
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   X2 = np.array(df.loc[:, header[3]:header[3]:1].values)
   data.flag2 = np.array(df.loc[:, header[4]:header[4]:1].values)
   X3 = np.array(df.loc[:, header[5]:header[5]:1].values)
   data.flag3 = np.array(df.loc[:, header[6]:header[6]:1].values)
   X4 = np.array(df.loc[:, header[7]:header[7]:1].values)
   data.flag4 = np.array(df.loc[:, header[8]:header[8]:1].values)
   X5 = np.array(df.loc[:, header[9]:header[9]:1].values)
   data.flag5 = np.array(df.loc[:, header[10]:header[10]:1].values)
   X6 = np.array(df.loc[:, header[11]:header[11]:1].values)
   data.flag6 = np.array(df.loc[:, header[12]:header[12]:1].values)
   X7 = np.array(df.loc[:, header[13]:header[13]:1].values)
   data.flag7 = np.array(df.loc[:, header[14]:header[14]:1].values)
   
   data.RH = np.array([])
   data.TT = np.array([])
   data.IR = np.array([])
   data.NetIR = np.array([])
   data.WS = np.array([])
   data.WD = np.array([])
   data.PP = np.array([])
   
   # RH
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 100)
   data.flag1[ii] = 3
   # Temperature
   ii = np.where(X2 <= -50)
   data.flag2[ii] = 2
   ii = np.where(X2 > 100)
   data.flag2[ii] = 3
   ii = np.where((X2 > -50) & (X1 < -20))
   data.flag2[ii] = 4
   ii = np.where((X2 > 40) & (X1 < 100))
   data.flag2[ii] = 5
   # Irradiance
   ii = np.where(X3 < 0)
   data.flag3[ii] = 2
   ii = np.where(X3 > 1000)
   data.flag3[ii] = 3
   # Net irradiance
   ii = np.where(X4 < -1000)
   data.flag4[ii] = 2
   ii = np.where(X4 > 1000)
   data.flag4[ii] = 3
   # Wind speed
   ii = np.where(X5 < 0)
   data.flag5[ii] = 2
   ii = np.where(X5 > 60)
   data.flag5[ii] = 3
   ii = np.where(X5 == 0)
   data.flag5[ii] = 4
   data.flag6[ii] = 4
   # Wind direction
   ii = np.where(X6 < 0)
   data.flag6[ii] = 2
   ii = np.where(X6 > 359)
   data.flag6[ii] = 3
   # Pressure
   ii = np.where(X7 <= 600)
   data.flag7[ii] = 2
   ii = np.where(X7 > 11000)
   data.flag7[ii] = 3
   
   #valid max and min values
   XX = X1
   np.putmask(XX, data.flag1 != 1, np.nan)
   data.min_dat1 = np.float32(np.nanmin(XX))
   data.max_dat1 = np.float32(np.nanmax(XX))
   
   XX = X2
   np.putmask(XX, data.flag2 != 1, np.nan)
   data.min_dat2 = np.float32(np.nanmin(XX) + 273.15)
   data.max_dat2 = np.float32(np.nanmax(XX) + 273.15)
   
   XX = X3 #Down welling
   np.putmask(XX, data.flag3 != 1, np.nan)
   data.min_dat3 = np.float32(np.nanmin(XX))
   data.max_dat3 = np.float32(np.nanmax(XX))
   
   XX = X4 #net flageed using down welling
   np.putmask(XX, data.flag3 != 1, np.nan)
   data.min_dat4 = np.float32(np.nanmin(XX))
   data.max_dat4 = np.float32(np.nanmax(XX))
   
   XX = X5
   np.putmask(XX, data.flag5 != 1, np.nan)
   data.min_dat5 = np.float32(np.nanmin(XX))
   data.max_dat5 = np.float32(np.nanmax(XX))
  
   XX = np.float32(X6)
   np.putmask(XX, data.flag6 != 1, np.nan)
   data.min_dat6 = np.float32(np.nanmin(XX))
   data.max_dat6 = np.float32(np.nanmax(XX))
   
   XX = X7
   np.putmask(XX, data.flag7 != 1, np.nan)
   data.min_dat7 = np.float32(np.nanmin(XX))
   data.max_dat7 = np.float32(np.nanmax(XX))
   
   data.RH = np.float32(X1)
   data.TT = np.float32(X2) + 273.15
   data.IR = np.float32(X3)
   data.NetIR = np.float32(X4)
   data.WS = np.float32(X5)
   data.WD = np.float32(X6)
   data.PP = np.float32(X7)
   
   return data      

def uea_caps_1(fn_in, data, logfile):
   import pandas as pd
   import numpy as np
   import time
   from datetime import datetime
   import calendar   
   
   try:
      df = pd.read_csv(fn_in)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn_in, ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn_in + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   
   X = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag = np.array(df.loc[:, header[2]:header[2]:1].values)
   
   data.mole_frac = np.array([])
   data.mass_frac = np.array([])
   data.mole_conc = np.array([])
   data.mass_conc = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X <= 0)
   data.flag[ii] = 2
   ii = np.where(X > 9000)
   data.flag[ii] = 3
   
   #valid max and min values
   XX = X
   np.putmask(XX, data.flag != 1, np.nan)
   data.min_dat = np.float32(np.nanmin(XX))
   data.max_dat = np.float32(np.nanmax(XX))
   
   if 'mol-1' in header[1]:
      data.mole_frac = X
      if 'mmol' in header[1]:
         data.unit = '1e-3'
         data.practical_units = 'mmol mol-1'
      if 'micro' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'micro mol mol-1'   
      if 'nmol' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'nmol-1'
      if 'mpol' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'pmol mol-1'         
   if 'pp' in header[1]:
      data.mass_frac = X
      if 'ppm' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'ppm'
      if 'ppb' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'ppb'
      if 'ppt' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'ppt'
   if 'mol m-3' in header[1]: 
      data.mole_conc = X  
      data.unit = 'mol m-3'
   if 'kg m-3' in header[1]:
      data.mass_conc = X
      data.unit = 'kg m-3'
   
   return data 
         
def uea_fidas200E_1(fn_in, data, logfile):
   import pandas as pd
   import numpy as np
   import time
   from datetime import datetime
   import calendar   
   
   try:
      df = pd.read_csv(fn_in)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn_in, ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn_in + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   df[header[3]].fillna(-1.00e+20, inplace = True) 
   df[header[5]].fillna(-1.00e+20, inplace = True) 
   df[header[7]].fillna(-1.00e+20, inplace = True) 
   df[header[9]].fillna(-1.00e+20, inplace = True) 
   df[header[11]].fillna(-1.00e+20, inplace = True) 
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   X2 = np.array(df.loc[:, header[3]:header[3]:1].values)
   data.flag2 = np.array(df.loc[:, header[4]:header[4]:1].values)
   X3 = np.array(df.loc[:, header[5]:header[5]:1].values)
   data.flag3 = np.array(df.loc[:, header[6]:header[6]:1].values)
   X4 = np.array(df.loc[:, header[7]:header[7]:1].values)
   data.flag4 = np.array(df.loc[:, header[8]:header[8]:1].values)
   X5 = np.array(df.loc[:, header[9]:header[9]:1].values)
   data.flag5 = np.array(df.loc[:, header[10]:header[10]:1].values)
   X6 = np.array(df.loc[:, header[11]:header[11]:1].values)
   data.flag6 = np.array(df.loc[:, header[12]:header[12]:1].values)
   
   data.pm1 = np.array([])
   data.pm25 = np.array([])
   data.pm4 = np.array([])
   data.pm10 = np.array([])
   data.pc = np.array([])
   data.tcp = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   
   ii = np.where(X2 <= 0)
   data.flag2[ii] = 2
   ii = np.where(X2 > 9000)
   data.flag2[ii] = 3
   
   ii = np.where(X3 <= 0)
   data.flag3[ii] = 2
   ii = np.where(X3 > 9000)
   data.flag3[ii] = 3
   
   ii = np.where(X4 <= 0)
   data.flag4[ii] = 2
   ii = np.where(X4 > 9000)
   data.flag4[ii] = 3
   
   ii = np.where(X5 <= 0)
   data.flag5[ii] = 2
   ii = np.where(X5 > 9000)
   data.flag5[ii] = 3
   
   ii = np.where(X6 <= 0)
   data.flag6[ii] = 2
   ii = np.where(X6 > 9000)
   data.flag6[ii] = 3
   
   #valid max and min values
   XX = X1
   np.putmask(XX, data.flag1 != 1, np.nan)
   data.min_dat1 = np.float32(np.nanmin(XX))
   data.max_dat1 = np.float32(np.nanmax(XX))
   
   XX = X2
   np.putmask(XX, data.flag2 != 1, np.nan)
   data.min_dat2 = np.float32(np.nanmin(XX))
   data.max_dat2 = np.float32(np.nanmax(XX))
   
   XX = X3
   np.putmask(XX, data.flag3 != 1, np.nan)
   data.min_dat3 = np.float32(np.nanmin(XX))
   data.max_dat3 = np.float32(np.nanmax(XX))
   
   XX = X4
   np.putmask(XX, data.flag4 != 1, np.nan)
   data.min_dat4 = np.float32(np.nanmin(XX))
   data.max_dat4 = np.float32(np.nanmax(XX))
   
   XX = X5
   np.putmask(XX, data.flag5 != 1, np.nan)
   data.min_dat5 = np.float32(np.nanmin(XX))
   data.max_dat5 = np.float32(np.nanmax(XX))
   
   XX = X6
   np.putmask(XX, data.flag6 != 1, np.nan)
   data.min_dat6 = np.float32(np.nanmin(XX))
   data.max_dat6 = np.float32(np.nanmax(XX))
   
   data.pm1 = X1
   data.pm25 = X2
   data.pm4 = X3
   data.pm10 = X4
   data.pc = X5
   data.tcp = X6
   
   return data
          
def uea_radon_1(fn_in, data, logfile):
   import pandas as pd
   import numpy as np
   import time
   from datetime import datetime
   import calendar   
   
   try:
      df = pd.read_csv(fn_in)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn_in, ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn_in + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   
   X = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag = np.array(df.loc[:, header[2]:header[2]:1].values)
   
   data.mole_frac = np.array([])
   data.mass_frac = np.array([])
   data.mole_conc = np.array([])
   data.mass_conc = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X <= 0)
   data.flag[ii] = 2
   ii = np.where(X > 9000)
   data.flag[ii] = 3
   
   #valid max and min values
   XX = X
   np.putmask(XX, data.flag != 1, np.nan)
   data.min_dat = np.float32(np.nanmin(XX))
   data.max_dat = np.float32(np.nanmax(XX))
   
   if 'mol-1' in header[1]:
      data.mole_frac = X
      if 'mmol' in header[1]:
         data.unit = '1e-3'
         data.practical_units = 'mmol mol-1'
      if 'micro' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'micro mol mol-1'   
      if 'nmol' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'nmol-1'
      if 'mpol' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'pmol mol-1'         
   if 'pp' in header[1]:
      data.mass_frac = X
      if 'ppm' in header[1]:
         data.unit = '1e-6'
         data.practical_units = 'ppm'
      if 'ppb' in header[1]:
         data.unit = '1e-9'
         data.practical_units = 'ppb'
      if 'ppt' in header[1]:
         data.unit = '1e-12'
         data.practical_units = 'ppt'
   if 'mol m-3' in header[1]: 
      data.mole_conc = X  
      data.unit = 'mol m-3'
   if 'kg m-3' in header[1]:
      data.mass_conc = X
      data.unit = 'kg m-3'
   
   return data 
         
def uea_sodar_rass_1(fn_in, data, logfile):
   import numpy as np
   import WAO_sodar as WAOC

   #parse the data  
   data = WAOC.sodar_parse(fn_in, data)      
   
   return data
 