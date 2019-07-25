#Python 3 code to parse wao h2 concentration data 
# args exected
#1. full path to file to be converted
#2. output diretory 
#3. path to meta file

import sys
from collections import namedtuple
import pandas as pd
import numpy as np
import coh2_post2017_parser_v2 as onp
import coh2_post2017_NC_v2 as nc

data = namedtuple("data", "DT DoY ET h2 flag")

# Read in command line arguments
fin = str(sys.argv[1])
dout = str(sys.argv[2])
fn_meta = str(sys.argv[3])

# Data
df = pd.read_csv(fin)
data = onp.parse_time_v2(pd, np, df, data)
data = onp.parse_data_v2(pd, np, df, data)

#Meta data
meta = pd.read_excel(fn_meta)

#save nc file
nc.NC_coh2_post2017_v2(pd, np, dout, meta, data)