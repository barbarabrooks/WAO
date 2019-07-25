def get_file_v1(fn, lines):
    ll=[]
    f = open(fn, 'r') 
    ll = f.readlines()
    f.close()
    for i in ll:
        lines.append(i)
    
    return lines
   
def parse_block_v1(lines):
    start_of_block = []
    for i in range(len(lines)):
        a = lines[i]
        if a.count('CT') == 1:
            start_of_block.append(i)
    
    return start_of_block
 
"""ashdfjhdgfhas;gh;as
asjdfksfj
kasfkasgfjaskj"""
def parse_time_v1(lines, start_of_block, np, data):
    import time
    from datetime import datetime
    import calendar
    DT = []
    DoY = []
    ET = []
    for i in range(len(start_of_block)-1):
        a = lines[start_of_block[i]]
        b = a[0:a.index('C')-1]   
        t = []
        t.append(int(b[0:4]))
        t.append(int(b[5:7]))
        t.append(int(b[8:10]))
        t.append(int(b[11:13]))
        t.append(int(b[14:16]))
        t.append(float(b[17:len(b)]))
       
        c = time.strptime(b[0:len(b)],'%Y-%m-%dT%H:%M:%S.%f')
      
        DT.append(t)
        DoY.append(float(c.tm_yday)+(float(t[3])+float(t[4]/(60))+float(t[5]/(60*60)))/24)
        ET.append(calendar.timegm(c))
       
    data.DT = np.array(DT)
    data.DoY = np.array(DoY)
    data.ET = np.array(ET)
       
    return data
  
def parse_line1_v1(lines, start_of_block, np, data):
    unit = []
    swl = []
    ms = []
    for i in range(len(start_of_block)-1):
        a = lines[start_of_block[i]]
        b = a[a.index('C'):len(a)-1] 
        unit.append(b[2])  #unit_no
        swl.append(b[3:5]) #software level
        ms.append(b[5])    #message
    
    data.UN = np.array(unit)
    data.SWL = np.array(swl)
    data.MS = np.array(ms)
    
    return data
   
def parse_line2_v1(lines, start_of_block, np, data):
    dets = []
    wrn = []
    cbh1 = []
    cbh2 = []
    cbh3 = []
    cflag = []
    for i in range(len(start_of_block)-1):
        a = lines[start_of_block[i]+1]
        b = a[a.index(' ')+1:len(a)-1]
        #dets.append(int(str(b[0])))#detection status
        #wrn.append(int(str(b[1]))) #warnings
        dets.append(b[0])#detection status
        wrn.append(b[1]) #warnings
        cbh1.append(b[3:8])        #cloudbase height 1
        cbh2.append(b[9:14])       #cloudbase height 2
        cbh3.append(b[15:20])      #cloudbase height 3
        cflag.append(b[21:len(b)]) #flag 
    
    data.DETS = np.array(dets)
    data.WRN = np.array(wrn)
    data.CBH1 = np.array(cbh1)
    data.CBH2 = np.array(cbh2)
    data.CBH3 = np.array(cbh3)
    data.CFLAG = np.array(cflag)
    
    return data 

def parse_line3_v1(lines, start_of_block, np, data):
    sc = []
    mm = []
    lpe = []
    lt = []
    rs = []
    wc = []
    ta = []
    bl = []
    mp = []
    ss = []
    for i in range(len(start_of_block)-1):
        a = lines[start_of_block[i]+2]
        b = a[a.index(' ')+1:len(a)-1]
        sc.append(b[0:3])       #scale
        mm.append(b[4])         #measurement mode
        lpe.append(b[6:9])      #laser pulse energy
        lt.append(b[10:13])     #laser temperature
        rs.append(b[14:17])     #receiver sensitivity
        wc.append(b[19:22])     #window contamination
        ta.append(b[24:27])     #tilt angle
        bl.append(b[28:31])     #background light
        mp.append(b[32:38])     #measurement parameters
        ss.append(b[39:len(b)]) #sum 
    
    data.SC = np.array(sc)
    data.MM = np.array(mm)
    data.LPE = np.array(lpe)
    data.LT = np.array(lt)
    data.RS = np.array(rs)
    data.WC = np.array(wc)
    data.TA = np.array(ta)
    data.BL = np.array(bl)
    data.MP = np.array(mp)
    data.SS = np.array(ss)
        
    return data 

def parse_BB_v1(lines, start_of_block, np, data):
    alt = []
    line4 = []
    for i in range(len(start_of_block)-1):
        z = []
        bb = []
        for ii in range(16): #16 line of data
            a = lines[start_of_block[i]+3+ii]
            b = a[a.index(' ')+1:len(a)-1]
            z1 = int(b[0:3])*100#start of line height
            c = b[3:len(b)]
            for cc in range(16): #16 range gates per line
                z.append((z1+(cc*100))*0.3048) #profile height
                temp = int(c[cc*4:((cc*4)+4)],16)#(1000.sr.km)-1
                bb.append(float(temp/1e6)) #sr-1 m-1
         
        line4.append(bb)
        alt.append(z)
        
    data.ZZ = np.array(alt)
    data.BB = np.array(line4)    
    
    return data