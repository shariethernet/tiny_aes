set source_path "rtl/"
set script_path "scripts/"
set design "aes_128"

proc create_dir {dir_name} {
  if {![file exists $dir_name]} {
    file mkdir $dir_name
    puts "Directory dosent exist so creating one"
  }
  return $dir_name
}

set log_path "[ create_dir "log"]/"
set ddc_path "[ create_dir ".ddc"]/"
set db_path "[ create_dir "db"]/"
set netlist_path "[ create_dir "netlist"]/"

set hdlin_enable_upf_compatible_naming true
#saif_map -start

source "$READ_SOURCES.tcl"
current_design $design
elaborate $design
#saif_map -write_map pp_map.tcl -type primepower
source "/home/local/nu/shg/tiny_aes/constraints/generated/c_GF22FDX_6P75T_104CPP_TT_0P80V_0P00V_0P00V_0P00V_25C/constraints_128.sdc"

check_design
compile
change_names -rules verilog -hierarchy
#compile -ungroup_all -map_effort medium
if {[shell_is_in_xg_mode]==0} {
write -hier -o "${db_path}${design}.db"
} else {
write_file -format ddc -hierarchy -output "${ddc_path}${design}.ddc"}
write_file -format verilog -hierarchy -output "${netlist_path}${design}.v"
write_sdf "${netlist_path}${design}.sdf"
write_sdc "${netlist_path}${design}.sdc"
write_parasitics -output "${netlist_path}${design}.spef"
#write_floorplan -all "${netlist_path}${design}phy_cstr_file_fp.tcl"
source "/home/local/nu/shg/tiny_aes/constraints/report.tcl"