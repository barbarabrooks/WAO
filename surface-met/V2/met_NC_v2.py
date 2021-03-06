def met_create_NC_file_v2(dout, DT):
   from netCDF4 import Dataset
   
   f1 = 'ncas-aws-6' #instrument name
   f2 = 'wao' #platform name
   mm = str(int(DT[0,1]))
   if len(mm)<2:
      mm = "0" + mm
   dd = str(int(DT[0,2]))
   if len(dd)<2:
      dd = "0" + dd   
   f3 = str(int(DT[0,0])) + mm + dd #date yyyymmdd
   f4 = 'surface-met' #data product
   f5 = "v1" #version number
   f6 = ".nc"
   fn = dout + f1 + chr(95) + f2 + chr(95) + f3 + chr(95) + f4 + chr(95) + f5 + f6

   fn_nc = Dataset(fn, "w",  format = "NETCDF4_CLASSIC") 
   
   return fn_nc
   
def met_NC_Global_Attributes_v2(fn_nc, meta, ET):
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
   
def met_NC_Dimensions_v2(fn_nc, ET):
   time = fn_nc.createDimension('time', len(ET) )
   latitude = fn_nc.createDimension('latitude', 1)
   longitude = fn_nc.createDimension('longitude', 1) 
   
def met_NC_VaraiblesAndData_v2(fn_nc, data, np, lat, lon):
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
   
   #PP
   PP = fn_nc.createVariable('air_pressure', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   PP.type = 'float32'
   PP.units = 'hPa'
   PP.standard_name = 'air_pressure'
   PP.long_name = 'Air Pressure'
   XX = data.pp
   np.putmask(XX, data.flag_pp != 1, np.nan)
   PP.valid_min = np.float32(np.nanmin(XX))
   PP.valid_max = np.float32(np.nanmax(XX))
   PP.cell_methods = 'time: mean'
   PP.coordinates = 'latitude longitude'
   #write data
   PP[:] = np.float32(data.pp)
   
   #Qc flag PP
   qc_flags_PP = fn_nc.createVariable('qc_flag_pressure', np.int8, ('time',))
   #variable attribute
   qc_flags_PP.type = 'byte'
   qc_flags_PP.units = '1'
   qc_flags_PP.long_name = 'Data Quality Flag: Pressure'
   qc_flags_PP.flag_values = '0b,1b,2b,3b'
   qc_flags_PP.flag_meanings = 'not_used' + '\n'
   qc_flags_PP.flag_meanings = qc_flags_PP.flag_meanings + 'good_data' + '\n'
   qc_flags_PP.flag_meanings = qc_flags_PP.flag_meanings + 'bad_data_pressure_outside_sensor_operational_range' + '\n'
   qc_flags_PP.flag_meanings = qc_flags_PP.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   qc_flags_PP[:] = np.int8(data.flag_pp)
   
   #TT
   TT = fn_nc.createVariable('air_temperature', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   TT.type = 'float32'
   TT.units = 'K'
   TT.standard_name = 'air_temperature'
   TT.long_name = 'Air Temperature'
   XX = data.tt
   np.putmask(XX, data.flag_tt != 1, np.nan)
   TT.valid_min = np.float32(np.nanmin(XX))
   TT.valid_max = np.float32(np.nanmax(XX))
   TT.cell_methods = 'time: mean'
   TT.coordinates = 'latitude longitude'
   #write data
   TT[:] = np.float32(data.tt)
   
   #Qc flag TT
   qc_flags_TT = fn_nc.createVariable('qc_flag_temperature', np.int8, ('time',))
   #variable attribute
   qc_flags_TT.type = 'byte'
   qc_flags_TT.units = '1'
   qc_flags_TT.long_name = 'Data Quality Flag: Temperature'
   qc_flags_TT.flag_values = '0b,1b,2b,3b'
   qc_flags_TT.flag_meanings = 'not_used' + '\n'
   qc_flags_TT.flag_meanings = qc_flags_TT.flag_meanings + 'good_data' + '\n'
   qc_flags_TT.flag_meanings = qc_flags_TT.flag_meanings + 'bad_data_temperature_outside_sensor_operational_range' + '\n'
   qc_flags_TT.flag_meanings = qc_flags_TT.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   qc_flags_TT[:] = np.int8(data.flag_tt)
   
   #RH
   RH = fn_nc.createVariable('relative_humidity', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   RH.type = 'float32'
   RH.units = '%'
   RH.standard_name = 'relative_humidity'
   RH.long_name = 'Relative Humidity'
   XX = data.rh
   np.putmask(XX, data.flag_rh != 1, np.nan)
   RH.valid_min = np.float32(np.nanmin(XX))
   RH.valid_max = np.float32(np.nanmax(XX))
   RH.cell_methods = 'time: mean'
   RH.coordinates = 'latitude longitude'
   #write data
   RH[:] = np.float32(data.rh)
   
   #Qc flag RH
   qc_flags_RH = fn_nc.createVariable('qc_flag_relative_humidity', np.int8, ('time',))
   #variable attribute
   qc_flags_RH.type = 'byte'
   qc_flags_RH.units = '1'
   qc_flags_RH.long_name = 'Data Quality Flag: Relative Humidity'
   qc_flags_RH.flag_values = '0b,1b,2b,3b'
   qc_flags_RH.flag_meanings = 'not_used' + '\n'
   qc_flags_RH.flag_meanings = qc_flags_RH.flag_meanings + 'good_data' + '\n'
   qc_flags_RH.flag_meanings = qc_flags_RH.flag_meanings + 'bad_data_relative_humidity_outside_sensor_operational_range' + '\n'
   qc_flags_RH.flag_meanings = qc_flags_RH.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   qc_flags_RH[:] = np.int8(data.flag_rh)
   
   #WS
   WS = fn_nc.createVariable('wind_speed', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   WS.type = 'float32'
   WS.units = 'm s-1'
   WS.standard_name = 'wind_speed'
   WS.long_name = 'Wind Speed'
   XX = data.ws
   np.putmask(XX, data.flag_ws != 1, np.nan)
   WS.valid_min = np.float32(np.nanmin(XX))
   WS.valid_max = np.float32(np.nanmax(XX))
   WS.cell_methods = 'time: mean'
   WS.coordinates = 'latitude longitude'
   #write data
   WS[:] = np.float32(data.ws)
   
   #Qc flag WS
   qc_flags_WS = fn_nc.createVariable('qc_flag_wind_speed', np.int8, ('time',))
   #variable attribute
   qc_flags_WS.type = 'byte'
   qc_flags_WS.units = '1'
   qc_flags_WS.long_name = 'Data Quality Flag: Wind Speed'
   qc_flags_WS.flag_values = '0b,1b,2b,3b,4b'
   qc_flags_WS.flag_meanings = 'not_used' + '\n'
   qc_flags_WS.flag_meanings = qc_flags_WS.flag_meanings + 'good_data' + '\n'
   qc_flags_WS.flag_meanings = qc_flags_WS.flag_meanings + 'suspect_data_measured_wind_speed_==_0_m_s-1' + '\n'
   qc_flags_WS.flag_meanings = qc_flags_WS.flag_meanings + 'bad_data_wind_speed_outside_sensor_operational_range' + '\n'
   qc_flags_WS.flag_meanings = qc_flags_WS.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   qc_flags_WS[:] = np.int8(data.flag_ws)
   
   #WD
   WD = fn_nc.createVariable('wind_from_direction', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   WD.type = 'float32'
   WD.units = 'degree'
   WD.standard_name = 'wind_from_direction'
   WD.long_name = 'Wind From Direction'
   #XX = data.wd
   #np.putmask(XX, data.flag_wd != 1, np.nan)
   #WD.valid_min = np.float32(np.nanmin(XX))
   #WD.valid_max = np.float32(np.nanmax(XX))
   WD.valid_min = np.float32(min(data.wd))
   WD.valid_max = np.float32(max(data.wd))
   WD.cell_methods = 'time: mean'
   WD.coordinates = 'latitude longitude'
   #write data
   WD[:] = np.float32(data.wd)
   
   #Qc flag WD
   qc_flags_WD = fn_nc.createVariable('qc_flag_wind_from_direction', np.int8, ('time',))
   #variable attribute
   qc_flags_WD.type = 'byte'
   qc_flags_WD.units = '1'
   qc_flags_WD.long_name = 'Data Quality Flag: Wind From Direction'
   qc_flags_WD.flag_values = '0b,1b,2b,3b,4b'
   qc_flags_WD.flag_meanings = 'not_used' + '\n'
   qc_flags_WD.flag_meanings = qc_flags_WD.flag_meanings + 'good_data' + '\n'
   qc_flags_WD.flag_meanings = qc_flags_WD.flag_meanings + 'suspect_data_measured_wind_speed_==_0_m_s-1' + '\n'
   qc_flags_WD.flag_meanings = qc_flags_WD.flag_meanings + 'bad_data_wind_direction_outside_sensor_operational_range' + '\n'
   qc_flags_WD.flag_meanings = qc_flags_WD.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   qc_flags_WD[:] = np.int8(data.flag_wd)
   
   
def NC_met_v2(pd, np, dout, meta, data):
   fn_nc = met_create_NC_file_v2(dout, data.DT)
   
   lat, lon = met_NC_Global_Attributes_v2(fn_nc, meta, data.ET)
   met_NC_Dimensions_v2(fn_nc, data.ET)
   met_NC_VaraiblesAndData_v2(fn_nc, data, np, lat, lon)

   fn_nc.close()