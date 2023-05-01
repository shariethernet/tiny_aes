import os
from jinja2 import Environment, FileSystemLoader
import re
import shutil
import csv
# Set to True when you need to eval the max freq and write the SDC files
# Eval Max Freq True, Run Make False - Just generates the core and the makefiles
# Eval Max Freq True, Run Make True - Generates core and makefiles, synth for max freq and generates sdcs and csv
# Eval Max Freq True, Run Make False - Generates core and makefiles for max freq
# Eval Max Freq True, Run Make True - Generates core and makefiles for max freq, and runs make with selected synth or power target
EVAL_MAX_FREQ = False
SDC_WRITE_PATH = "/home/local/nu/shg/cv32e40p_builds/sdc/"

# VARIABLES
RUN_MAKE = False
COREFILENAME = "aes.core"
MAKEFILENAME = "Makefile_gen"
FREQ_CSV = "max_freq.csv"

MAKE_RUN_DIR =  "/home/local/nu/shg/tiny_aes/tiny_aes_builds/runs_2/"

if EVAL_MAX_FREQ is True:
  MAKE_RUN_DIR = "/home/local/nu/shg/tiny_aes/tiny_aes_builds/runs_max_freq_1/"
  
if os.path.exists(MAKE_RUN_DIR):
  try:
    shutil.rmtree(MAKE_RUN_DIR)
  except OSError as E:
    print("Error removing the {} directory".format(MAKE_RUN_DIR))

#Select Makefile Flow
# When selected True, only synthesis is performed, if false synth and power analysis is performed
# However, Makefile and core files will have all the targets. This just sets the SELECT_TARGET variable in the Makefile
Synth_only = False

# List the corners to synthesize and do power sims
SELECT_CORNERS = ["TT_v10",]
#SELECT_CORNERS = ["FFG","SSG","TT"]

#  Absolute Path variables to db folder
PATH_new = "/home/local/nu/shg/pdk/lib/GF22FDX_6P75T_104CPP/rel_04182023_GF22FDX_6P75T_104CPP_0v09_ut/GF22FDX_6P75T_104CPP/0v09_ut/timing/db"
PATH_old = "/home/local/nu/shg/pdk/lib/GF22FDX_6P75T_104CPP/rel_03162023_GF22FDX_6P75T_104CPP_0v08_1_ut/GF22FDX_6P75T_104CPP/0v08_1_ut/timing/ccs_db"
PATH_v10 = "/usr/local/packages/ip/gerstl-gf/lib/GF22FDX_6P75T_104CPP/rel_04252023_GF22FDX_6P75T_104CPP_0v10_ut/GF22FDX_6P75T_104CPP/0v10_ut/db"

#path to verilog folder
verilog_PATH_new = "/home/local/nu/shg/pdk/lib/GF22FDX_6P75T_104CPP/rel_04182023_GF22FDX_6P75T_104CPP_0v09_ut/GF22FDX_6P75T_104CPP/0v09_ut/verilog"
verilog_PATH_old = "/home/local/nu/shg/pdk/lib/GF22FDX_6P75T_104CPP/rel_03162023_GF22FDX_6P75T_104CPP_0v08_1_ut/GF22FDX_6P75T_104CPP/0v08_1_ut/verilog"
verilog_PATH_v10 = "/usr/local/packages/ip/gerstl-gf/lib/GF22FDX_6P75T_104CPP/rel_04252023_GF22FDX_6P75T_104CPP_0v10_ut/GF22FDX_6P75T_104CPP/0v10_ut/verilog"

