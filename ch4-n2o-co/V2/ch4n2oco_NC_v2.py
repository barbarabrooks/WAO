def ch4n2oco_create_NC_file_v2(dout, DT):
   from netCDF4 import Dataset
   
   f1 = 'ncas-ftir-1' #instrument name
   f2 = 'wao' #platform name
   mm = str(int(DT[0,1]))
   if len(mm)<2:
      mm = "0" + mm
   dd = str(int(DT[0,2]))
   if len(dd)<2:
      dd = "0" + dd   
   f3 = str(int(DT[0,0])) + mm + dd #date yyyymmdd
   f4 = 'ch4-n2o-co-concentration' #data product
   f5 = "v1" #version number
   f6 = ".nc"
   fn = dout + f1 + chr(95) + f2 + chr(95) + f3 + chr(95) + f4 + chr(95) + f5 + f6

   fn_nc = Dataset(fn, "w",  format = "NETCDF4_CLASSIC") 
   
   return fn_nc
   
def ch4n2oco_NC_Global_Attributes_v2(fn_nc, meta, ET):
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
   
def ch4n2oco_NC_Dimensions_v2(fn_nc, ET):
   time = fn_nc.createDimension('time', len(ET) )
   latitude = fn_nc.createDimension('latitude', 1)
   longitude = fn_nc.createDimension('longitude', 1) 
   
def ch4n2oco_NC_VaraiblesAndData_v2(fn_nc, data, np, lat, lon):
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
   
   #CH4 conc
   CH4 = fn_nc.createVariable('mole_fraction_of_methane_in_air', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   CH4.type = 'float32'
   CH4.units = '1e-9'
   CH4.practical_units = 'ppb'
   CH4.standard_name = 'mole_fraction_of_methane_in_air'
   CH4.long_name = 'Mole Fraction of Methane in air'
   XX = data.ch4
   np.putmask(XX, data.flag_ch4 != 1, np.nan)
   CH4.valid_min = np.float32(np.nanmin(XX))
   CH4.valid_max = np.float32(np.nanmax(XX))
   CH4.cell_methods = 'time: point'
   CH4.coordinates = 'latitude longitude'
   CH4.chemical_species = 'CH4'
   #write data
   CH4[:] = np.float32(data.ch4)
   
   #Qc flag CH4
   qc_flags_CH4 = fn_nc.createVariable('qc_flag_ch4', np.int8, ('time',))
   #variable attribute
   qc_flags_CH4.type = 'byte'
   qc_flags_CH4.units = '1'
   qc_flags_CH4.long_name = 'Data Quality Flag: CH4'
   qc_flags_CH4.flag_values = '0b,1b,2b,3b'
   qc_flags_CH4.flag_meanings = 'not_used' + '\n'
   qc_flags_CH4.flag_meanings = qc_flags_CH4.flag_meanings + 'good_data' + '\n'
   qc_flags_CH4.flag_meanings = qc_flags_CH4.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   qc_flags_CH4.flag_meanings = qc_flags_CH4.flag_meanings + 'bad_data_do_not_use' 
   #write data
   qc_flags_CH4[:] = np.int8(data.flag_ch4)
   
   #N2O conc
   N2O = fn_nc.createVariable('mole_fraction_of_nitrous_oxide_in_air', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   N2O.type = 'float32'
   N2O.units = '1e-9'
   N2O.practical_units = 'ppb'
   N2O.standard_name = 'mole_fraction_of_nitrous_oxide_in_air'
   N2O.long_name = 'Mole Fraction of Nitrous Oxide in air'
   XX = data.n2o
   np.putmask(XX, data.flag_n2o != 1, np.nan)
   N2O.valid_min = np.float32(np.nanmin(XX))
   N2O.valid_max = np.float32(np.nanmax(XX))
   N2O.cell_methods = 'time: point'
   N2O.coordinates = 'latitude longitude'
   N2O.chemical_species = 'N2O'
   #write data
   N2O[:] = np.float32(data.n2o)
   
   #Qc flag N2O
   qc_flags_n2o = fn_nc.createVariable('qc_flag_n2o', np.int8, ('time',))
   #variable attribute
   qc_flags_n2o.type = 'byte'
   qc_flags_n2o.units = '1'
   qc_flags_n2o.long_name = 'Data Quality Flag: N2O'
   qc_flags_n2o.flag_values = '0b,1b,2b,3b'
   qc_flags_n2o.flag_meanings = 'not_used' + '\n'
   qc_flags_n2o.flag_meanings = qc_flags_n2o.flag_meanings + 'good_data' + '\n'
   qc_flags_n2o.flag_meanings = qc_flags_n2o.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   qc_flags_n2o.flag_meanings = qc_flags_n2o.flag_meanings + 'bad_data_do_not_use' 
   #write data
   qc_flags_n2o[:] = np.int8(data.flag_n2o)
   
   #CO conc
   CO = fn_nc.createVariable('mole_fraction_of_carbon_monoxide_in_air', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   CO.type = 'float32'
   CO.units = '1e-9'
   CO.practical_units = 'ppb'
   CO.standard_name = 'mole_fraction_of_carbon_monoxide_in_air'
   CO.long_name = 'Mole Fraction of Carbon Monoxide in air'
   XX = data.co
   np.putmask(XX, data.flag_co != 1, np.nan)
   CO.valid_min = np.float32(np.nanmin(XX))
   CO.valid_max = np.float32(np.nanmax(XX))
   CO.cell_methods = 'time: point'
   CO.coordinates = 'latitude longitude'
   CO.chemical_species = 'CO'
   #write data
   CO[:] = np.float32(data.co)
   
   #Qc flag CO
   qc_flags_co = fn_nc.createVariable('qc_flag_co', np.int8, ('time',))
   #variable attribute
   qc_flags_co.type = 'byte'
   qc_flags_co.units = '1'
   qc_flags_co.long_name = 'Data Quality Flag: CO'
   qc_flags_co.flag_values = '0b,1b,2b,3b'
   qc_flags_co.flag_meanings = 'not_used' + '\n'
   qc_flags_co.flag_meanings = qc_flags_co.flag_meanings + 'good_data' + '\n'
   qc_flags_co.flag_meanings = qc_flags_co.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   qc_flags_co.flag_meanings = qc_flags_co.flag_meanings + 'bad_data_do_not_use' 
   #write data
   qc_flags_co[:] = np.int8(data.flag_co)
   
   
def NC_ch4n2oco_v2(pd, np, dout, meta, data):
   fn_nc = ch4n2oco_create_NC_file_v2(dout, data.DT)
   
   lat, lon = ch4n2oco_NC_Global_Attributes_v2(fn_nc, meta, data.ET)
   ch4n2oco_NC_Dimensions_v2(fn_nc, data.ET)
   ch4n2oco_NC_VaraiblesAndData_v2(fn_nc, data, np, lat, lon)

   fn_nc.close()