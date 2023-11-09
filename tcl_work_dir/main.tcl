# initialize and import vhd files
# SET this to max numner of physical processors
set_param general.maxThreads 8
create_project <proj_name> <proj_dir> -part xczu9eg-ffvb1156-2-e -force
add_files <src_dir>
import_files -force
set_property top main [current_fileset]
update_compile_order -fileset sources_1

# import constraints
import_files -fileset constrs_1 -force -norecurse <cons_dir>

# import simulation files and simulate
add_files -fileset sim_1 <sim_dir>
set_property top main_tb [get_filesets sim_1]
set_property top_lib xil_defaultlib [get_filesets sim_1]
update_compile_order -fileset sim_1
set_property -name {xsim.simulate.runtime} -value {205000ns} -objects [get_filesets sim_1]
launch_simulation -simset sim_1 -quiet

# synthesize
# SET jobs to max numner of physical processors
launch_runs synth_1 -jobs 16 -quiet
wait_on_run synth_1 -quiet

# SET jobs to max numner of physical processors
launch_runs impl_1 -jobs 16 -quiet
wait_on_run impl_1 -quiet
open_run impl_1 -quiet

# Generate utilization, timing and power reports and write to disk
report_utilization -file <out_dir>/<file_name> -quiet
report_timing_summary -delay_type min_max -report_unconstrained -check_timing_verbose -max_paths 10 -input_pins -routable_nets -file <out_dir>/<file_name> -quiet
report_power -file <out_dir>/<file_name> -quiet

#start_gui
exit
