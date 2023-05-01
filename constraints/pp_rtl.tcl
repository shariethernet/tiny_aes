# write_activity_waveforms -vcd /home/unga/shg/work/edalize_primepower_example/wave/wave_dump.vcd -output wvfrm_1_new.out \
#  -interval 5 -peak_window 30 -hierarchical_levels 2
# report_activity_waveforms

#set lib_dir "/usr/local/packages/ip/gerstl-gf/lib/GF22FDX_6P75T_104CPP/rel_03162023_GF22FDX_6P75T_104CPP_0v08_1_ut/GF22FDX_6P75T_104CPP/0v08_1_ut/timing/ccs_db"
# set std_library "GF22FDX_6P75T_104CPP_FFG_0P88V_0P00V_0P00V_0P00V_M40C.db"
# set target_library "GF22FDX_6P75T_104CPP_FFG_0P88V_0P00V_0P00V_0P00V_M40C.db"
# set search_path "/usr/local/packages/ip/gerstl-gf/lib/GF22FDX_6P75T_104CPP/rel_03162023_GF22FDX_6P75T_104CPP_0v08_1_ut/GF22FDX_6P75T_104CPP/0v08_1_ut/verilog \
#                  /usr/local/packages/ip/gerstl-gf/lib/GF22FDX_6P75T_104CPP/rel_03162023_GF22FDX_6P75T_104CPP_0v08_1_ut/GF22FDX_6P75T_104CPP/0v08_1_ut/timing/ccs_db \
#                  /home/unga/shg/work/pwr_gf_tt"
# set link_path [concat * $std_library]

#read_verilog cv32e40p.v
#set search_path [concat * "/usr/local/packages/ip/gerstl-gf/lib/GF22FDX_6P75T_104CPP/rel_03162023_GF22FDX_6P75T_104CPP_0v08_1_ut/GF22FDX_6P75T_104CPP/0v08_1_ut/verilog \
#                 /usr/local/packages/ip/gerstl-gf/lib/GF22FDX_6P75T_104CPP/rel_03162023_GF22FDX_6P75T_104CPP_0v08_1_ut/GF22FDX_6P75T_104CPP/0v08_1_ut/timing/ccs_db "]
read_vcd -rtl -strip_path test_aes_128/uut ${VCD_FILE} 
check_activity [get_pins *]
check_power
update_power

report_switching_activity > ${REPORT_DIR}/switching.rpt 
report_power -nosplit > ${REPORT_DIR}/pwr_group.rpt
report_power -nosplit -verbose -cell_power -hierarchy > ${REPORT_DIR}/pwr_cell.rpt
report_power -nosplit -verbose -leaf -hierarchy > ${REPORT_DIR}/pwr_leaf.rpt
report_power -nosplit -verbose -net_power > ${REPORT_DIR}/pwr_net.rpt

