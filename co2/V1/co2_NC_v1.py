def wao_co2_get_meta_v1(fn):
   import csv
   meta = []
   
   str3 = "platform_location"
   str4 = "platform_height"
   
   ifile = open(fn)
   reader = csv.reader(ifile, delimiter = chr(9))

   for row in reader:
      if len(row) > 0:  
         xx = str(row[0])
         yy = str(row[1])
         meta.append(yy)

         #extract loaction
         ix3 = xx.find(str3)
         if ix3 > -1:
            xxx = yy
            ix31 = xxx.find(" (")
            ix32 = xxx.find(") ")
            lat = float(xxx[ix31+2:ix32])
            yyy = xxx[ix32+1:len(xxx)]
            ix41 = yyy.find("(")
            lon = float(yyy[ix41+1:len(yyy)-1])
         #extract platform height
         ix4 = xx.find(str4)
         if ix4 > -1:
            ix5 = yy.find("m")
            if ix5 > -1:
               plat_Z = float(yy[0:ix5])
            if ix5 < 0:
               plat_Z = float(yy)
      
   ifile.close()
   meta.append(lat)
   meta.append(lon)
   meta.append(plat_Z)
   
   return meta
   
def wao_co2_create_NC_file_v1(meta, dout, DT):
   from netCDF4 import Dataset
   
   f1 = meta[0] #instrument name
   f2 = meta[29] #platform name
   mm = str(int(DT[0,1]))
   if len(mm)<2:
      mm = "0" + mm
   f3 = str(int(DT[0,0])) + mm #date
   f4 = meta[1] #data product
   f5 = "v" + meta[20] #version number
   f6 = ".nc"
   fn = dout + f1 + chr(95) + f2 + chr(95) + f3 + chr(95) + f4 + chr(95) + f5 + f6

   nc = Dataset(fn, "w",  format = "NETCDF4_CLASSIC") 
   
   return nc
   
def wao_co2_NC_Global_Attributes_v1(nc, meta, ET):
   from datetime import datetime
   import pytz
   
   nc.Conventions = meta[2]
   nc.source = meta[3]
   nc.instrument_manufacturer = meta[4]
   nc.instrument_model = meta[5]
   nc.serial_number = meta[6]
   nc.operational_software = meta[7]
   nc.operational_software_version = meta[8]
   nc.creator_name = meta[9]
   nc.creator_email = meta[10]
   nc.creator_url = meta[11]
   nc.institution = meta[12]
   nc.processing_software = meta[13]
   nc.processing_software_version = meta[14]
   nc.calibration_sensitivity = meta[15]
   nc.calibration_certification_date = meta[16]
   nc.calibration_certification_url = meta[17]
   nc.sampling_interval = meta[18]
   nc.averaging_interval = meta[19]
   nc.data_set_version = meta[20]
   nc.data_product_level = meta[21]
   nc.last_revised_date = datetime.now(pytz.utc).isoformat()
   nc.project = meta[23]
   nc.project_principle_investigator = meta[24]
   nc.project_principle_investigator_contact = meta[25]
   nc.licence = meta[26]
   nc.acknowledgement = meta[27]
   nc.platform_type = meta[28]
   nc.platform_name = meta[29]
   nc.title = meta[30]
   nc.feature_type = meta[31]
   nc.start_time = datetime.fromtimestamp(ET[0], pytz.UTC).isoformat()
   nc.end_time = datetime.fromtimestamp(ET[len(ET)-1], pytz.UTC).isoformat()
   nc.platform_location = meta[34]
   nc.platform_height = meta[35]
   nc.location_keywords = meta[36]
   nc.history = meta[37]
   nc.comment = meta[38]
   #flags
   nc.qc_flag_comment = meta[40]
   nc.qc_flag_value_0_description = meta[41]
   nc.qc_flag_value_1_description = meta[42]
   nc.qc_flag_value_1_assessment = meta[43]
   nc.qc_flag_value_2_description = meta[44]
   nc.qc_flag_value_2_assessment = meta[45]
   nc.qc_flag_value_3_description = meta[46]
   nc.qc_flag_value_3_assessment = meta[47]
   
def wao_co2_NC_Dimensions_v1(nc, ET):
   time = nc.createDimension('time', len(ET) )
   latitude = nc.createDimension('latitude', 1)
   longitude = nc.createDimension('longitude', 1) 
   
