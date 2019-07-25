#Python 3 code to parse wao met data 
# args exected
#1. full path to file to be converted
#2. output diretory 
#3. path to meta file

import sys
from collections import namedtuple
import pandas as pd
import numpy as np
import met_parser_v2 as onp
import met_NC_v2 as nc

data = namedtuple("data", "")

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
nc.NC_met_v2(pd, np, dout, meta, data)