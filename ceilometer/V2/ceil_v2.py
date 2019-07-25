#Python 3 code to parse wao cceilometer data 
# args expected
#1. input directory 
#2. output diretory 
#3. path to meta file

import sys
import os
import numpy as np
import pandas as pd
np.warnings.simplefilter(action='ignore', category=FutureWarning)
from collections import namedtuple
import ceil_parser_v2 as onp
import ceil_QC_v2 as qc
import ceil_plot_v2 as cplt
import ceil_NC_v2 as nc

data_raw = namedtuple("data_raw", "")
data_QC = namedtuple("data_QC", "")

din = str(sys.argv[1]) #input directory
dout = str(sys.argv[2]) #output directory
fn_meta_bck = str(sys.argv[3]) # backscatter meta file
fn_meta_cbh = str(sys.argv[4]) # cloud-base meta file

infiles = os.listdir(din) #list of file in input directory
   
#parse the data  
data_raw = onp.ceil_parse_v2(din, infiles, np, data_raw)      

#QC data
data_QC = qc.QC_data_v2(data_raw, np, data_QC)

#plot and save image
#cplt.quick_look_plt_v2(data_QC, np, dout)

#Meta data
meta_bck = pd.read_excel(fn_meta_bck)
meta_cbh = pd.read_excel(fn_meta_cbh)

#save nc file
nc.NC_ceil_v2(pd, np, dout, meta_bck, meta_cbh, data_QC)