def QC_BB_v1(data, np):
    data.BB_flag = np.ones(data.BB.shape)
   
    ii_0 = np.where(data.BB == 0)
    data.BB_flag[ii_0] = 2
    ii_min = np.where(data.BB <= 1e-7)
    data.BB_flag[ii_min] = 2
    ii_max = np.where(data.BB >= 10)
    data.BB_flag[ii_max] = 2
   
    return data
   
def QC_BB_noise_v1(data):
    dur, gates = data.BB_flag.shape
    #for each gate
    for i in range(gates-1):
        for ii in range(2,dur-3):
            if ((data.BB_flag[ii-2,i]) and (data.BB_flag[ii,i] == 1) and (data.BB_flag[ii+2,i] != 1)):
                data.BB_flag[ii,i] = 2
        for ii in range(2,dur-2):
            if ((data.BB_flag[ii-1,i]) and (data.BB_flag[ii,i] == 1) and (data.BB_flag[ii+1,i] != 1)):
                data.BB_flag[ii,i] = 2
   
    #for each time
    for i in range(dur-1):
        for ii in range(2,gates-3):
            if ((data.BB_flag[i,ii-2]) and (data.BB_flag[i,ii] == 1) and (data.BB_flag[i,ii+2] != 1)):
                data.BB_flag[i,ii] = 2
        for ii in range(2,gates-2):
            if ((data.BB_flag[i,ii-1]) and (data.BB_flag[i,ii] == 1) and (data.BB_flag[i,ii+1] != 1)):
                data.BB_flag[i,ii] = 2
                
    return data
   
def QC_CBH_v1(data, np):
    # AMF flags: 
    #1 - good data, 2 - no sig backscatter, 3 - full obfurscation no cloud base
    #4 - some obfurscation - transparent, 5 - time stamp
   
    # vaisala flags:
    #0 - no sig backscatter, 1 - one cb, 2 - two cbs, 3 - 3 cbs,
    #4 - full obfurscation no cloud base, 5 - some obfurscation - transparent
    #/ - Raw data input to algorithm missing or suspect
    
    #get rid of '/////'
    for n in range(len(data.ET)):
        if data.CBH1[n].find('/') > -1:
            data.CBH1[n] = np.nan
        else:
            data.CBH1[n] = int(data.CBH1[n])    
    
    for n in range(len(data.ET)):
        if data.CBH2[n].find('/') > -1:
            data.CBH2[n] = np.nan
        else:
            data.CBH2[n] = int(data.CBH2[n]) 
        
    for n in range(len(data.ET)):
        if data.CBH3[n].find('/') > -1:
            data.CBH3[n] = np.nan
        else:
            data.CBH3[n] = int(data.CBH3[n])  
    
    data.CBH_flag = np.ones(data.CBH1.shape)
    
    ii_0 = np.where(data.DETS == 0)
    data.CBH_flag[ii_0] = 2
    data.CBH1[ii_0] = np.nan
    data.CBH2[ii_0] = np.nan
    data.CBH3[ii_0] = np.nan
    
    ii_0 = np.where(data.DETS == 1)
    data.CBH2[ii_0] = np.nan
    data.CBH3[ii_0] = np.nan
    
    ii_0 = np.where(data.DETS == 2)
    data.CBH3[ii_0] = np.nan

    ii_0 = np.where(data.DETS == 4)
    data.CBH_flag[ii_0] = 3
    data.CBH1[ii_0] = np.nan
    data.CBH2[ii_0] = np.nan
    data.CBH3[ii_0] = np.nan
    
    ii_0 = np.where(data.DETS == 5)
    data.CBH_flag[ii_0] = 4
    data.CBH1[ii_0] = np.nan
    data.CBH2[ii_0] = np.nan
    data.CBH3[ii_0] = np.nan
     
    return data
   
def tidy_data_v1(data, data_out, np):
    s = (len(data.ET),3)
    data_out.CBH = np.ones(s)
    data_out.DT = data.DT
    data_out.ET = data.ET
    data_out.DoY = data.DoY
    data_out.BB = data.BB
    data_out.ZZ = data.ZZ
    data_out.BB_FLAG = data.BB_flag
    for n in range(len(data.ET)):
        data_out.CBH[n,0] = (float(data.CBH1[n]))*0.3048
        data_out.CBH[n,1] = (float(data.CBH2[n]))*0.3048
        data_out.CBH[n,2] = (float(data.CBH3[n]))*0.3048
        
    data_out.CBH_FLAG = data.CBH_flag
    
    return data_out