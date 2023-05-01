import os
import csv
# pdk and results dir

RUN_DIR = "/home/local/nu/shg/tiny_aes/tiny_aes_builds/runs_2/"
POWER_REPORT_DIR = "/report"
OUTPUT_CSV = "out_maxfreq_aes128_200.csv"


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


pdk_reports = {

}

for corner in SELECT_CORNERS:
    for pdk_set in LIBRARIES[corner]:
        pdk_reports[pdk_set[0]] = RUN_DIR+"run_p"+pdk_set[0]+"/"+"p"+pdk_set[0]+POWER_REPORT_DIR



print(pdk_reports)


# Report file name mappings
power_log_mappings = {
    "power_groups":"pwr_group.rpt"
}
synth_log_mappings = {
    "area_report":"area.rpt",
    "synth_power_report":"reportpower.rpt",
    "timing_report":"reporttimingmaxpaths.rpt",
}

def extract_pdk_info(pdk):
    #GF22FDX_6P75T_104CPP_FFG_0P88V_0P00V_0P00V_0P00V_M40C
    _i = pdk.split("_")
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

def synthesis_runs_extract(paths):
    for path in paths:
        targets = os.listdir(path)
        for target in targets:
           # for file in os.listdir(os.path.join(os.path.relpath(target),"log"))
                pass


def power_runs_extract(pdk_reports):
    
    pdk_info_empty = {
        "corner":"",
        "supply_voltage":"",
        "nfet_bias":"",
        "pfet_bias":"",
        "temperature":""
    }
    power_data_empty = {'Net Switching Power': "",
            'Cell Internal Power': "",
            'Cell Leakage Power': "",
            'Total Power': "",
            'Peak Power': "",
            'Peak Time': ""}
    
    empty = {}
    empty.update(pdk_info_empty)
    empty.update(power_data_empty)
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=empty.keys())
        writer.writeheader()

    for key,value in pdk_reports.items():
        if os.path.isdir(value):
            print("Extracting info for run",value)
            for file in os.listdir(value):
                if file==power_log_mappings.get("power_groups"):
                    net_switching_power = ''
                    cell_internal_power = ''
                    cell_leakage_power = ''
                    total_power = ''
                    peak_power = ''
                    peak_time = ''
                    with open(os.path.join(value,file),'r') as f:

                        for line in f:
                            if 'Net Switching Power' in line:
                                net_switching_power = line.split('=')[1].strip().split(" ")[0]
                            elif 'Cell Internal Power' in line:
                                cell_internal_power = line.split('=')[1].strip().split(" ")[0]
                            elif 'Cell Leakage Power' in line:
                                cell_leakage_power = line.split('=')[1].strip().split(" ")[0]
                            elif 'Total Power' in line:
                                total_power = line.split('=')[1].strip().split(" ")[0]
                            elif 'Peak Power' in line:
                                peak_power = line.split('=')[1].strip().split(" ")[0]
                                peak_time = line.split('=')[1].strip().split(" ")[0]
                            print("File found")
                
                    power_data = {'Net Switching Power': net_switching_power,
                        'Cell Internal Power': cell_internal_power,
                        'Cell Leakage Power': cell_leakage_power,
                        'Total Power': total_power,
                        'Peak Power': peak_power,
                        'Peak Time': peak_time}

                    pdk_data = extract_pdk_info(key)
                    data = {}
                    data.update(pdk_data)
                    data.update(power_data)
                    with open(OUTPUT_CSV, 'a', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=data.keys())
                        writer.writerow(data)
                     #print(os.listdir(path))



if __name__ == "__main__":
    #synthesis_runs_extract(["/home/unga/shg/work/cores/cv32e40p/runs_200mhz",])
    #print(pdk_reports)
    power_runs_extract(pdk_reports)
    #extract_pdk_info("GF22FDX_6P75T_104CPP_FFG_0P88V_0P00V_0P00V_0P00V_M40C")
#
    #extract_pdk_info("GF22FDX_6P75T_104CPP_FFG_0P72V_0P00V_0P00V_0P00V_125C")  
    #extract_pdk_info("GF22FDX_6P75T_104CPP_FFG_0P72V_0P00V_0P00V_0P00V_M40C")
    #extract_pdk_info("GF22FDX_6P75T_104CPP_FFG_0P88V_0P00V_0P00V_0P00V_125C")
    #extract_pdk_info("GF22FDX_6P75T_104CPP_FFG_0P88V_0P00V_0P00V_0P00V_M40C")
    #extract_pdk_info("GF22FDX_6P75T_104CPP_SSG_0P59V_0P00V_0P00V_0P00V_125C")
    #extract_pdk_info("GF22FDX_6P75T_104CPP_SSG_0P59V_0P00V_0P00V_0P00V_M40C")
    #extract_pdk_info("GF22FDX_6P75T_104CPP_SSG_0P59V_0P00V_0P60V_M0P80V_125C")
    #extract_pdk_info("GF22FDX_6P75T_104CPP_SSG_0P59V_0P00V_0P85V_M1P50V_M40C")
    #extract_pdk_info("GF22FDX_6P75T_104CPP_SSG_0P72V_0P00V_0P00V_0P00V_125C")
    #extract_pdk_info("GF22FDX_6P75T_104CPP_SSG_0P72V_0P00V_0P00V_0P00V_M40C")
    #extract_pdk_info("GF22FDX_6P75T_104CPP_SSG_0P72V_0P00V_0P60V_M1P00V_125C")
    #extract_pdk_info("GF22FDX_6P75T_104CPP_TT_0P65V_0P00V_0P00V_M0P20V_25C")
    #extract_pdk_info("GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P00V_0P00V_25C")
