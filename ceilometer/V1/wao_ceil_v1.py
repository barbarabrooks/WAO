# args exected
#1. input directory 
#2. output diretory 

import sys
import os
import numpy as np
from collections import namedtuple
from wao_ceil_parser_v1 import get_file_v1, parse_time_v1, parse_block_v1
from wao_ceil_parser_v1 import parse_line1_v1, parse_line2_v1, parse_line3_v1, parse_BB_v1
from wao_ceil_QC_v1 import QC_BB_v1, QC_BB_noise_v1, QC_CBH_v1, tidy_data_v1 
from wao_ceil_plot_v1 import data_means_v1, data_plot_v1


data = namedtuple("data", "DT DoY ET UN SWL MS BB ZZ BB_flag CBH_flag DETS WRN CBH1 CBH2 CBH3 CFLAG SC MM LPE LT RS WC TA BL MP SS") 
data_out = namedtuple("data_out", "DT DoY ET BB ZZ CBH BB_FLAG CBH_FLAG")
data_plt = namedtuple("data_plt", "DT DoY ET BB ZZ CBH")
lines = []
din = str(sys.argv[1]) #input directory
dout = str(sys.argv[2]) #output directory

infiles = os.listdir(din) #list of file in input directory

#read all file in directory
for ii in range(0,len(infiles)):
   lines = get_file_v1((din + infiles[ii]), lines)
   
#parse the data           
start_of_block = parse_block_v1(lines)
data = parse_time_v1(lines, start_of_block, np, data)  # time
data = parse_line1_v1(lines, start_of_block, np, data) # housekeeping 1
data = parse_line2_v1(lines, start_of_block, np, data) # cloudbase height
data = parse_line3_v1(lines, start_of_block, np, data) # housekeeping 2
data = parse_BB_v1(lines, start_of_block, np, data)    # backscatter profile

#QC data
data = QC_BB_v1(data, np)
data = QC_BB_noise_v1(data)
data = QC_CBH_v1(data, np)

# tidy up data
data_out = tidy_data_v1(data, data_out, np)

#create 5 min average for plotting plt and save image
data_plt = data_means_v1(data_out, data_plt, np)
plot_data = data_plot_v1(data_plt, np, dout) 


