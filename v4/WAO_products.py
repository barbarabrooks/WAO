def create_NC_file(nm, dp, ver, opt1, opt2, opt3, start_date, logfile):
   from netCDF4 import Dataset
   from datetime import datetime
   
   try:
      # create nc file
      from netCDF4 import Dataset
      dout = 'Data\\'
      f1 = nm # instrument name
      f2 = 'wao'
      f3 = datetime.fromtimestamp(int(start_date)).strftime('%Y%m') # date
      f4 = dp # data product
      f5 = 'v' + ver # version number
      f6 = '.nc'
      
      if ((len(opt1)<1) and (len(opt2)<1) and (len(opt3)<1)):
         fn = dout+f1+chr(95)+f2+chr(95)+f3+chr(95)+f4+chr(95)+f5+f6         
      if ((len(opt1)>1) and (len(opt2)<1) and (len(opt3)<1)):
         fn = dout+f1+chr(95)+f2+chr(95)+f3+chr(95)+f4+chr(95)+opt1+chr(95)+f5+f6
      if ((len(opt1)>1) and (len(opt2)>1) and (len(opt3)<1)):
         fn = dout+f1+chr(95)+f2+chr(95)+f3+chr(95)+f4+chr(95)+opt1+chr(95)+opt2+chr(95)+f5+f6
      if ((len(opt1)>1) and (len(opt2)>1) and (len(opt3)>1)):
         fn = dout+f1+chr(95)+f2+chr(95)+f3+chr(95)+f4+chr(95)+opt1+chr(95)+opt2+chr(95)+opt3+chr(95)+f5+f6
      
      nc = Dataset(fn, "w",  format = "NETCDF4_CLASSIC") 
   except:
      # exit if problem encountered
      print('Unable to create: ',fn,'. This program will terminate')
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat()+' Unable to create: '+fn+'. This program will terminate\n')
      g.close()
      exit()
      
      del Dataset, datetime

   return nc

