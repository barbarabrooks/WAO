def wao_co2_get_file_v1(fn, np):
   import csv
   
   DT = []
   ET = []
   DoY = []
   CO2 = []
   flag = []
   
   ifile = open(fn)
   reader = csv.reader(ifile, delimiter = chr(9))
   
   for row in reader:
      t = []
      xx = str(row[0])
      ix = xx.find("decimal_day")
      if ix < 0:
         #year
         xx = str(row[3])
         t.append(int(xx))
         #month
         xx = str(row[2])
         t.append(int(xx))
         #day 
         xx = str(row[1])
         t.append(int(xx))
         #hour
         xx = str(row[4])
         t.append(int(xx))
         #minute
         xx = str(row[5])
         t.append(int(xx))
         #second
         xx = str(row[6])
         t.append(float(xx))
         #DT
         DT.append(t)
         #doy
         xx = str(row[0])
         DoY.append(float(xx))
         #et
         xx = str(row[9])
         ET.append(float(xx))
         #co2
         xx = str(row[10]) 
         CO2.append(float(xx))
         #fl
         xx = str(row[11])
         flag.append(int(xx))

   return np.array(DT), np.array(DoY), np.array(ET), np.array(CO2), np.array(flag) 
   
def wao_co2_parse_data_v1(data):
   for ii in range(1,len(data.DoY)):
      if data.DT[ii,1] == data.DT[0,1]:
         ix = ii
   
   return data.DT[0:ix,:], data.DoY[0:ix], data.ET[0:ix], data.CO2[0:ix], data.flag[0:ix]