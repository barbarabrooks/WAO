def nox_create_NC_file_v2(dout, DT):
   from netCDF4 import Dataset
   
   f1 = 'ncas-42i-nox-2' #instrument name
   f2 = 'wao' #platform name
   mm = str(int(DT[0,1]))
   if len(mm)<2:
      mm = "0" + mm
   dd = str(int(DT[0,2]))
   if len(dd)<2:
      dd = "0" + dd   
   f3 = str(int(DT[0,0])) + mm + dd #date yyyymmdd
   f4 = 'nox-noxy-concentration' #data product
   f5 = "v1" #version number
   f6 = ".nc"
   fn = dout + f1 + chr(95) + f2 + chr(95) + f3 + chr(95) + f4 + chr(95) + f5 + f6

   fn_nc = Dataset(fn, "w",  format = "NETCDF4_CLASSIC") 
   
   return fn_nc
   
def nox_NC_Global_Attributes_v2(fn_nc, meta, ET):
   from datetime import datetime
   import numpy as np
   
   name = meta.loc[:, 'Name':'Name':1].values
   exp = meta.loc[:, 'Example':'Example':1].values
   pos = exp[34]
   pos = pos[0]
   ix1 = pos.find('N')
   ix2 = pos.find(',')
   ix3 = pos.find('E')
   
   lat = np.float32(pos[0:ix1])
   lon = np.float32(pos[ix2+1:ix3])
   
   for i in range(0,len(name)):
      msg1 = np.array(name[i])
      msg2 = np.array(exp[i])
      fn_nc.setncattr(msg1[0], msg2[0])
   
   fn_nc.last_revised_date = datetime.utcnow().isoformat()  
   fn_nc.time_coverage_start = datetime.utcfromtimestamp(ET[0]).isoformat()
   fn_nc.time_coverage_end = datetime.utcfromtimestamp(ET[len(ET)-1]).isoformat()
   
   return lat, lon
   
def nox_NC_Dimensions_v2(fn_nc, ET):
   time = fn_nc.createDimension('time', len(ET) )
   latitude = fn_nc.createDimension('latitude', 1)
   longitude = fn_nc.createDimension('longitude', 1) 
   
