def read_meta(logfile, name):
   import pandas as pd
   import numpy as np
   from datetime import datetime
   
   # read in meta
   try:
      df = pd.read_excel("meta.xlsx")
   except:
      # exit if problem encountered
      print("Unable to open meta.xlsx. This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open meta.xlsx. Program will terminate.\n')
      g.close()
      exit()     
      
   # find the approprate line
   inst = df.loc[:, 'instrument\n':'instrument\n':1].values
   tp = df.columns
   header = np.array(tp[1:len(tp)])      
   for x in range (0, len(inst)):
      if (name in inst[x]):
         tp = df.loc[x,:].values  
         dd = np.array(tp[1:len(tp)])
         break
            
   meta = np.empty([len(header), 2], dtype=object)       
   if 'dd' not in locals():
      print("Can't find meta data about named instrument. This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Can\'t find meta data about named instrument. Program will terminate.\n')
      g.close()
      exit()
   else:
      for x in range (0, len(header)):
         meta[x, 0] = header[x]
         meta[x, 1] = dd[x]
   
   del pd, datetime, np    
   
   return meta

def read_config(logfile):
   from datetime import datetime
   import numpy as np
   
   # read in Config file
   try:
      f = open("Config.txt", "r")
      if f.mode == 'r':
         lines = f.readlines()
         f.close()
   except:
      # exit if problem encountered
      print("Unable to open Config.txt file. This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open Config.txt. Program will terminate.\n')
      g.close()
      exit()
   
   # process information in config file
   x_st = 0; x_ed = 0;
   ss1 = "Start - do not remove"
   for x in range (0, len(lines)):
      if (ss1 in lines[x]):
         try:
            ver = lines[x+1].strip('\n') 
            name = lines[x+2].strip('\n') 
            product = lines[x+3].strip('\n') 
            fn_in =  lines[x+4].strip('\n')        
            break  
         except:   
            print("An instrument product pair must be given. This program will terminate.")
            g = open(logfile, 'a')
            g.write(datetime.utcnow().isoformat() + ' Error in config file. Program will terminate.\n')
            g.close()
            exit()
      
   del lines, datetime, np
      
   return ver, fn_in, name, product
      
def read_data_file(dp, fn_in, data, logfile):
   import WAO_data as dat
   
   if dp == 'ncas-ceilometer-2':
      data = dat.ncas_ceilometer_2(fn_in, data, logfile)
         
   if dp == 'ncas-co2-1':
      data = dat.ncas_co2_1(fn_in, data, logfile)    
         
   if dp == 'ncas-ftir-1':
      data = dat.ncas_ftir_1(fn_in, data, logfile) 
         
   if dp == 'ncas-ghg-gc-fid-1':
      data = dat.ncas_ghg_gc_fid_1(fn_in, data, logfile) 

   if dp == 'ncas-ghg-gc-ecd-1':
      data = dat.ncas_ghg_gc_ecd_1(fn_in, data, logfile) 
         
   if dp == 'ncas-o2-1':
      data = dat.ncas_o2_1(fn_in, data, logfile) 

   if dp == 'ncas-rga3-1':
      data = dat.ncas_rga3_1(fn_in, data, logfile) 
        
   if dp == 'uea-42i-nox-1':
      data = dat.uea_42i_nox_1(fn_in, data, logfile)  
         
   if dp == 'uea-43i-so2-1':
      data = dat.uea_43i_so2_1(fn_in, data, logfile)
      
   if dp == 'uea-49i-o3-1':
      data = dat.uea_49i_o3_1(fn_in, data, logfile)
         
   if dp == 'uea-aws-1':
      data = dat.uea_aws_1and2(fn_in, data, logfile)
         
   if dp == 'uea-aws-2':
      data = dat.uea_aws_1and2(fn_in, data, logfile)

   if dp == 'uea-caps-1':
      data = dat.uea_caps_1(fn_in, data, logfile)
         
   if dp == 'uea-fidas200E-1':
      data = dat.uea_fidas200E_1(fn_in, data, logfile)
          
   if dp == 'uea-radon-1':
      data = dat.uea_radon_1(fn_in, data, logfile)
         
   if dp == 'uea-sodar-rass-1':
      data = dat.uea_sodar_rass_1(fn_in, data, logfile)
      
   del dat
   
   return data

def do_run(name, product, ver, meta, data, logfile):
   import WAO_products as prod
      
   start_date = ''
   # set default file naming options
   opt1 = ''; opt2 = ''; opt3 = ''
      
   # create, write and close the files
   # A
   if product == 'acoustic-backscatter-winds':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.acoustic_backscatter_winds(meta, data, nc, ver)
      nc.close()
         
   if product == 'aerosol-backscatter':
      # set up all naming options
      opt1 = 'standard' #need option for advanced
      
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.aerosol_backscatter(meta, data, nc, ver)
      nc.close()     
         
   # C
   if product == 'ch4-concentration':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.ch4_concentration(meta, data, nc, ver)
      nc.close()
         
   if product == 'ch4-n2o-co2-co-concentration':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.ch4_n2o_co2_co_concentration(meta, data, nc, ver)
      nc.close()  

   if product == 'cloud-base':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.cloud_base(meta, data, nc, ver)
      nc.close()
         
   if product == 'cloud-coverage':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.cloud_coverage(meta, data, nc, ver)
      nc.close()

   if product == 'co-h2-concentration':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.co_h2_concentration(meta, data, nc, ver)
      nc.close()  
        
   if product == 'co2-concentration':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.co2_concentration(meta, data, nc, ver)
      nc.close()  
         
   # H
   if product == 'h2-concentration':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.h2_concentration(meta, data, nc, ver)
      nc.close()  
      
   # N 
   if product == 'n2o-sf6-concentration':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.n2o_sf6_concentration(meta, data, nc, ver)
      nc.close() 
         
   if product == 'no2-concentration':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.no2_concentration(meta, data, nc, ver)
      nc.close() 
         
   if product == 'nox-noxy-concentration':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.nox_noxy_concentration(meta, data, nc, ver)
      nc.close() 

   # O
   if product == 'o2n2-concentration-ratio':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.o2n2_concentration_ratio(meta, data, nc, ver)
      nc.close() 
         
   if product == 'o3-concentration':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.o3_concentration(meta, data, nc, ver)
      nc.close() 
        
   # P   
   if product == 'pm-concentration':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.pm_concentration(meta, data, nc, ver)
      nc.close() 
         
   # R
   if product == 'radon-concentration':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.radon_concentration(meta, data, nc, ver)
      nc.close() 

   # S
   if product == 'sf6-concentration':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.sf6_concentration(meta, data, nc, ver)
      nc.close()        
         
   if product == 'so2-concentration':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.so2_concentration(meta, data, nc, ver)
      nc.close()       
       
   if product == 'surface-met':
      if name == 'uea-aws-1':
         # set up all naming options
         opt1 = '10m'; opt2 = ''; opt3 = ''
         
         # create nc file - campbell - radiation - aws1
         nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
         prod.surface_met1(meta, data, nc, ver)
         nc.close()
         
      if name == 'uea-aws-2':
         # set up all naming options
         opt1 = '10m'; opt2 = ''; opt3 = ''
   
         # create nc file - gill metpak - aws2
         nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
         prod.surface_met2(meta, data, nc, ver)
         nc.close() 
         
   del prod

def t_control(logfile): 
   from collections import namedtuple  
   
   # read in and process config file   
   [ver, fn_in, name, product] = read_config(logfile)
   
   # read in meta file
   meta = read_meta(logfile, name)
   
   #read in data
   data = namedtuple("data", "") 
   data.lat = 52.9506
   data.lon = 1.1219
   data = read_data_file(name, fn_in, data, logfile)
   
   # run through run list for each deployment mode
   do_run(name, product, ver, meta, data, logfile)
   