# A
def acoustic_backscatter_winds(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write specific dimensions
   altitude = nc.createDimension('altitude', len(data.H[1,:]))
   
   # write common variables
   com.variables(nc, data)  
   
   # write specific variables
   v = nc.createVariable('altitude', np.float32, ('altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm'
   v.standard_name = 'altitude'
   v.long_name = 'Geometric height above geoid (WGS84).'
   v.axis = 'Z'
   v.valid_min = np.float32(min(data.H[1,:])) + 10
   v.valid_max = np.float32(max(data.H[1,:])) + 10
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.H[1,:]) + 10
   
   v = nc.createVariable('sound_intensity_level_in_air', np.float32, ('time', 'altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'dB'
   v.standard_name = 'sound_intensity_level_in_air'
   v.long_name = 'Sound Intensity Level in Air'
   xx = data.R
   np.putmask(xx, data.qc_backscatter != 1, np.nan)
   v.valid_min = np.float32(np.nanmin(xx))
   v.valid_max = np.float32(np.nanmax(xx))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(data.R)
   
   v = nc.createVariable('wind_speed', np.float32, ('time', 'altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.standard_name = 'wind_speed'
   v.long_name = 'Wind Speed'
   xx = data.V
   np.putmask(xx, data.qc_mean_winds != 1, np.nan)
   v.valid_min = np.float32(np.nanmin(xx))
   v.valid_max = np.float32(np.nanmax(xx))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(data.V)
   
   v = nc.createVariable('wind_from_direction', np.float32, ('time', 'altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'degree'
   v.standard_name = 'wind_from_direction'
   v.long_name = 'Wind From Direction'
   xx = data.D
   np.putmask(xx, data.qc_mean_winds != 1, np.nan)
   v.valid_min = np.float32(np.nanmin(xx))
   v.valid_max = np.float32(np.nanmax(xx))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(data.D)
  
   v = nc.createVariable('eastward_wind', np.float32, ('time', 'altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.standard_name = 'eastward_wind'
   v.long_name = 'Eastward Wind Component (U)'
   xx = data.VVU
   np.putmask(xx, data.qc_wind_component_eastward != 1, np.nan)
   v.valid_min = np.float32(np.nanmin(xx))
   v.valid_max = np.float32(np.nanmax(xx))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(data.VVU)
   
   v = nc.createVariable('northward_wind', np.float32, ('time', 'altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.standard_name = 'northward_wind'
   v.long_name = 'Northward Wind Component (V)'
   xx = data.VVV
   np.putmask(xx, data.qc_wind_component_northward != 1, np.nan)
   v.valid_min = np.float32(np.nanmin(xx))
   v.valid_max = np.float32(np.nanmax(xx))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(data.VVV)
   
   v = nc.createVariable('upward_air_velocity', np.float32, ('time', 'altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.standard_name = 'upward_air_velocity'
   v.long_name = 'Upward Air Velocity (W)'
   xx = data.VVW
   np.putmask(xx, data.qc_wind_component_upward_air_velocity != 1, np.nan)
   v.valid_min = np.float32(np.nanmin(xx))
   v.valid_max = np.float32(np.nanmax(xx))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(data.VVW)
   
   v = nc.createVariable('qc_flag_mean_winds', np.int8, ('time', 'altitude',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Mean Winds'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b,7b,8b,9b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise<0' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise>50' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:mean_wind_speed<0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:mean_wind_speed>35ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:mean_wind_direction<0degrees' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:mean_wind_direction>=360degrees' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:mean_wind_speed==0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:time_stamp_error' 
   #write data
   v[:,:] = np.int8(data.qc_mean_winds)
   
   v = nc.createVariable('qc_flag_wind_component_eastward', np.int8, ('time', 'altitude',))
   #variable attribute
   v.units = '1'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b,7b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise<0' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise>50' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:U_component<-10ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:U_component>10ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:U_component==0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:time_stamp_error' 
   #write data
   v[:,:] = np.int8(data.qc_wind_component_eastward)
   
   v = nc.createVariable('qc_flag_wind_component_northward', np.int8, ('time', 'altitude',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Northward Wind Component (V)'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b,7b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise<0' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise>50' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:U_component<-10ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:U_component>10ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:U_component==0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:time_stamp_error' 
   #write data
   v[:,:] = np.int8(data.qc_wind_component_northward)
   
   v = nc.createVariable('qc_flag_wind_component_upward_air_velocity', np.int8, ('time', 'altitude',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Upward Air Velocity (W)'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b,7b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise<0' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise>50' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:U_component<-10ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:U_component>10ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:U_component==0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:time_stamp_error' 
   #write data
   v[:,:] = np.int8(data.qc_wind_component_upward_air_velocity)
   
   v = nc.createVariable('qc_flag_backscatter', np.int8, ('time', 'altitude',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Backscatter'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise<0' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise>50' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:backscatter<1dB' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:backscatter>90db' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:time_stamp_error' 
   #write data
   v[:,:] = np.int8(data.qc_backscatter)
   
def aerosol_backscatter(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
   nc.setncattr('laser_wavelength', '905 nm')
   nc.setncattr('nominal_laser_pulse_energy', '1.6e-06 J')
   nc.setncattr('pulse_repetition_frequency', '5570 s-1')
   nc.setncattr('lens_diameter', '0.145 m')
   nc.setncattr('beam_divergence', '0.53 mrad')
   nc.setncattr('pulse_length', 'Not Known')
   nc.setncattr('sampling_frequency', 'Not Known')
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write specific dimensions
   altitude = nc.createDimension('altitude', 256)
   
   # write common variables
   com.variables(nc, data)    

   # write specific variables
   v = nc.createVariable('altitude', np.float32, ('altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm'
   v.standard_name = 'altitude'
   v.long_name = 'Geometric height above geoid (WGS84).'
   v.axis = 'Z'
   v.valid_min = np.float32(min(data.ZZ))
   v.valid_max = np.float32(max(data.ZZ))
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.ZZ)
      
   v = nc.createVariable('attenuated_aerosol_backscatter_coefficient', np.float32, ('time', 'altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm-1 sr-1'
   v.long_name = 'Attenuated Aerosol Backscatter Coefficient'
   xx = data.BB
   np.putmask(xx, data.BB_flag != 1, np.nan)
   v.valid_min = np.float32(np.nanmin(xx))
   v.valid_max = np.float32(np.nanmax(xx))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(data.BB)    
   
   v = nc.createVariable('laser_pulse_energy', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = '%'
   v.long_name = 'Laser Pulse Energy (% of maximum)'
   v.valid_min = np.float32(min(data.L33))
   v.valid_max = np.float32(max(data.L33))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.L33)
   
   v = nc.createVariable('laser_temperature', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'K'
   v.long_name = 'Laser Temperature'
   v.valid_min = np.float32(min(data.L34))
   v.valid_max = np.float32(max(data.L34))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.L34)
   
   v = nc.createVariable('sensor_zenith_angle', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'degree'
   v.standard_name = 'sensor_zenith_angle'
   v.long_name = 'Sensor Zenith Angle (from vertical)'
   v.valid_min = np.float32(min(data.L37))
   v.valid_max = np.float32(max(data.L37))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.L37)
   
   v = nc.createVariable('profile_scaling', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = '%'
   v.long_name = 'Scaling of range profile (default = 100%)'
   v.valid_min = np.float32(min(data.L31))
   v.valid_max = np.float32(max(data.L31))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.L31)
   
   v = nc.createVariable('window_contamination', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'mV'
   v.long_name = 'Window Contamination (mV as measured by ADC: 0 - 2500)'
   v.valid_min = np.float32(min(data.L36))
   v.valid_max = np.float32(max(data.L36))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.L36)
   
   v = nc.createVariable('background_light', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'mV'
   v.long_name = 'Background Light (mV as measured by ADC: 0 - 2500)'
   v.valid_min = np.float32(min(data.L38))
   v.valid_max = np.float32(max(data.L38))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.L38)
   
   v = nc.createVariable('backscatter_sum', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'sr-1'
   v.long_name = 'Sum of detected and normalized backscatter'
   v.valid_min = np.float32(min(data.L310))
   v.valid_max = np.float32(max(data.L310))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.L310)
   
   v = nc.createVariable('qc_flag', np.float32, ('time', 'altitude',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_attenuated_aerosol_backscatter_coefficient_outside_instrument_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   #write data
   v[:,:] = np.int8(data.BB_flag)
      
#B
#C   
def ch4_concentration(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables  
   if len(data.mole_frac) == len(data.ET):
      v = nc.createVariable('mole_fraction_of_methane_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mole_fraction_of_methane_in_air'
      v.long_name = 'Mole Fraction of Methane in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CH4'
      #write data
      v[:] = np.float32(data.mole_frac)
   
   if len(data.mass_frac) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_methane_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mass_fraction_of_methane_in_air'
      v.long_name = 'Mass Fraction of Methane in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CH4'
      #write data
      v[:] = np.float32(data.mass_frac)
   
   if len(data.mole_conc) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_methane_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mole_concentration_of_methane_in_air'
      v.long_name = 'Mole Concentration of Methane in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CH4'
      #write data
      v[:] = np.float32(data.mole_conc)
   
   if len(data.mass_conc) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_methane_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mass_concentration_of_methane_in_air'
      v.long_name = 'Mass Concentration of Methane in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CH4'
      #write data
      v[:] = np.float32(data.mass_conc)
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   #write data
   v[:] = np.int8(data.flag)
      
         
def ch4_n2o_co2_co_concentration(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   
   if len(data.mole_frac1) == len(data.ET):
      v = nc.createVariable('mole_fraction_of_methane_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.practical_units = data.practical_units1
      v.standard_name = 'mole_fraction_of_methane_in_air'
      v.long_name = 'Mole Fraction of Methane in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: mean'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CH4'
      #write data
      v[:] = np.float32(data.mole_frac1)
   
   if len(data.mass_frac1) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_methane_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.practical_units = data.practical_units1
      v.standard_name = 'mass_fraction_of_methane_in_air'
      v.long_name = 'Mass Fraction of Methane in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: mean'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CH4'
      #write data
      v[:] = np.float32(data.mass_frac1)
   
   if len(data.mole_conc1) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_methane_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.standard_name = 'mole_concentration_of_methane_in_air'
      v.long_name = 'Mole Concentration of Methane in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: mean'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CH4'
      #write data
      v[:] = np.float32(data.mole_conc1)
   
   if len(data.mass_conc1) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_methane_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.standard_name = 'mass_concentration_of_methane_in_air'
      v.long_name = 'Mass Concentration of Methane in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: mean'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CH4'
      #write data
      v[:] = np.float32(data.mass_conc1)
   
   if len(data.mole_frac2) == len(data.ET):
      # write specific variables
      v = nc.createVariable('mole_fraction_of_nitrous_oxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit2
      v.practical_units = data.practical_units2
      v.standard_name = 'mole_fraction_of_nitrous_oxide_in_air'
      v.long_name = 'Mole Fraction of Nitrous Oxide in air'
      v.valid_min = np.float32(data.min_dat2)
      v.valid_max = np.float32(data.max_dat2)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'N2O'
      #write data
      v[:] = np.float32(data.mole_frac2)
   
   if len(data.mass_frac2) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_nitrous_oxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit2
      v.practical_units = data.practical_units2
      v.standard_name = 'mass_fraction_of_nitrous_oxide_in_air'
      v.long_name = 'Mass Fraction of Nitrous Oxide in air'
      v.valid_min = np.float32(data.min_dat2)
      v.valid_max = np.float32(data.max_dat2)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'N2O'
      #write data
      v[:] = np.float32(data.mass_frac2)
   
   if len(data.mole_conc2) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_nitrous_oxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit2
      v.standard_name = 'mole_concentration_of_nitrous_oxide_in_air'
      v.long_name = 'Mole Concentration of Nitrous Oxide in air'
      v.valid_min = np.float32(data.min_dat2)
      v.valid_max = np.float32(data.max_dat2)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'N2O'
      #write data
      v[:] = np.float32(data.mole_conc2)
   
   if len(data.mass_conc2) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_nitrous_oxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit2
      v.standard_name = 'mass_concentration_of_nitrous_oxide_in_air'
      v.long_name = 'Mass Concentration of Nitrous Oxide in air'
      v.valid_min = np.float32(data.min_dat2)
      v.valid_max = np.float32(data.max_dat2)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'N2O'
      #write data
      v[:] = np.float32(data.mass_conc2)
      
   if len(data.mole_frac3) == len(data.ET):
      v = nc.createVariable('mole_fraction_of_carbon_monoxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit3
      v.practical_units = data.practical_units3
      v.standard_name = 'mole_fraction_of_carbon_monoxide_in_air'
      v.long_name = 'Mole Fraction of Carbon Monoxide in air'
      v.valid_min = np.float32(data.min_dat3)
      v.valid_max = np.float32(data.max_dat3)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO'
      #write data
      v[:] = np.float32(data.mole_frac3)
   
   if len(data.mass_frac3) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_carbon_monoxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit3
      v.practical_units = data.practical_units3
      v.standard_name = 'mass_fraction_of_carbon_monoxide_in_air'
      v.long_name = 'Mass Fraction of Carbon Monoxide in air'
      v.valid_min = np.float32(data.min_dat3)
      v.valid_max = np.float32(data.max_dat3)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO'
      #write data
      v[:] = np.float32(data.mass_frac3)
   
   if len(data.mole_conc3) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_carbon_monoxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit3
      v.standard_name = 'mole_concentration_of_carbon_dioxide_in_air'
      v.long_name = 'Mole Concentration of Carbon Monoxide in air'
      v.valid_min = np.float32(data.min_dat3)
      v.valid_max = np.float32(data.max_dat3)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO'
      #write data
      v[:] = np.float32(data.mole_conc3)
   
   if len(data.mass_conc3) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_carbon_monoxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit3
      v.standard_name = 'mass_concentration_of_carbon_monoxide_in_air'
      v.long_name = 'Mass Concentration of Carbon Monoxide in air'
      v.valid_min = np.float32(data.min_dat3)
      v.valid_max = np.float32(data.max_dat3)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO'
      #write data
      v[:] = np.float32(data.mass_conc3)   
   
   if len(data.mole_frac4) == len(data.ET): 
      v = nc.createVariable('mole_fraction_of_carbon_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit4
      v.practical_units = data.practical_units4
      v.standard_name = 'mole_fraction_of_carbon_dioxide_in_air'
      v.long_name = 'Mole Fraction of Carbon Dioxide in air'
      v.valid_min = np.float32(data.min_dat4)
      v.valid_max = np.float32(data.max_dat4)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO2'
      #write data
      v[:] = np.float32(data.mole_frac4)
   
   if len(data.mass_frac4) == len(data.ET): 
      v = nc.createVariable('mass_fraction_of_carbon_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit4
      v.practical_units = data.practical_units4
      v.standard_name = 'mass_fraction_of_carbon_dioxide_in_air'
      v.long_name = 'Mass Fraction of Carbon Dioxide in air'
      v.valid_min = np.float32(data.min_dat4)
      v.valid_max = np.float32(data.max_dat4)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO2'
      #write data
      v[:] = np.float32(data.mass_frac4)
   
   if len(data.mole_conc4) == len(data.ET): 
      v = nc.createVariable('mole_concentration_of_carbon_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit4
      v.standard_name = 'mole_concentration_of_carbon_dioxide_in_air'
      v.long_name = 'Mole Concentration of Carbon Dioxide in air'
      v.valid_min = np.float32(data.min_dat4)
      v.valid_max = np.float32(data.max_dat4)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO2'
      #write data
      v[:] = np.float32(data.mole_conc4)
   
   if len(data.mass_conc4) == len(data.ET): 
      v = nc.createVariable('mass_concentration_of_carbon_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit4
      v.standard_name = 'mass_concentration_of_carbon_dioxide_in_air'
      v.long_name = 'Mass Concentration of Carbon Dioxide in air'
      v.valid_min = np.float32(data.min_dat4)
      v.valid_max = np.float32(data.max_dat4)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO2'
      #write data
      v[:] = np.float32(data.mass_conc4)
      
   v = nc.createVariable('qc_flag_ch4', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: CH4'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   #write data
   v[:] = np.int8(data.flag1)
   
   v = nc.createVariable('qc_flag_n2o', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: N2O'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   #write data
   v[:] = np.int8(data.flag2)
   
   v = nc.createVariable('qc_flag_co', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: CO'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   #write data
   v[:] = np.int8(data.flag3)
   
   v = nc.createVariable('qc_flag_co2', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: CO2'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   #write data
   v[:] = np.int8(data.flag4)

def cloud_base(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
   nc.setncattr('laser_wavelength', '905 nm')
   nc.setncattr('nominal_laser_pulse_energy', '1.6e-06 J')
   nc.setncattr('pulse_repetition_frequency', '5570 s-1')
   nc.setncattr('lens_diameter', '0.145 m')
   nc.setncattr('beam_divergence', '0.53 mrad')
   nc.setncattr('pulse_length', 'Not Known')
   nc.setncattr('sampling_frequency', 'Not Known')
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write specific dimensions
   layer_index = nc.createDimension('layer_index', 3)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('cloud_base_altitude', np.float32, ('time','layer_index',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm'
   v.standard_name = 'cloud_base_altitude'
   v.long_name = 'Cloud Base Altitude (Geometric height above geoid WGS84)'
   xx1 = data.CBH[:,0]
   np.putmask(xx1, data.CBH_flag != 1, np.nan)
   np.putmask(xx1, xx1 < 0, np.nan)
   xx2 = data.CBH[:,1]
   np.putmask(xx2, data.CBH_flag != 1, np.nan)
   np.putmask(xx2, xx2 < 0, np.nan)
   xx3 = data.CBH[:,2]
   np.putmask(xx3, data.CBH_flag != 1, np.nan)
   np.putmask(xx3, xx3 < 0, np.nan)
   yy = np.array([xx1, xx2, xx3])
   v.valid_min = np.float32(np.nanmin(yy))
   v.valid_max = np.float32(np.nanmax(yy))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(data.CBH)
   
   v = nc.createVariable('laser_pulse_energy', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = '%'
   v.long_name = 'Laser Pulse Energy (% of maximum)'
   v.valid_min = np.float32(min(data.L33))
   v.valid_max = np.float32(max(data.L33))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.L33)
   
   v = nc.createVariable('laser_temperature', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'K'
   v.long_name = 'Laser Temperature'
   v.valid_min = np.float32(min(data.L34))
   v.valid_max = np.float32(max(data.L34))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.L34)
   
   v = nc.createVariable('sensor_zenith_angle', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'degree'
   v.standard_name = 'sensor_zenith_angle'
   v.long_name = 'Sensor Zenith Angle (from vertical)'
   v.valid_min = np.float32(min(data.L37))
   v.valid_max = np.float32(max(data.L37))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.L37)
   
   v = nc.createVariable('profile_scaling', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = '%'
   v.long_name = 'Scaling of range profile (default = 100%)'
   v.valid_min = np.float32(min(data.L31))
   v.valid_max = np.float32(max(data.L31))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.L31)
   
   v = nc.createVariable('window_contamination', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'mV'
   v.long_name = 'Window Contamination (mV as measured by ADC: 0 - 2500)'
   v.valid_min = np.float32(min(data.L36))
   v.valid_max = np.float32(max(data.L36))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.L36)
   
   v = nc.createVariable('background_light', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'mV'
   v.long_name = 'Background Light (mV as measured by ADC: 0 - 2500)'
   v.valid_min = np.float32(min(data.L38))
   v.valid_max = np.float32(max(data.L38))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.L38)
   
   v = nc.createVariable('backscatter_sum', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'sr-1'
   v.long_name = 'Sum of detected and normalized backscatter'
   v.valid_min = np.float32(min(data.L310))
   v.valid_max = np.float32(max(data.L310))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.L310)
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_no_signifcant_backscatter' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_full_obscuration_determined_but_no_cloud_base_detected' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_some_obscuration_detected_but_determined_to_be_transparent' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_raw_data_missing' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   #write data
   v[:] = np.int8(data.CBH_flag)
            
def co_h2_concentration(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   if len(data.mole_frac1) == len(data.ET):
      v = nc.createVariable('mole_fraction_of_carbon_monoxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.practical_units = practical_units1
      v.standard_name = 'mole_fraction_of_carbon_monoxide_in_air'
      v.long_name = 'Mole Fraction of Carbon Monoxide in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO'
      #write data
      v[:] = np.float32(data.mole_frac1)
   
   
   if len(data.mass_frac1) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_carbon_monoxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.practical_units = data.practical_units1
      v.standard_name = 'mass_fraction_of_carbon_monoxide_in_air'
      v.long_name = 'Mass Fraction of Carbon Monoxide in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO'
      #write data
      v[:] = np.float32(data.mass_frac1)
   
   if len(data.mole_conc1) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_carbon_monoxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.standard_name = 'mole_concentration_of_carbon_dioxide_in_air'
      v.long_name = 'Mole Concentration of Carbon Monoxide in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO'
      #write data
      v[:] = np.float32(data.mole_conc1)
   
   if len(data.mass_conc1) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_carbon_monoxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.standard_name = 'mass_concentration_of_carbon_monoxide_in_air'
      v.long_name = 'Mass Concentration of Carbon Monoxide in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO'
      #write data
      v[:] = np.float32(data.mass_conc1)
   
   if len(data.mole_frac) == len(data.ET):
      v = nc.createVariable('mole_fraction_of_molecular_hydrogen_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mole_fraction_of_molecular_hydrogen_in_air'
      v.long_name = 'Mole Fraction of Molecular Hydrogen in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'H2'
      #write data
      v[:] = np.float32(data.mole_frac)
   
   if len(data.mass_frac) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_molecular_hydrogen_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mass_fraction_of_molecular_hydrogen_in_air'
      v.long_name = 'Mass Fraction of Molecular Hydrogen in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'H2'
      #write data
      v[:] = np.float32(data.mass_frac)
   
   if len(data.mole_conc) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_molecular_hydrogen_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mole_concentration_of_molecular_hydrogen_in_air'
      v.long_name = 'Mole Concentration of Molecular Hydrogen in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'H2'
      #write data
      v[:] = np.float32(data.mole_conc)
   
   if len(data.mass_conc) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_molecular_hydrogen_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mass_concentration_of_molecular_hydrogen_in_air'
      v.long_name = 'Mass Concentration of Molecular Hydrogen in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'H2'
      #write data
      v[:] = np.float32(data.mass_conc)
   
   v = nc.createVariable('qc_flag_co', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: CO'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   #write data
   v[:] = np.int8(data.flag1)
   
   v = nc.createVariable('qc_flag_h2', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: H2'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag)
                  
def co2_concentration(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   if len(data.mole_frac) == len(data.ET): 
      v = nc.createVariable('mole_fraction_of_carbon_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit4
      v.practical_units = data.practical_units
      v.standard_name = 'mole_fraction_of_carbon_dioxide_in_air'
      v.long_name = 'Mole Fraction of Carbon Dioxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO2'
      #write data
      v[:] = np.float32(data.mole_frac)
   
   if len(data.mass_frac) == len(data.ET): 
      v = nc.createVariable('mass_fraction_of_carbon_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mass_fraction_of_carbon_dioxide_in_air'
      v.long_name = 'Mass Fraction of Carbon Dioxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO2'
      #write data
      v[:] = np.float32(data.mass_frac)
   
   if len(data.mole_conc) == len(data.ET): 
      v = nc.createVariable('mole_concentration_of_carbon_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mole_concentration_of_carbon_dioxide_in_air'
      v.long_name = 'Mole Concentration of Carbon Dioxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO2'
      #write data
      v[:] = np.float32(data.mole_conc)
   
   if len(data.mass_conc) == len(data.ET): 
      v = nc.createVariable('mass_concentration_of_carbon_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mass_concentration_of_carbon_dioxide_in_air'
      v.long_name = 'Mass Concentration of Carbon Dioxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'CO2'
      #write data
      v[:] = np.float32(data.mass_conc)
      
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag)
   
# D   
# E
# F
# G
# H
def h2_concentration(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   if len(data.mole_frac) == len(data.ET):
      v = nc.createVariable('mole_fraction_of_molecular_hydrogen_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mole_fraction_of_molecular_hydrogen_in_air'
      v.long_name = 'Mole Fraction of Molecular Hydrogen in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'H2'
      #write data
      v[:] = np.float32(data.mole_frac)
   
   if len(data.mass_frac) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_molecular_hydrogen_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mass_fraction_of_molecular_hydrogen_in_air'
      v.long_name = 'Mass Fraction of Molecular Hydrogen in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'H2'
      #write data
      v[:] = np.float32(data.mass_frac)
   
   if len(data.mole_conc) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_molecular_hydrogen_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mole_concentration_of_molecular_hydrogen_in_air'
      v.long_name = 'Mole Concentration of Molecular Hydrogen in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'H2'
      #write data
      v[:] = np.float32(data.mole_conc)
   
   if len(data.mass_conc) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_molecular_hydrogen_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mass_concentration_of_molecular_hydrogen_in_air'
      v.long_name = 'Mass Concentration of Molecular Hydrogen in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'H2'
      #write data
      v[:] = np.float32(data.mass_conc)
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag)
   
 # I
 # J
 # K
 # L
 # M
 # N
def n2o_sf6_concentration(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   
   if len(data.mole_frac) == len(data.ET):
      # write specific variables
      v = nc.createVariable('mole_fraction_of_nitrous_oxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mole_fraction_of_nitrous_oxide_in_air'
      v.long_name = 'Mole Fraction of Nitrous Oxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'N2O'
      #write data
      v[:] = np.float32(data.mole_frac)
   
   if len(data.mass_frac) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_nitrous_oxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mass_fraction_of_nitrous_oxide_in_air'
      v.long_name = 'Mass Fraction of Nitrous Oxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'N2O'
      #write data
      v[:] = np.float32(data.mass_frac)
   
   if len(data.mole_conc) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_nitrous_oxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mole_concentration_of_nitrous_oxide_in_air'
      v.long_name = 'Mole Concentration of Nitrous Oxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'N2O'
      #write data
      v[:] = np.float32(data.mole_conc)
   
   if len(data.mass_conc) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_nitrous_oxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mass_concentration_of_nitrous_oxide_in_air'
      v.long_name = 'Mass Concentration of Nitrous Oxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'N2O'
      #write data
      v[:] = np.float32(data.mass_conc)
   
   if len(data.mole_frac1) == len(data.ET):
      v = nc.createVariable('mole_fraction_of_sulfur_hexafluoride_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.practical_units = data.practical_units1
      v.long_name = 'Mole Fraction of Sulphur Hexafluoride in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'SF6'
      #write data
      v[:] = np.float32(data.mole_frac1)
   
   if len(data.mass_frac1) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_sulfur_hexafluoride_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.practical_units = data.practical_units1
      v.long_name = 'Mass Fraction of Sulphur Hexafluoride in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'SF6'
      #write data
      v[:] = np.float32(data.mass_frac1)
   
   if len(data.mole_conc1) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_sulfur_hexafluoride_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.long_name = 'Mole Concentration of Sulphur Hexafluoride in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'SF6'
      #write data
      v[:] = np.float32(data.mole_conc1)
   
   if len(data.mass_conc1) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_sulfur_hexafluoride_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.long_name = 'Mass Concentration of Sulphur Hexafluoride in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'SF6'
      #write data
      v[:] = np.float32(data.mass_conc1)
   
   v = nc.createVariable('qc_flag_n2o', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: N2O'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_unspecified_instrument_performance_issues_contact_data_originator_for_more_information' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag)
   
   v = nc.createVariable('qc_flag_sf6', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: SF6'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_unspecified_instrument_performance_issues_contact_data_originator_for_more_information' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag1)
   
def no2_concentration(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   if len(data.mole_frac) == len(data.ET):
      v = nc.createVariable('mole_fraction_of_nitrogen_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mole_fraction_of_nitrogen_dioxide_in_air'
      v.long_name = 'Mole Fraction of Nitrogen Dioxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NO2'
      #write data
      v[:] = np.float32(data.mole_frac)
   
   if len(data.mass_frac) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_nitrogen_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mass_fraction_of_nitrogen_dioxide_in_air'
      v.long_name = 'Mass Fraction of Nitrogen Dioxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NO2'
      #write data
      v[:] = np.float32(data.mass_frac)
   
   if len(data.mole_conc) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_nitrogen_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mole_concentration_of_nitrogen_dioxide_in_air'
      v.long_name = 'Mole Concentration of Nitrogen Dioxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NO2'
      #write data
      v[:] = np.float32(data.mole_conc)
   
   if len(data.mass_conc) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_nitrogen_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mass_concentration_of_nitrogen_dioxide_in_air'
      v.long_name = 'Mass Concentration of Nitrogen Dioxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NO2'
      #write data
      v[:] = np.float32(data.mass_conc)
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_gas_concentration_outside_instrument_operational _range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp _error' 
   #write data
   v[:] = np.int8(data.flag)
         
def nox_noxy_concentration(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   if len(data.mole_frac1) == len(data.ET):
      v = nc.createVariable('mole_fraction_of_nitric_oxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.practical_units = data.practical_units1
      v.long_name = 'Mole Fraction of Nitric Oxide in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NO'
      #write data
      v[:] = np.float32(data.mole_frac1)
   
   if len(data.mass_frac1) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_nitric_oxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.practical_units = data.practical_units1
      v.long_name = 'Mass Fraction of Nitric Oxide in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NO'
      #write data
      v[:] = np.float32(data.mass_frac1)
   
   if len(data.mole_conc1) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_nitric_oxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.long_name = 'Mole Concentration of Nitric Oxide in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NO'
      #write data
      v[:] = np.float32(data.mole_conc1)
   
   if len(data.mass_conc1) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_nitric_oxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit1
      v.long_name = 'Mass Concentration of Nitric Oxide in air'
      v.valid_min = np.float32(data.min_dat1)
      v.valid_max = np.float32(data.max_dat1)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NO'
      #write data
      v[:] = np.float32(data.mass_conc1)  
   
   if len(data.mole_frac2) == len(data.ET):
      v = nc.createVariable('mole_fraction_of_nitrogen_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit2
      v.practical_units = data.practical_units2
      v.standard_name = 'mole_fraction_of_nitrogen_dioxide_in_air'
      v.long_name = 'Mole Fraction of Nitrogen Dioxide in air'
      v.valid_min = np.float32(data.min_dat2)
      v.valid_max = np.float32(data.max_dat2)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NO2'
      #write data
      v[:] = np.float32(data.mole_frac2)
   
   if len(data.mass_frac2) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_nitrogen_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit2
      v.practical_units = data.practical_units2
      v.standard_name = 'mass_fraction_of_nitrogen_dioxide_in_air'
      v.long_name = 'Mass Fraction of Nitrogen Dioxide in air'
      v.valid_min = np.float32(data.min_dat2)
      v.valid_max = np.float32(data.max_dat2)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NO2'
      #write data
      v[:] = np.float32(data.mass_frac2)
   
   if len(data.mole_conc2) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_nitrogen_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit2
      v.standard_name = 'mole_concentration_of_nitrogen_dioxide_in_air'
      v.long_name = 'Mole Concentration of Nitrogen Dioxide in air'
      v.valid_min = np.float32(data.min_dat2)
      v.valid_max = np.float32(data.max_dat2)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NO2'
      #write data
      v[:] = np.float32(data.mole_conc2)
   
   if len(data.mass_conc2) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_nitrogen_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit2
      v.standard_name = 'mass_concentration_of_nitrogen_dioxide_in_air'
      v.long_name = 'Mass Concentration of Nitrogen Dioxide in air'
      v.valid_min = np.float32(data.min_dat2)
      v.valid_max = np.float32(data.max_dat2)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NO2'
      #write data
      v[:] = np.float32(data.mass_conc2)
   
   if len(data.mole_frac3) == len(data.ET):
      v = nc.createVariable('mole_fraction_of_nox_expressed_as_nitrogen_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit3
      v.practical_units = data.practical_units3
      v.standard_name = 'mole_fraction_of_nox_expressed_as_nitrogen_in_air'
      v.long_name = 'Mole Fraction of NOx expressed as nitrogen in air'
      v.valid_min = np.float32(data.min_dat3)
      v.valid_max = np.float32(data.max_dat3)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NOx'
      #write data
      v[:] = np.float32(data.mole_frac3)
   
   if len(data.mass_frac3) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_nox_expressed_as_nitrogen_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit3
      v.practical_units = data.practical_units3
      v.standard_name = 'mass_fraction_of_nox_expressed_as_nitrogen_in_air' 
      v.long_name = 'Mass Fraction of NOx expressed as nitrogen in air'
      v.valid_min = np.float32(data.min_dat3)
      v.valid_max = np.float32(data.max_dat3)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NOx'
      #write data
      v[:] = np.float32(data.mass_frac3)
   
   if len(data.mole_conc3) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_nox_expressed_as_nitrogen_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit3
      v.standard_name = 'mole_concentration_of_nox_expressed_as_nitrogen_in_air'
      v.long_name = 'Mole Concentration of NOx expressed as nitrogen in air'
      v.valid_min = np.float32(data.min_dat3)
      v.valid_max = np.float32(data.max_dat3)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NOx'
      #write data
      v[:] = np.float32(data.mole_conc3)
   
   if len(data.mass_conc3) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_nox_expressed_as_nitrogen_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit3
      v.standard_name = 'mass_concentration_of_nox_expressed_as_nitrogen_in_air'
      v.long_name = 'Mass Concentration of NOx expressed as nitrogen in air'
      v.valid_min = np.float32(data.min_dat3)
      v.valid_max = np.float32(data.max_dat3)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'NOx'
      #write data
      v[:] = np.float32(data.mass_conc3)
   
   v = nc.createVariable('qc_flag_no', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: NO'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag1)
   
   v = nc.createVariable('qc_flag_no2', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: NO2'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag2)
   
   v = nc.createVariable('qc_flag_nox', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: NOx'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag3)
   
# O   
def o2n2_concentration_ratio(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('molecular_oxygen_molecular_nitrogen_ratio_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'per meg'
   v.long_name = 'O2/N2 ratio in air'
   v.valid_min = np.float32(data.min_dat)
   v.valid_max = np.float32(data.max_dat)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.O2N2)

   v = nc.createVariable('qc_flag', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_gas_concentration_outside_instrument_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag) 
         
def o3_concentration(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   if len(data.mole_frac) == len(data.ET):
      v = nc.createVariable('mole_fraction_of_ozone_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mole_fraction_of_ozone_in_air'
      v.long_name = 'Mole Fraction of Ozone in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'O3'
      #write data
      v[:] = np.float32(data.mole_frac)
   
   if len(data.mass_frac) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_ozone_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mass_fraction_of_ozone_in_air'
      v.long_name = 'Mass Fraction of Ozone in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'O3'
      #write data
      v[:] = np.float32(data.mass_frac)
   
   if len(data.mole_conc) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_ozone_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mole_concentration_of_ozone_in_air'
      v.long_name = 'Mole Concentration of Ozone in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'O3'
      #write data
      v[:] = np.float32(data.mole_conc)
   
   if len(data.mass_conc) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_ozone_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mass_concentration_of_ozone_in_air'
      v.long_name = 'Mass Concentration of Ozone in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'O3'
      #write data
      v[:] = np.float32(data.mass_conc)
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_unspecified_instrument_performance_issues_contact_data_originator_for_more_information' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag) 
   
# P
def pm_concentration(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('mass_concentration_of_pm1_ambient_aerosol_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'ug m-3'
   v.standard_name = 'mass_concentration_of_pm1_ambient_aerosol_in_air'
   v.long_name = 'Mass Concentration of PM1 Ambient Aerosol in Air'
   v.valid_min = np.float32(data.min_dat1)
   v.valid_max = np.float32(data.max_dat1)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.pm1)  
   
   v = nc.createVariable('mass_concentration_of_pm2p5_ambient_aerosol_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'ug m-3'
   v.standard_name = 'mass_concentration_of_pm2p5_ambient_aerosol_in_air'
   v.long_name = 'Mass Concentration of PM2.5 Ambient Aerosol in Air'
   v.valid_min = np.float32(data.min_dat2)
   v.valid_max = np.float32(data.max_dat2)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.pm25) 
   
   v = nc.createVariable('mass_concentration_of_pm4_ambient_aerosol_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'ug m-3'
   v.long_name = 'Mass Concentration of PM4 Ambient Aerosol in Air'
   v.valid_min = np.float32(data.min_dat3)
   v.valid_max = np.float32(data.max_dat3)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.pm4)
   
   v = nc.createVariable('mass_concentration_of_pm10_ambient_aerosol_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'ug m-3'
   v.standard_name = 'mass_concentration_of_pm10_ambient_aerosol_in_air'
   v.long_name = 'Mass Concentration of PM10 Ambient Aerosol in Air'
   v.valid_min = np.float32(data.min_dat4)
   v.valid_max = np.float32(data.max_dat4)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.pm10) 
   
   v = nc.createVariable('mass_concentration_of_total_pm_ambient_aerosol_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'ug m-3'
   v.long_name = 'Mass Concentration of Total PM Ambient Aerosol Particles in air'
   v.valid_min = np.float32(data.min_dat5)
   v.valid_max = np.float32(data.max_dat5)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.pc)
   
   v = nc.createVariable('number_concentration_of_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'cm-3'
   v.standard_name = 'number_concentration_of_ambient_aerosol_particles_in_air'
   v.long_name = 'Number Concentration of Ambient Aerosol Particles in air'
   v.valid_min = np.float32(data.min_dat6)
   v.valid_max = np.float32(data.max_dat6)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.tcp) 

   v = nc.createVariable('qc_flag_pm1', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: PM1'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_pm1_outside_sensor_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag1)
   
   v = nc.createVariable('qc_flag_pm2p5', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: PM2.5'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_pm2.5_outside_sensor_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag2)
   
   v = nc.createVariable('qc_flag_pm4', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: PM4'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_pm4_outside_sensor_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag3)
   
   v = nc.createVariable('qc_flag_pm10', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: PM10'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_pm10_outside_sensor_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag4)
   
   v = nc.createVariable('qc_flag_total_pm', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Total PM'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_total_pm_outside_sensor_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag5)
   
   v = nc.createVariable('qc_flag_total_number', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Total Number'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_total_number_outside_sensor_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag6)
   
# Q
# R
def radon_concentration(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   if len(data.mole_frac) == len(data.ET):
      v = nc.createVariable('mole_fraction_of_radon_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mole_fraction_of_radon_in_air'
      v.long_name = 'Mole Fraction of Radon in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'Ra'
      #write data
      v[:] = np.float32(mole_frac)
   
   if len(data.mass_frac) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_radon_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mass_fraction_of_radon_in_air'
      v.long_name = 'Mass Fraction of Radon in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'Ra'
      #write data
      v[:] = np.float32(data.mass_frac)
   
   if len(data.mole_conc) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_radon_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mole_concentration_of_radon_in_air'
      v.long_name = 'Mole Concentration of Radon in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'Ra'
      #write data
      v[:] = np.float32(data.mole_conc)
   
   if len(data.mass_conc) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_radon_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mass_concentration_of_radon_in_air'
      v.long_name = 'Mass Concentration of Radon in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'Ra'
      #write data
      v[:] = np.float32(data.mass_conc)
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_unspecified_instrument_performance_issues_contact_data_originator_for_more_information' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag)
   
# S
def sf6_concentration(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   if len(data.mole_frac) == len(data.ET):
      v = nc.createVariable('mole_fraction_of_sulfur_hexafluoride_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.long_name = 'Mole Fraction of Sulphur Hexafluoride in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'SF6'
      #write data
      v[:] = np.float32(data.mole_frac)
   
   if len(data.mass_frac) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_sulfur_hexafluoride_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.long_name = 'Mass Fraction of Sulphur Hexafluoride in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'SF6'
      #write data
      v[:] = np.float32(data.mass_frac)
   
   if len(data.mole_conc) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_sulfur_hexafluoride_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.long_name = 'Mole Concentration of Sulphur Hexafluoride in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'SF6'
      #write data
      v[:] = np.float32(data.mole_conc)
   
   if len(data.mass_conc) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_sulfur_hexafluoride_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.long_name = 'Mass Concentration of Sulphur Hexafluoride in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'SF6'
      #write data
      v[:] = np.float32(data.mass_conc)
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_unspecified_instrument_performance_issues_contact_data_originator_for_more_information' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag)
   
def so2_concentration(meta, data, nc, ver):
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   if len(data.mole_frac) == len(data.ET):
      v = nc.createVariable('mole_fraction_of_sulfur_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mole_fraction_of_sulfur_dioxide_in_air'
      v.long_name = 'Mole Fraction of Sulphur Dioxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'SO2'
      #write data
      v[:] = np.float32(data.mole_frac)
   
   if len(data.mass_frac) == len(data.ET):
      v = nc.createVariable('mass_fraction_of_sulfur_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.practical_units = data.practical_units
      v.standard_name = 'mass_fraction_of_sulfur_dioxide_in_air'
      v.long_name = 'Mass Fraction of Sulphur Dioxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'SO2'
      #write data
      v[:] = np.float32(data.mass_frac)
   
   if len(data.mole_conc) == len(data.ET):
      v = nc.createVariable('mole_concentration_of_sulfur_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mole_concentration_of_sulfur_dioxide_in_air'
      v.long_name = 'Mole Concentration of Sulphur Dioxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'SO2'
      #write data
      v[:] = np.float32(data.mole_conc)
   
   if len(data.mass_conc) == len(data.ET):
      v = nc.createVariable('mass_concentration_of_sulfur_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
      #variable attributes
      v.units = data.unit
      v.standard_name = 'mass_concentration_of_sulfur_dioxide_in_air'
      v.long_name = 'Mass Concentration of Sulphur Dioxide in air'
      v.valid_min = np.float32(data.min_dat)
      v.valid_max = np.float32(data.max_dat)
      v.cell_methods = 'time: point'
      v.coordinates = 'latitude longitude'
      v.chemical_species = 'SO2'
      #write data
      v[:] = np.float32(data.mass_conc)
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   qc_flags.flag_values = '0b,1b,2b,3b'
   qc_flags.flag_meanings = 'not_used' + '\n'
   qc_flags.flag_meanings = qc_flags.flag_meanings + 'good_data' + '\n'
   qc_flags.flag_meanings = qc_flags.flag_meanings + 'suspect_data_unspecified_instrument_performance_issues_contact_data_originator_for_more_information' + '\n'
   qc_flags.flag_meanings = qc_flags.flag_meanings + 'suspect_data_time_stamp_error'  
   #write data
   v[:] = np.int8(data.flag)

def surface_met1(meta, data, nc, ver):
   #campbell radiation only
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('downwelling_total_irradiance', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'W m-2'
   v.long_name = 'Downwelling Total Radiative Flux'
   v.valid_min = np.float32(data.min_dat3)
   v.valid_max = np.float32(data.max_dat3)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.IR)
   
   v = nc.createVariable('net_total_irradiance', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'W m-2'
   v.long_name = 'Net Downwelling Radiative Flux'
   v.valid_min = np.float32(data.min_dat4)
   v.valid_max = np.float32(data.max_dat4)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.NetIR)
   
   v = nc.createVariable('qc_flag_radiation', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Radiation'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data<0Wm-2' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_exceeds_instrument_measurment_range_of_2000Wm-2'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'
   #write data
   v[:] = np.int8(data.flag3)
   
def surface_met2(meta, data, nc, ver):
   #metpak
   import WAO_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('air_pressure', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'hPa'
   v.standard_name = 'air_pressure'
   v.long_name = 'Air Pressure'
   v.valid_min = np.float32(data.min_dat7)
   v.valid_max = np.float32(data.max_dat7)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.PP) 
   
   v = nc.createVariable('air_temperature', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'K'
   v.standard_name = 'air_temperature'
   v.long_name = 'Air Temperature'
   v.valid_min = np.float32(data.min_dat2)
   v.valid_max = np.float32(data.max_dat2)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.TT)
   
   v = nc.createVariable('relative_humidity', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = '%'
   v.standard_name = 'relative_humidity'
   v.long_name = 'Relative Humidity'
   v.valid_min = np.float32(data.min_dat1)
   v.valid_max = np.float32(data.max_dat1)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.RH)
   
   v = nc.createVariable('wind_speed', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.standard_name = 'wind_speed'
   v.long_name = 'Wind Speed'
   v.valid_min = np.float32(data.min_dat5)
   v.valid_max = np.float32(data.max_dat5)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.WS)
   
   v = nc.createVariable('wind_from_direction', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'degree'
   v.standard_name = 'wind_from_direction'
   v.long_name = 'Wind From Direction'
   v.valid_min = np.float32(data.min_dat6)
   v.valid_max = np.float32(data.max_dat6)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.WD)
   
   v = nc.createVariable('qc_flag_temperature', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Temperature'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_below_measurement_threshold_of_50C' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_above_measurement_threshold_of_100C' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:T<_-20C_and_T>-50C' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:T>_40C_and_T<100C' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag2)  
   
   v = nc.createVariable('qc_flag_relative_humidity', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Relative Humidity'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_below_measurement_threshold_of_0%' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_above_measurement_threshold_of_100%' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag1)
   
   v = nc.createVariable('qc_flag_pressure', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Pressure'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_below_measurement_threshold_of_600hPa' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_above_measurement_threshold_of_11000hPa' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag7)
   
   v = nc.createVariable('qc_flag_wind_speed', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Wind Speed'
   v.flag_values = '0b,1b,2b,3b,4b,5b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_below_measurement_threshold_of_0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_above_measurement_threshold_of_60ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:data=0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag5)
   
   v = nc.createVariable('qc_flag_wind_from_direction', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Wind From Direction'
   v.flag_values = '0b,1b,2b,3b,4b,5b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_below_measurement_threshold_of_0degrees' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_above_measurement_threshold_of_359degrees' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:windspeed=0ms-1_so_direction_cannot_be_determined' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag6)  