PATH_primepower_script_dir = "/home/local/nu/shg/tiny_aes/constraints"
PATH_default_constraints_dir = "/home/local/nu/shg/tiny_aes/constraints"
PATH_generated_constraints_dir = "/home/local/nu/shg/tiny_aes/constraints/generated"
PATH_eval_max_freq_dir = "/home/local/nu/shg/tiny_aes/constraints/max_freq_eval"
# Libraries according to their corners - (Names, db abs paths, verilog model abs paths)
LIBRARIES = {
            "FFG":
            [
            ("GF22FDX_6P75T_104CPP_FFG_0P88V_0P00V_0P00V_0P00V_M40C",PATH_old,verilog_PATH_old),
		   	("GF22FDX_6P75T_104CPP_FFG_0P88V_0P00V_0P00V_0P00V_125C",PATH_old,verilog_PATH_old),
		   	("GF22FDX_6P75T_104CPP_FFG_0P72V_0P00V_0P00V_0P00V_M40C",PATH_old,verilog_PATH_old),
			("GF22FDX_6P75T_104CPP_FFG_0P72V_0P00V_0P00V_0P00V_125C",PATH_old,verilog_PATH_old),
            ],
            "SSG":
            [
			("GF22FDX_6P75T_104CPP_SSG_0P59V_0P00V_0P00V_0P00V_125C",PATH_old,verilog_PATH_old), 
			("GF22FDX_6P75T_104CPP_SSG_0P59V_0P00V_0P00V_0P00V_M40C",PATH_old,verilog_PATH_old), 
			("GF22FDX_6P75T_104CPP_SSG_0P59V_0P00V_0P60V_M0P80V_125C",PATH_old,verilog_PATH_old),
			("GF22FDX_6P75T_104CPP_SSG_0P59V_0P00V_0P85V_M1P50V_M40C",PATH_old,verilog_PATH_old),
			("GF22FDX_6P75T_104CPP_SSG_0P72V_0P00V_0P00V_0P00V_125C",PATH_old,verilog_PATH_old),
			("GF22FDX_6P75T_104CPP_SSG_0P72V_0P00V_0P00V_0P00V_M40C",PATH_old,verilog_PATH_old),
			("GF22FDX_6P75T_104CPP_SSG_0P72V_0P00V_0P60V_M1P00V_125C",PATH_old,verilog_PATH_old),
            ],
            "TT_old":[
   			("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P00V_M0P20V_25C",PATH_old,verilog_PATH_old),
			("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P00V_0P00V_25C",PATH_old,verilog_PATH_old),
            ],
            "TT":
            [
            ("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_0P00V_0P00V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_0P00V_M0P25V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_0P25V_0P00V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_0P00V_0P00V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_0P00V_M0P25V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_0P25V_0P00V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_0P00V_0P00V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_0P00V_M0P25V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_0P25V_0P00V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_0P25V_M0P25V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P00V_0P00V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P00V_M0P25V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P25V_0P00V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P25V_M0P25V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_0P00V_0P00V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_0P00V_M0P25V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_0P25V_0P00V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_0P25V_M0P25V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_0P00V_0P00V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_0P00V_M0P25V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_0P25V_0P00V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_0P25V_M0P25V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P00V_0P00V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P00V_M0P25V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P25V_0P00V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P25V_M0P25V_25C",PATH_new,verilog_PATH_new),
            ],
            "TEST":[
			("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P00V_M0P25V_25C",PATH_new,verilog_PATH_new),
			("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P25V_0P00V_25C",PATH_new,verilog_PATH_new),
			#("GF22FDX6P75T_104CPP_TT_0P80V_0P00V_0P25V_M0P25V_25C",PATH_new,verilog_PATH_new),                   
            ],
            "TT_v10":[
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_0P00V_0P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_0P00V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_0P25V_0P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_0P25V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_0P25V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_0P5V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_0P5V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_0P5V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_0P75V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_0P75V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_0P75V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_1P00V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_1P00V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_1P00V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_1P25V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_1P25V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_1P25V_M1P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_1P5V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P50V_0P00V_1P5V_M1P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_0P00V_0P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_0P00V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_0P25V_0P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_0P25V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_0P25V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_0P5V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_0P5V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_0P5V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_0P75V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_0P75V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_0P75V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_1P00V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_1P00V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_1P00V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_1P25V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_1P25V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_1P25V_M1P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_1P5V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P55V_0P00V_1P5V_M1P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_0P00V_0P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_0P00V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_0P25V_0P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_0P25V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_0P25V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_0P5V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_0P5V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_0P5V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_0P75V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_0P75V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_0P75V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_1P00V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_1P00V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_1P00V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_1P25V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_1P25V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_1P25V_M1P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_1P5V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P60V_0P00V_1P5V_M1P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P00V_0P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P00V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P25V_0P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P25V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P25V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P5V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P5V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P5V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P75V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P75V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P75V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_1P00V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_1P00V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_1P00V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_1P25V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_1P25V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_1P25V_M1P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_1P5V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_1P5V_M1P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_0P00V_0P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_0P00V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_0P25V_0P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_0P25V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_0P25V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_0P5V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_0P5V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_0P5V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_0P75V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_0P75V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_0P75V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_1P00V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_1P00V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_1P00V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_1P25V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_1P25V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_1P25V_M1P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_1P5V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P70V_0P00V_1P5V_M1P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_0P00V_0P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_0P00V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_0P25V_0P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_0P25V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_0P25V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_0P5V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_0P5V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_0P5V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_0P75V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_0P75V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_0P75V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_1P00V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_1P00V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_1P00V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_1P25V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_1P25V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_1P25V_M1P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_1P5V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P75V_0P00V_1P5V_M1P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P00V_0P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P00V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P25V_0P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P25V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P25V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P5V_M0P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P5V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P5V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P75V_M0P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P75V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P75V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_1P00V_M0P75V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_1P00V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_1P00V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_1P25V_M1P00V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_1P25V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_1P25V_M1P5V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_1P5V_M1P25V_25C",PATH_v10,verilog_PATH_v10),
("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_1P5V_M1P5V_25C",PATH_v10,verilog_PATH_v10),
]
}