def nox_NC_VaraiblesAndData_v2(fn_nc, data, np, lat, lon):
   #time
   times = fn_nc.createVariable('time', np.float64, ('time',))
   #variable attributes
   times.type = 'float64'
   times.units = 'seconds since 1970-01-01 00:00:00'
   times.standard_name = 'time'
   times.long_name = 'Time (seconds since 1970-01-01 00:00:00)'
   times.axis = 'T'
   times.valid_min = np.float64(min(data.ET))
   times.valid_max = np.float64(max(data.ET))
   times.calendar = 'standard'
   #write data
   times[:] = np.float64(data.ET)
   
   #lat
   latitudes = fn_nc.createVariable('latitude', np.float32, ('latitude',))
   #variable attributes
   latitudes.type = 'float32'
   latitudes.units = 'degrees_north'
   latitudes.standard_name = 'latitude'
   latitudes.long_name = 'Latitude'
   #write data
   latitudes[:] = np.float32(lat)
   
   #lon
   longitudes = fn_nc.createVariable('longitude', np.float32, ('longitude',))
   #variable attributes
   longitudes.type = 'float32'
   longitudes.units = 'degrees_east'
   longitudes.standard_name = 'longitude'
   longitudes.long_name = 'Longitude'
   #write data
   longitudes[:] = np.float32(lon)
   
   #doy
   doys = fn_nc.createVariable('day_of_year', np.float32, ('time',))
   #variable attributes
   doys.type = 'float32'
   doys.units = '1'
   doys.long_name = 'Day of Year'
   doys.valid_min = np.float32(min(data.DoY))
   doys.valid_max = np.float32(max(data.DoY))
   #write data
   doys[:] = np.float32(data.DoY)
   
   #year
   years = fn_nc.createVariable('year', np.int32, ('time',))
   #variable attributes
   years.type = 'int32'
   years.units = '1'
   years.long_name = 'Year'
   years.valid_min = np.int32(min(data.DT[:,0]))
   years.valid_max = np.int32(max(data.DT[:,0])) 
   #write data
   years[:] = np.int32(data.DT[:,0])
   
   #month
   months = fn_nc.createVariable('month', np.int32, ('time',))
   #variable attributes
   months.type = 'int32'
   months.units = '1'
   months.long_name = 'Month'
   months.valid_min = np.int32(min(data.DT[:,1]))
   months.valid_max = np.int32(max(data.DT[:,1])) 
   #write data
   months[:] = np.int32(data.DT[:,1])
   
   #day
   days = fn_nc.createVariable('day', np.int32, ('time',))
   #variable attributes
   days.type = 'int32'
   days.units = '1'
   days.long_name = 'Day'
   days.valid_min = np.int32(min(data.DT[:,2]))
   days.valid_max = np.int32(max(data.DT[:,2]))
   #write data
   days[:] = np.int32(data.DT[:,2])
   
   #hour
   hours = fn_nc.createVariable('hour', np.int32, ('time',))
   #variable attributes
   hours.type = 'int32'
   hours.units = '1'
   hours.long_name = 'Hour'
   hours.valid_min = np.int32(min(data.DT[:,3]))
   hours.valid_max = np.int32(max(data.DT[:,3])) 
   #write data
   hours[:] = np.int32(data.DT[:,3])
   
   #minute
   minutes = fn_nc.createVariable('minute', np.int32, ('time',))
   #variable attributes
   minutes.type = 'int32'
   minutes.units = '1'
   minutes.long_name = 'Minute'
   minutes.valid_min = np.int32(min(data.DT[:,4]))
   minutes.valid_max = np.int32(max(data.DT[:,4]))  
   #write data
   minutes[:] = np.int32(data.DT[:,4])
   
   #second
   seconds = fn_nc.createVariable('second', np.float32, ('time',))
   #variable attributes
   seconds.type = 'float32'
   seconds.units = '1'
   seconds.long_name = 'Second'
   seconds.valid_min = np.float32(min(data.DT[:,5]))
   seconds.valid_max = np.float32(max(data.DT[:,5])) 
   #write data
   seconds[:] = np.float32(data.DT[:,5])
   
   #NO conc
   NO = fn_nc.createVariable('mole_fraction_of_nitric_oxide_in_air', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   NO.type = 'float32'
   NO.units = '1e-9'
   NO.practical_units = 'ppb'
   NO.long_name = 'Mole Fraction of Nitric Oxide in air'
   XX = data.no
   np.putmask(XX, data.flag_no != 1, np.nan)
   NO.valid_min = np.float32(np.nanmin(XX))
   NO.valid_max = np.float32(np.nanmax(XX))
   NO.cell_methods = 'time: point'
   NO.coordinates = 'latitude longitude'
   NO.chemical_species = 'NO'
   #write data
   NO[:] = np.float32(data.no)
   
   #Qc flag NO
   qc_flags_no = fn_nc.createVariable('qc_flag_no', np.int8, ('time',))
   #variable attribute
   qc_flags_no.type = 'byte'
   qc_flags_no.units = '1'
   qc_flags_no.long_name = 'Data Quality Flag: NO'
   qc_flags_no.flag_values = '0b,1b,2b'
   qc_flags_no.flag_meanings = 'not_used' + '\n'
   qc_flags_no.flag_meanings = qc_flags_no.flag_meanings + 'good_data' + '\n'
   qc_flags_no.flag_meanings = qc_flags_no.flag_meanings + 'bad_data_do_not_use' 
   #write data
   qc_flags_no[:] = np.int8(data.flag_no)
   
   #NO2 conc
   NO2 = fn_nc.createVariable('mole_fraction_of_nitrogen_dioxide_in_air', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   NO2.type = 'float32'
   NO2.units = '1e-9'
   NO2.practical_units = 'ppb'
   NO2.standard_name = 'mole_fraction_of_nitrogen_dioxide_in_air'
   NO2.long_name = 'Mole Fraction of Nitrogen Dioxide in air'
   XX = data.no2
   np.putmask(XX, data.flag_no2 != 1, np.nan)
   NO2.valid_min = np.float32(np.nanmin(XX))
   NO2.valid_max = np.float32(np.nanmax(XX))
   NO2.cell_methods = 'time: point'
   NO2.coordinates = 'latitude longitude'
   NO2.chemical_species = 'NO2'
   #write data
   NO2[:] = np.float32(data.no2)
   
   #Qc flag NO2
   qc_flags_no2 = fn_nc.createVariable('qc_flag_no2', np.int8, ('time',))
   #variable attribute
   qc_flags_no2.type = 'byte'
   qc_flags_no2.units = '1'
   qc_flags_no2.long_name = 'Data Quality Flag: NO2'
   qc_flags_no2.flag_values = '0b,1b,2b'
   qc_flags_no2.flag_meanings = 'not_used' + '\n'
   qc_flags_no2.flag_meanings = qc_flags_no2.flag_meanings + 'good_data' + '\n'
   qc_flags_no2.flag_meanings = qc_flags_no2.flag_meanings + 'bad_data_do_not_use' 
   #write data
   qc_flags_no2[:] = np.int8(data.flag_no2)
   
   #NOx conc
   NOx = fn_nc.createVariable('mole_fraction_of_nox_expresssed_as_nitrogen_in_air', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   NOx.type = 'float32'
   NOx.units = '1e-9'
   NOx.practical_units = 'ppb'
   NOx.standard_name = 'mole_fraction_of_nox_expresssed_as_nitrogen_in_air'
   NOx.long_name = 'Mole Fraction of NOx expresssed as nitrogen in air'
   XX = data.nox
   np.putmask(XX, data.flag_nox != 1, np.nan)
   NOx.valid_min = np.float32(np.nanmin(XX))
   NOx.valid_max = np.float32(np.nanmax(XX))
   NOx.cell_methods = 'time: point'
   NOx.coordinates = 'latitude longitude'
   NOx.chemical_species = 'NOx'
   #write data
   NOx[:] = np.float32(data.nox)
   
   #Qc flag NOx
   qc_flags_nox = fn_nc.createVariable('qc_flag_nox', np.int8, ('time',))
   #variable attribute
   qc_flags_nox.type = 'byte'
   qc_flags_nox.units = '1'
   qc_flags_nox.long_name = 'Data Quality Flag: NOx'
   qc_flags_nox.flag_values = '0b,1b,2b'
   qc_flags_nox.flag_meanings = 'not_used' + '\n'
   qc_flags_nox.flag_meanings = qc_flags_nox.flag_meanings + 'good_data' + '\n'
   qc_flags_nox.flag_meanings = qc_flags_nox.flag_meanings + 'bad_data_do_not_use' 
   #write data
   qc_flags_nox[:] = np.int8(data.flag_nox)
   
def NC_nox_v2(pd, np, dout, meta, data):
   fn_nc = nox_create_NC_file_v2(dout, data.DT)
   
   lat, lon = nox_NC_Global_Attributes_v2(fn_nc, meta, data.ET)
   nox_NC_Dimensions_v2(fn_nc, data.ET)
   nox_NC_VaraiblesAndData_v2(fn_nc, data, np, lat, lon)

   fn_nc.close()