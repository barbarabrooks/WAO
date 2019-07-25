# args exected
#1. full path to file to be converted
#2. output diretory 
#3. path to meta file

import sys
#import os
import numpy as np
from collections import namedtuple
from wao_co2_parser_v1 import wao_co2_get_file_v1, wao_co2_parse_data_v1
from wao_co2_NC_v1 import wao_co2_get_meta_v1, NC_wao_co2_v1

data = namedtuple("data", "DT DoY ET CO2 flag")
fin = str(sys.argv[1])
dout = str(sys.argv[2])
fn_meta = str(sys.argv[3])

#get the data
data.DT, data.DoY, data.ET, data.CO2, data.flag = wao_co2_get_file_v1(fin, np)

#parse data - make sure just one month of data
data.DT, data.DoY, data.ET, data.CO2, data.flag = wao_co2_parse_data_v1(data)

#save nc file
meta = wao_co2_get_meta_v1(fn_meta)
NC_wao_co2_v1(meta, dout, data, np)