# TEMPLATES
COREHEADER = """\
CAPI=2:
name : ::aes:0

"""
COREFILESETS = """\
filesets:    
    libs:
        files:
            - rtl/round.v
            - rtl/table.v
        file_type: verilogSource

    rtl_aes_128:
        files:
            - rtl/aes_128.v
        file_type: verilogSource
    
    gate_level_128:
        files:
            - /home/local/nu/shg/tiny_aes/runs/run_synth/synth-design_compiler/netlist/aes_128.v
            - /home/local/nu/shg/pdk/lib/GF22FDX_6P75T_104CPP/rel_04182023_GF22FDX_6P75T_104CPP_0v09_ut/GF22FDX_6P75T_104CPP/0v09_ut/verilog/GF22FDX6P75T_104CPP.all.v
        file_type: verilogSource

    rtl_aes_192:
        files:
            - rtl/aes_192.v
        file_type: verilogSource

    rtl_aes_256:
        files:
            - rtl/aes_256.v
        file_type: verilogSource

    tb_aes_128:
        files:
            - testbench/test_aes_128.v
        file_type: verilogSource
    
    tb_aes_128_extended:
        files:
            - testbench/test_aes_128_extended.v
        file_type: verilogSource
        
    tb_aes_192:
        files:
            - testbench/test_aes_192.v
        file_type: verilogSource

    tb_aes_256:
        files:
            - testbench/test_aes_256.v
        file_type: verilogSource

    waves_rtl:
        files:
            - /home/local/nu/shg/tiny_aes/runs_e/run_sim/sim-vcs/wave_dump_rtl.vcd
        file_type: vcd

    waves_gate:
        files:
            - /home/local/nu/shg/tiny_aes/runs_e/run_gate_sim/gate_sim-vcs/wave_dump_gls.vcd
        file_type: vcd
"""

CORETARGET_HEADER= """\
targets:
"""

CORETARGET_SYNTH="""\
  {lib}:
      default_tool : design_compiler
      filesets: [rtl_aes_128,libs]
      toplevel : [aes_128]
      tools:
        design_compiler: 
          script_dir: "{dc_script_dir_path}"
          dc_script:  "synth_128.tcl"
          report_dir: "report"
          jobs: 1
          target_library: "{target_library_path}"
          libs: "{lib_path}"
"""

CORETARGET_SYNTH_POW="""\
  p{lib}:
      filesets: [rtl_aes_128,libs,waves_gate]
      toplevel : [aes_128]
      flow: dc_pp
      flow_options:
          script_dir: "{dc_script_dir_path}"
          dc_script:  "synth_128.tcl"
          report_dir: "report"
          jobs: 1
          target_library: "{target_library_path}"
          libs: "{lib_path}"
          mode: "time_based"
          pp_script_dir: "{pp_script_dir_path}"
          lib_dir: "{lib_dir_path}"
          verilog_dir: "{verilog_dir_path}"
          pp_script: "pp_gls.tcl"
          vcd_strip_path: "test_aes_128/uut"
          netlistpath: "netlist"
          netlistname: "aes_128"
          indir_source: "true"
"""  
def generate_synth_targets(f):
    for corner in SELECT_CORNERS:
        for pdk_set in LIBRARIES[corner]:
            if EVAL_MAX_FREQ is False:
                _c_path = "c_"+pdk_set[0]
                f.write(CORETARGET_SYNTH.format(
                    lib = pdk_set[0],
                    dc_script_dir_path = os.path.join(PATH_generated_constraints_dir,_c_path),
                    target_library_path = os.path.join(pdk_set[1],pdk_set[0])+".db",
                    lib_path = os.path.join(pdk_set[1],pdk_set[0])+".db",
                ))
            else:
                f.write(CORETARGET_SYNTH.format(
                    lib = pdk_set[0],
                    dc_script_dir_path = PATH_eval_max_freq_dir,
                    target_library_path = os.path.join(pdk_set[1],pdk_set[0])+".db",
                    lib_path = os.path.join(pdk_set[1],pdk_set[0])+".db",
                ))

