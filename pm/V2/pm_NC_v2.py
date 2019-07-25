def pm_create_NC_file_v2(dout, DT):
   from netCDF4 import Dataset
   
   f1 = 'uea-fidas200E-1' #instrument name
   f2 = 'wao' #platform name
   mm = str(int(DT[0,1]))
   if len(mm)<2:
      mm = "0" + mm
   dd = str(int(DT[0,2]))
   if len(dd)<2:
      dd = "0" + dd   
   f3 = str(int(DT[0,0])) + mm + dd #date yyyymmdd
   f4 = 'pm-concentration' #data product
   f5 = "v1" #version number
   f6 = ".nc"
   fn = dout + f1 + chr(95) + f2 + chr(95) + f3 + chr(95) + f4 + chr(95) + f5 + f6

   fn_nc = Dataset(fn, "w",  format = "NETCDF4_CLASSIC") 
   
   return fn_nc
   
def pm_NC_Global_Attributes_v2(fn_nc, meta, ET):
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
   
def pm_NC_Dimensions_v2(fn_nc, ET):
   time = fn_nc.createDimension('time', len(ET) )
   latitude = fn_nc.createDimension('latitude', 1)
   longitude = fn_nc.createDimension('longitude', 1) 
   
def pm_NC_VaraiblesAndData_v2(fn_nc, data, np, lat, lon):
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
   
   #PM1
   PM1 = fn_nc.createVariable('mass_concentration_of_pm1_ambient_aerosol_in_air', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   PM1.type = 'float32'
   PM1.units = 'ug m-3'
   PM1.standard_name = 'mass_concentration_of_pm1_ambient_aerosol_in_air'
   PM1.long_name = 'Mass Concentration of PM1 Ambient Aerosol in Air'
   XX = data.pm1
   np.putmask(XX, data.flag_pm1 != 1, np.nan)
   PM1.valid_min = np.float32(np.nanmin(XX))
   PM1.valid_max = np.float32(np.nanmax(XX))
   PM1.cell_methods = 'time: mean'
   PM1.coordinates = 'latitude longitude'
   #write data
   PM1[:] = np.float32(data.pm1)
   
   #Qc flag PM1
   qc_flags_PM1 = fn_nc.createVariable('qc_flag_pm1', np.int8, ('time',))
   #variable attribute
   qc_flags_PM1.type = 'byte'
   qc_flags_PM1.units = '1'
   qc_flags_PM1.long_name = 'Data Quality Flag: PM1'
   qc_flags_PM1.flag_values = '0b,1b,2b,3b'
   qc_flags_PM1.flag_meanings = 'not_used' + '\n'
   qc_flags_PM1.flag_meanings = qc_flags_PM1.flag_meanings + 'good_data' + '\n'
   qc_flags_PM1.flag_meanings = qc_flags_PM1.flag_meanings + 'bad_data_pm1_outside_sensor_operational_range' + '\n'
   qc_flags_PM1.flag_meanings = qc_flags_PM1.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   qc_flags_PM1[:] = np.int8(data.flag_pm1)
   
   #PM2.5
   PM25 = fn_nc.createVariable('mass_concentration_of_pm2p5_ambient_aerosol_in_air', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   PM25.type = 'float32'
   PM25.units = 'ug m-3'
   PM25.standard_name = 'mass_concentration_of_pm2p5_ambient_aerosol_in_air'
   PM25.long_name = 'Mass Concentration of PM2.5 Ambient Aerosol in Air'
   XX = data.pm25
   np.putmask(XX, data.flag_pm25 != 1, np.nan)
   PM25.valid_min = np.float32(np.nanmin(XX))
   PM25.valid_max = np.float32(np.nanmax(XX))
   PM25.cell_methods = 'time: mean'
   PM25.coordinates = 'latitude longitude'
   #write data
   PM25[:] = np.float32(data.pm25)
   
   #Qc flag PM2.5
   qc_flags_PM25 = fn_nc.createVariable('qc_flag_pm2p5', np.int8, ('time',))
   #variable attribute
   qc_flags_PM25.type = 'byte'
   qc_flags_PM25.units = '1'
   qc_flags_PM25.long_name = 'Data Quality Flag: PM2.5'
   qc_flags_PM25.flag_values = '0b,1b,2b,3b'
   qc_flags_PM25.flag_meanings = 'not_used' + '\n'
   qc_flags_PM25.flag_meanings = qc_flags_PM25.flag_meanings + 'good_data' + '\n'
   qc_flags_PM25.flag_meanings = qc_flags_PM25.flag_meanings + 'bad_data_pm2.5_outside_sensor_operational_range' + '\n'
   qc_flags_PM25.flag_meanings = qc_flags_PM25.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   qc_flags_PM25[:] = np.int8(data.flag_pm25)
   
   #PM4
   PM4 = fn_nc.createVariable('mass_concentration_of_pm4_ambient_aerosol_in_air', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   PM4.type = 'float32'
   PM4.units = 'ug m-3'
   PM4.long_name = 'Mass Concentration of PM4 Ambient Aerosol in Air'
   XX = data.pm4
   np.putmask(XX, data.flag_pm4 != 1, np.nan)
   PM4.valid_min = np.float32(np.nanmin(XX))
   PM4.valid_max = np.float32(np.nanmax(XX))
   PM4.cell_methods = 'time: mean'
   PM4.coordinates = 'latitude longitude'
   #write data
   PM4[:] = np.float32(data.pm4)
   
   #Qc flag PM4
   qc_flags_PM4 = fn_nc.createVariable('qc_flag_pm4', np.int8, ('time',))
   #variable attribute
   qc_flags_PM4.type = 'byte'
   qc_flags_PM4.units = '1'
   qc_flags_PM4.long_name = 'Data Quality Flag: PM4'
   qc_flags_PM4.flag_values = '0b,1b,2b,3b'
   qc_flags_PM4.flag_meanings = 'not_used' + '\n'
   qc_flags_PM4.flag_meanings = qc_flags_PM4.flag_meanings + 'good_data' + '\n'
   qc_flags_PM4.flag_meanings = qc_flags_PM4.flag_meanings + 'bad_data_pm4_outside_sensor_operational_range' + '\n'
   qc_flags_PM4.flag_meanings = qc_flags_PM4.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   qc_flags_PM4[:] = np.int8(data.flag_pm4)
   
   #PM10
   PM10 = fn_nc.createVariable('mass_concentration_of_pm10_ambient_aerosol_in_air', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   PM10.type = 'float32'
   PM10.units = 'ug m-3'
   PM10.standard_name = 'mass_concentration_of_pm10_ambient_aerosol_in_air'
   PM10.long_name = 'Mass Concentration of PM10 Ambient Aerosol in Air'
   XX = data.pm10
   np.putmask(XX, data.flag_pm10 != 1, np.nan)
   PM10.valid_min = np.float32(np.nanmin(XX))
   PM10.valid_max = np.float32(np.nanmax(XX))
   PM10.cell_methods = 'time: mean'
   PM10.coordinates = 'latitude longitude'
   #write data
   PM10[:] = np.float32(data.pm10)
   
   #Qc flag PM10
   qc_flags_PM10 = fn_nc.createVariable('qc_flag_pm10', np.int8, ('time',))
   #variable attribute
   qc_flags_PM10.type = 'byte'
   qc_flags_PM10.units = '1'
   qc_flags_PM10.long_name = 'Data Quality Flag: PM10'
   qc_flags_PM10.flag_values = '0b,1b,2b,3b'
   qc_flags_PM10.flag_meanings = 'not_used' + '\n'
   qc_flags_PM10.flag_meanings = qc_flags_PM10.flag_meanings + 'good_data' + '\n'
   qc_flags_PM10.flag_meanings = qc_flags_PM10.flag_meanings + 'bad_data_pm10_outside_sensor_operational_range' + '\n'
   qc_flags_PM10.flag_meanings = qc_flags_PM10.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   qc_flags_PM10[:] = np.int8(data.flag_pm10)
   
   #PM Total
   PMT = fn_nc.createVariable('mass_concentration_of_total_pm_ambient_aerosol_in_air', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   PMT.type = 'float32'
   PMT.units = 'ug m-3'
   PMT.long_name = 'Mass Concentration of Total PM Ambient Aerosol Particles in air'
   XX = data.pm_tot
   np.putmask(XX, data.flag_pm_tot != 1, np.nan)
   PMT.valid_min = np.float32(np.nanmin(XX))
   PMT.valid_max = np.float32(np.nanmax(XX))
   PMT.cell_methods = 'time: mean'
   PMT.coordinates = 'latitude longitude'
   #write data
   PMT[:] = np.float32(data.pm_tot)
   
   #Qc flag PMT
   qc_flags_PMT = fn_nc.createVariable('qc_flag_total_pm', np.int8, ('time',))
   #variable attribute
   qc_flags_PMT.type = 'byte'
   qc_flags_PMT.units = '1'
   qc_flags_PMT.long_name = 'Data Quality Flag: Total PM'
   qc_flags_PMT.flag_values = '0b,1b,2b,3b'
   qc_flags_PMT.flag_meanings = 'not_used' + '\n'
   qc_flags_PMT.flag_meanings = qc_flags_PMT.flag_meanings + 'good_data' + '\n'
   qc_flags_PMT.flag_meanings = qc_flags_PMT.flag_meanings + 'bad_data_total_pm_outside_sensor_operational_range' + '\n'
   qc_flags_PMT.flag_meanings = qc_flags_PMT.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   qc_flags_PMT[:] = np.int8(data.flag_pm_tot)
   
   #N
   N = fn_nc.createVariable('number_concentration_of_ambient_aerosol_particles_in_air', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   N.type = 'float32'
   N.units = 'cm-3'
   N.standard_name = 'number_concentration_of_ambient_aerosol_particles_in_air'
   N.long_name = 'Number Concentration of Ambient Aerosol Particles in air'
   XX = data.n
   np.putmask(XX, data.flag_n != 1, np.nan)
   N.valid_min = np.float32(np.nanmin(XX))
   N.valid_max = np.float32(np.nanmax(XX))
   N.cell_methods = 'time: mean'
   N.coordinates = 'latitude longitude'
   #write data
   N[:] = np.float32(data.n)
   
   #Qc flag N
   qc_flags_N = fn_nc.createVariable('qc_flag_total_number', np.int8, ('time',))
   #variable attribute
   qc_flags_N.type = 'byte'
   qc_flags_N.units = '1'
   qc_flags_N.long_name = 'Data Quality Flag: Total Number'
   qc_flags_N.flag_values = '0b,1b,2b,3b'
   qc_flags_N.flag_meanings = 'not_used' + '\n'
   qc_flags_N.flag_meanings = qc_flags_N.flag_meanings + 'good_data' + '\n'
   qc_flags_N.flag_meanings = qc_flags_N.flag_meanings + 'bad_data_total_number_outside_sensor_operational_range' + '\n'
   qc_flags_N.flag_meanings = qc_flags_N.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   qc_flags_N[:] = np.int8(data.flag_n)
   
   
def NC_pm_v2(pd, np, dout, meta, data):
   fn_nc = pm_create_NC_file_v2(dout, data.DT)
   
   lat, lon = pm_NC_Global_Attributes_v2(fn_nc, meta, data.ET)
   pm_NC_Dimensions_v2(fn_nc, data.ET)
   pm_NC_VaraiblesAndData_v2(fn_nc, data, np, lat, lon)

   fn_nc.close()