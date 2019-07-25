'''hfshdfjhsaD
SJDFKSJDF
KSDJFKLSd
]SDJFKKSDF'''
def wao_o2_get_file_v1(fn, np):
   import csv
   from time import mktime, strptime
    
   DT = []
   ET = []
   DoY = []
   O2N2 = []
   flag = []
   
   ifile = open(fn)
   reader = csv.reader(ifile, delimiter = chr(44)) #9 = tab, 44 = ,
   for row in reader:
      xx = str(row[0])
      ix = xx.find("Date_Time")
      if ix < 0:
         xx = str(row[0])
         tt = strptime(str(row[0]), '%d/%m/%Y %H:%M')
         #DoY
         DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
         #ET
         ET.append(int(mktime(tt)))
         #DT
         DT.append(tt[0:6])
         #o2/n2 ratio
         xx = str(row[1])
         O2N2.append(float(xx))
         #fl
         xx = str(row[2])
         flag.append(int(xx))
		 
   return np.array(DT), np.array(DoY), np.array(ET), np.array(O2N2), np.array(flag) 
   
def wao_o2_parse_data_v1(data):
   ix = len(data.DoY)
   for ii in range(0,len(data.DoY)):
      if data.DT[ii,1] != data.DT[0,1]:
         ix = ii
		 
   return data.DT[0:ix,:], data.DoY[0:ix], data.ET[0:ix], data.O2N2[0:ix], data.flag[0:ix]