def wao_co2_NC_VaraiblesAndData_v1(nc, meta, data, np):
   #time
   times = nc.createVariable('time', np.double, ('time',))
   #time variable attributes
   times.dimension = 'time'
   times.type = 'double'
   times.units = 'seconds since 1970-01-01 00:00:00 UTC'
   times.standard_name = 'time'
   times.long_name = 'Time (seconds since 1970-01-01)'
   times.axis = 'T'
   times.valid_min = min(data.ET)
   times.valid_max = max(data.ET)
   times.calendar = 'julian'
   #write data
   times[:] = data.ET
   
   #lat
   latitudes = nc.createVariable('latitude', np.double, ('latitude',))
   #latitude variable attributes
   latitudes.dimension = 'latitude'
   latitudes.type = 'double'
   latitudes.units = 'degree_north'
   latitudes.standard_name = 'latitude'
   latitudes.long_name = 'Latitude'
   #write data
   latitudes[:] = float(meta[len(meta)-3])
   
   #lon
   longitudes = nc.createVariable('longitude', np.double, ('longitude',))
   #longitude variable attributes
   longitudes.dimension = 'longitude'
   longitudes.type = 'double'
   longitudes.units = 'degree_east'
   longitudes.standard_name = 'longitude'
   longitudes.long_name = 'Longitude'
   #write data
   longitudes = float(meta[len(meta)-2])
   
   #doy
   doys = nc.createVariable('day_of_year', np.double, ('time',))
   #day_of_year variable attributes
   doys.dimension = 'time'
   doys.type = 'double'
   doys.units = '1'
   doys.long_name = 'Day of Year'
   doys.valid_min = 1
   doys.valid_max = 366 
   #write data
   doys[:] = data.DoY
   
   #year
   years = nc.createVariable('year', np.int, ('time',))
   #year variable attributes
   years.dimension = 'time'
   years.type = 'int'
   years.units = '1'
   years.long_name = 'Year'
   years.valid_min = 1900
   years.valid_max = 2100 
   #write data
   years[:] = data.DT[:,0]
   
   #month
   months = nc.createVariable('month', np.int, ('time',))
   #month variable attributes
   months.dimension = 'time'
   months.type = 'int'
   months.units = '1'
   months.long_name = 'Month'
   months.valid_min = 1
   months.valid_max = 12 
   #write data
   months[:] = data.DT[:,1]
   
   #day
   days = nc.createVariable('day', np.int, ('time',))
   #day variable attributes
   days.dimension = 'time'
   days.type = 'int'
   days.units = '1'
   days.long_name = 'Day'
   days.valid_min = 1
   days.valid_max = 31 
   #write data
   days[:] = data.DT[:,2]
   
   #hour
   hours = nc.createVariable('hour', np.int, ('time',))
   #hour variable attributes
   hours.dimension = 'time'
   hours.type = 'int'
   hours.units = '1'
   hours.long_name = 'Hour'
   hours.valid_min = 0
   hours.valid_max = 23 
   #write data
   hours[:] = data.DT[:,3]
   
   #minute
   minutes = nc.createVariable('minute', np.int, ('time',))
   #minute variable attributes
   minutes.dimension = 'time'
   minutes.type = 'int'
   minutes.units = '1'
   minutes.long_name = 'Minute'
   minutes.valid_min = 0
   minutes.valid_max = 59 
   #write data
   minutes[:] = data.DT[:,4]
   
   #second
   seconds = nc.createVariable('second', np.double, ('time',))
   #second variable attributes
   seconds.dimension = 'time'
   seconds.type = 'double'
   seconds.units = '1'
   seconds.long_name = 'Second'
   seconds.valid_min = 0
   seconds.valid_max = 59.99999 
   #write data
   seconds[:] = data.DT[:,5]
   
   #co2 conc
   CO2 = nc.createVariable('co2_concentration_in_air', np.double, ('time',),fill_value=-1.00e+20)
   #bks variable attributes
   CO2.dimension = 'time'
   CO2.type = 'double'
   CO2.units = 'ppm'
   CO2.long_name = 'CO2 concentration in air'
   CO2.valid_min = 200
   CO2.valid_max = 800
   CO2.cell_methods = 'time:point'
   CO2.coordinates = 'latitude longitude'
   #write data
   CO2[:] = data.CO2
   
   #Qc falg
   qc_flags = nc.createVariable('qc_flag', np.int, ('time',))
   #qc_flag variable attribute
   qc_flags.dimension = 'time, altitude'
   qc_flags.type = 'int'
   qc_flags.units = '1'
   qc_flags.long_name = 'Data Quality Flag'
   qc_flags.valid_min = 1
   qc_flags.valid_max = 3
   #write data
   qc_flags[:] = data.flag
   
def NC_wao_co2_v1(meta, dout, data, np):
   nc = wao_co2_create_NC_file_v1(meta, dout, data.DT)
   
   wao_co2_NC_Global_Attributes_v1(nc, meta, data.ET)
   wao_co2_NC_Dimensions_v1(nc, data.ET)
   wao_co2_NC_VaraiblesAndData_v1(nc, meta, data, np)

   nc.close()