def generate_synth_pow_targets(f):
    for corner in SELECT_CORNERS:
        for pdk_set in LIBRARIES[corner]:
            _c_path = "c_"+pdk_set[0]
            f.write(CORETARGET_SYNTH_POW.format(
                lib = pdk_set[0],
                dc_script_dir_path = os.path.join(PATH_generated_constraints_dir,_c_path),
                target_library_path = os.path.join(pdk_set[1],pdk_set[0])+".db",
                lib_path = os.path.join(pdk_set[1],pdk_set[0])+".db",
                lib_dir_path= pdk_set[1],
                pp_script_dir_path = PATH_primepower_script_dir,
                verilog_dir_path = pdk_set[2],     
            ))


def render_template(template_file_name, template_file_dir, target_file_name, target_file_dir, template_vars={}):
    jinja_env = Environment(
            loader= FileSystemLoader(template_file_dir),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
    template = jinja_env.get_template(template_file_name)
    file_path = os.path.join(target_file_dir, target_file_name)
    with open(file_path, "w") as f:
        f.write(template.render(template_vars))

def extract_pdk_info(pdk):
    #GF22FDX_6P75T_104CPP_FFG_0P88V_0P00V_0P00V_0P00V_M40C
    _i = pdk.split("_")
    print("i ",_i )
    corner = _i[3]
    supply_voltage = _i[4].replace("P",".").replace("V","")
    nfet_bias = _i[6].replace("P",".").replace("V","").replace("M","-")
    pfet_bias = _i[7].replace("P",".").replace("V","").replace("M","-")
    temperature = _i[8]

    pdk_info = {
        "corner":corner,
        "supply_voltage":supply_voltage,
        "nfet_bias":nfet_bias,
        "pfet_bias":pfet_bias,
        "temperature":temperature
    }
    print(pdk_info)
    return pdk_info

min_clk_period_list = []
def eval_min_clk_period():
    for dirpath, dirnames, filenames in os.walk(MAKE_RUN_DIR):
      for filename in filenames:
        if filename == "reporttimingmaxpaths.rpt":
          print("found timing report file",filename,dirpath)
          
          with open(os.path.join(dirpath,filename),'r') as f:
            #pdk_name = dirpath.split("/")
            pattern = r"GF22FDX[\w_\-\.]*"
            match = re.search(pattern, dirpath)
            if match:
              pdk_name = match.group(0)
            _slacks = []
            for line in f:
              if 'slack (VIOLATED)' in line:
                _slacks.append(abs(float(line.split(" ")[-1])))
            if len(_slacks) > 0:
              min_clk_period = max(_slacks)
              min_clk_period_list.append((pdk_name,min_clk_period))
    print(min_clk_period_list)

def write_max_freq_csv(in_tuple):
  pdk_info_empty = {
        "corner":"",
        "supply_voltage":"",
        "nfet_bias":"",
        "pfet_bias":"",
        "temperature":""
    }
  clk_period_empty = {'Clock Period (ns)': "",
                      'Frequency (Mhz)': "",
  }
    
  empty = {}
  empty.update(pdk_info_empty)
  empty.update(clk_period_empty)
  with open(FREQ_CSV, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=empty.keys())
    writer.writeheader()
  
  for i in in_tuple:
    data = {}
    pdk,min_clk_period = i[0], i[1]
    pdk_data = extract_pdk_info(pdk)

    max_freq = (1/(i[1]))*(10**3)
    clk_period_data = {'Clock Period (ns)': i[1],
            'Frequency (Mhz)': max_freq ,
    }
    data.update(pdk_data)
    data.update(clk_period_data)
    with open(FREQ_CSV, 'a', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=data.keys())
                        writer.writerow(data)


def generate_corefile():
    with open(COREFILENAME,'w') as f:
        f.write(COREHEADER)
        f.write(COREFILESETS)
        f.write(CORETARGET_HEADER)
        generate_synth_targets(f)
        generate_synth_pow_targets(f)

MAKEFILE_BODY="""\
all: $(SELECTED_TARGETS)

$(SELECTED_TARGETS):
	fusesoc run --target=$@ --build-root=$(addprefix $(RUN_DIR),$(addprefix run_,$@)) aes

.PHONY: run

run:
	fusesoc run --target=$(CURRENT_TARGET) --build-root=$(addprefix $(RUN_DIR),$(addprefix run_,$(CURRENT_TARGET))) aes
"""

MAKEFILE_TARGETS1="""\
TARGETS := {_targets}  
"""

MAKEFILE_TARGETS2="""\
SP_TARGETS := {_sptargets}
"""

MAKEFILE_RUNDIR="""\
RUN_DIR := {_run_dir}
"""
def make_targets_1():
    targets_list = []
    for corner in SELECT_CORNERS:
        for pdk_set in LIBRARIES[corner]:
            targets_list.append(pdk_set[0])
    targets_string = "\n".join(targets_list)
    targets_string = targets_string.replace("\n", "\\\n\t\t", len(targets_list)-1)
    return targets_string

def make_targets_2():
    targets_list = []
    for corner in SELECT_CORNERS:
        for pdk_set in LIBRARIES[corner]:
            targets_list.append("p"+pdk_set[0])
    targets_string = "\n".join(targets_list)
    targets_string = targets_string.replace("\n", "\\\n\t\t", len(targets_list)-1)
    return targets_string

def generate_makefile():
    with open(MAKEFILENAME,'w') as f:
        f.write(MAKEFILE_TARGETS1.format(_targets=make_targets_1()))
        f.write("\n")
        f.write(MAKEFILE_TARGETS2.format(_sptargets=make_targets_2()))
        f.write("\n")    
        if Synth_only is True:
            f.write("SELECTED_TARGETS := $(TARGETS)")
        else:
            f.write("SELECTED_TARGETS := $(SP_TARGETS)")
        f.write("\n")
        f.write(MAKEFILE_RUNDIR.format(_run_dir=MAKE_RUN_DIR))
        f.write("\n")
        f.write(MAKEFILE_BODY)

if __name__ == "__main__":
  #'''
    generate_corefile()
    generate_makefile()
    if RUN_MAKE is True:
      os.system(f"make -f {MAKEFILENAME} -j16 all")
    template_file_name = "constraints_128.sdc.j2"
    template2_file_name = "synth_128.tcl.j2"
    template_file_dir = "/home/local/nu/shg/tiny_aes/constraints/templates"
    template2_file_dir = template_file_dir
    target_file_name = "constraints_128.sdc"
    target2_file_name = "synth_128.tcl"
    target_file_dir_parent = "/home/local/nu/shg/tiny_aes/constraints/generated" 
    target2_file_dir_parent = target_file_dir_parent
    template_vars = {
        "clock_period":0.6,
    }
    template2_vars = {
      "constraints_path": ""
    }
    #render_template(template_file_name, template_file_dir, target_file_name, target_file_dir, template_vars)
    if EVAL_MAX_FREQ is True and RUN_MAKE is True:
      eval_min_clk_period()
      if len(min_clk_period_list) == 0:
        raise Exception("The min clock period list is empty. Check")
      else:
        write_max_freq_csv(min_clk_period_list)
        for i in min_clk_period_list:
          target_file_dir = os.path.join(target_file_dir_parent,"c_"+i[0])
          if not os.path.exists(target_file_dir):
            os.makedirs(target_file_dir)
          template_vars["clock_period"] = i[1]
          template2_vars["constraints_path"] = target_file_dir+"/constraints_128.sdc"
          render_template(template_file_name, template_file_dir,target_file_name,target_file_dir,template_vars)
          render_template(template2_file_name, template2_file_dir,target2_file_name,target_file_dir,template2_vars)
  #'''
