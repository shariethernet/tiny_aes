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
source "$READ_SOURCES.tcl"
current_design $design
elaborate $design

source "/home/local/nu/shg/tiny_aes/constraints/max_freq_eval/constraints_128.sdc"
check_design
compile
change_names -rules verilog -hierarchy
#compile -ungroup_all -map_effort medium
if {[shell_is_in_xg_mode]==0} {
write -hier -o "${db_path}${design}.db"
} else {
write -format ddc -hier -o "${ddc_path}${design}.ddc"}
write_file -format verilog -hier -o "${netlist_path}${design}.v"
write_sdf "${netlist_path}${design}.sdf"
write_sdc "${netlist_path}${design}.sdc"
write_parasitics -output "${netlist_path}${design}parasitics.spef"
#write_floorplan -all "${netlist_path}${design}phy_cstr_file_fp.tcl"
source "/home/local/nu/shg/tiny_aes/constraints/report.tcl"